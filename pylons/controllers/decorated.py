"""Decorated Controller"""
import logging

import formencode

import pylons
from pylons.controllers import WSGIController

log = logging.getLogger(__name__)

def _configured_engines():
    """Returns set with the currently configured template engine's names
    from the active application's globals"""
    g = pylons.g._current_obj()
    if not hasattr(g, 'tg_configured_engines'):
        g.tg_configured_engines = set()
    return g.tg_configured_engines


class DecoratedController(WSGIController):

    def _perform_validate(self, controller, params):
        validation = getattr(controller.decoration, 'validation', None)
        if validation is None:
            return params
        
        new_params = None
        if isinstance(validation.validators, dict):
            errors = {}
            #new_params = {}
            for field, validator in validation.validators.iteritems():
                try:
                    new_params[field] = validator.to_python(params.get(field))
                except formencode.api.Invalid, inv:
                    errors[field] = inv

            if errors:
                raise formencode.api.Invalid(
                    formencode.schema.format_compound_error(errors),
                    params, None, error_dict=errors)
        elif isinstance(validation.validators, formencode.Schema):
            new_params = validation.validators.to_python(params)
        elif hasattr(validation.validators, 'validate'):
            new_params = validation.validators.validate(params)

        if new_params is None:
            return params
        return new_params

    def _render_response(self, controller, response):
        """Render response takes the dictionary returned by the
        controller calls the appropriate template engine. It uses
        information off of the decoration object to decide which engine
        and template to use, and removes anything in the exclude_names
        list from the returned dictionary.

        The exclude_names functionality allows you to pass variables to
        some template rendering engines, but not others. This behavior
        is particularly useful for rendering engines like JSON or other
        "web service" style engines which don't use and explicit
        template.

        All of these values are populated into the context object by the
        expose decorator.
        """
        content_type, engine_name, template_name, exclude_names = \
            controller.decoration.lookup_template_engine(pylons.request)

        # Always set content type
        pylons.response.headers['Content-Type'] = content_type 
        req = pylons.request

        if template_name is None:
            return response

        #Prepare the engine, if it's not already been prepared.

        if engine_name not in _configured_engines():
            from pylons import config
            template_options = dict(config).get('buffet.template_options', {})
            pylons.buffet.prepare(engine_name, **template_options)
            _configured_engines().add(engine_name)

        # Setup the template namespace, removing anything that the user
        # has marked to be excluded.
        namespace = dict(context=pylons.c)
        namespace.update(response)

        for name in exclude_names:
            namespace.pop(name)

        # If we are in a test request put the namespace where it can be accessed directly
        if req.environ.get('paste.testing'):
            req.environ['paste.testing_variables']['namespace'] = namespace
            req.environ['paste.testing_variables']['template_name'] = template_name
            req.environ['paste.testing_variables']['exclude_names'] = exclude_names

        # Render the result.
        result = pylons.buffet.render(engine_name=engine_name,
                                      template_name=template_name,
                                      include_pylons_variables=False,
                                      namespace=namespace)
        return result

    def _handle_validation_errors(self, controller, exception):
        pylons.c.form_errors = exception.error_dict
        pylons.c.form_values = exception.value

        error_handler = controller.decoration.validation.error_handler
        if error_handler is None:
            error_handler = controller

        output = error_handler(controller.im_self)

        return error_handler, output

    def _perform_call(self, func, args, remainder=None):
        if remainder is None:
            remainder = []
        try:
            controller, params = func, args
            pylons.request.headers['tg_format'] = params.get('tg_format', None)

            # Validate user input
            controller.decoration.run_hooks('before_validate', remainder,
                                            params)
            params = self._perform_validate(controller, params)
            pylons.c.form_values = params

            # call controller method
            controller.decoration.run_hooks('before_call', remainder, params)
            output = controller(*remainder, **dict(params))

        except formencode.api.Invalid, inv:
            controller, output = self._handle_validation_errors(controller,
                                                                inv)

        # Render template
        controller.decoration.run_hooks('before_render', remainder, params,
                                        output)
        response = self._render_response(controller, output)
        controller.decoration.run_hooks('after_render', response)
        return response
