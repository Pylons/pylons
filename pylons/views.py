from repoze.bfg.traversal import quote_path_segment

class LegacyView(object):
    def __init__(self, app):
        self.app = app # app is the legacy Pylons app

    def __call__(self, request):
        traversed = request.traversed
        vroot_path = request.virtual_root_path or ()
        view_name = request.view_name
        subpath = request.subpath or ()
        script_tuple = traversed[len(vroot_path):]
        script_list = [ quote_path_segment(name) for name in script_tuple ]
        script_name =  '/' + '/'.join(script_list)
        path_list = [ quote_path_segment(name) for name in subpath ] + [
            quote_path_segment(view_name) ]
        path_info = '/' + '/'.join(path_list)
        request.environ['PATH_INFO'] = path_info
        script_name = request.environ['SCRIPT_NAME'] + script_name
        if script_name.endswith('/'):
            script_name = script_name[:-1]
        request.environ['SCRIPT_NAME'] = script_name
        return request.get_response(self.app)
    
