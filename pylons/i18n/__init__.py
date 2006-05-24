"""
Setuptools extensions and tools to add multiple language support
"""
import setuptools, sys, os, re

# Ignore these directories when iterating through paths
exclude_dirs = ('.AppleDouble', '.svn', 'CVS', '_darcs')

class LangExtract(setuptools.Command):

    description = "extract strings for internationalisation"
    user_options = []
    boolean_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
        
    def run(self):
        project = re.compile('[^a-zA-Z0-9_]').sub('', self.distribution.get_name().lower())
        i18n_path = os.path.join(project, 'i18n%s' % os.sep)
        pot_filename = '%s.pot' % project
        pot_path = os.path.join(i18n_path, pot_filename)
        
        if os.path.exists(pot_path):
            print "Error: File %s already exists" % pot_path
            sys.exit(1)

        oldsys = sys.argv
        sys.argv.pop(1)
        sys.argv.extend(['-K', '-k', '_', '-o', pot_filename, '-p', i18n_path, '*'])
        
        import pylons.i18n.pygettext
        pylons.i18n.pygettext.pot_header = '''\
# Pylons Project %s Translation File
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: %%(time)s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: %s <%s>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: ENCODING\\n"
"Generated-By: Pylons %%(version)s\\n"

''' % (
        project,
        self.distribution.get_author().lower(),
        self.distribution.get_author_email().lower(), 
        )
        # These could be filled in from setup.py
        pylons.i18n.pygettext.main()
        print "\nSucessfully created langauage template in %s\n" % pot_path
        print """Now create your langauge files, save them in i18n/lang replacing 
lang with the language code and changing the file extension to .po then run 
setup.py lang_compile mode to produce your .mo files"""

        sys.argv = oldsys

class LangCompile(setuptools.Command):
    description = "compile strings for internationalisation"
    user_options = [('lang=', 'l', "language to compile"),]
    boolean_options = []
    def finalize_options(self): pass

    def initialize_options(self): 
        self.lang = None
        
    def compile_lang(self, lang):
        project = re.compile('[^a-zA-Z0-9_]').sub('', self.distribution.get_name().lower())
        lang_path = os.path.join(project, 'i18n', lang)
        po_path = os.path.join(lang_path, '%s.po' % project)
        lc_path = os.path.join(lang_path, 'LC_MESSAGES')
        mo_path = os.path.join(lc_path, '%s.mo' % project)

        if not os.path.exists(lang_path) or not os.path.exists(po_path):
            print "Error: Could not find the directory %s" % lang_path
            sys.exit(1)
        if not os.path.exists(lc_path):
            os.mkdir(lc_path)
        
        oldsys = sys.argv
        sys.argv = [sys.argv[0], '-o', mo_path, po_path]

        import pylons.i18n.msgfmt
        pylons.i18n.msgfmt.main()
        print "Sucessfully generated '%s' catalog" % lang
        
        sys.argv = oldsys
        
    def run(self):
        project = re.compile('[^a-zA-Z0-9_]').sub('', self.distribution.get_name().lower())
        if not self.lang:
            print "No langauge specified, compiling all languages"
            i18n_path = os.path.join(project, 'i18n')
            for lang in os.listdir(i18n_path):
                if os.path.isdir(os.path.join(i18n_path, lang)) and \
                                     lang not in exclude_dirs:
                    self.compile_lang(lang)
        else:
            self.compile_lang(self.lang)
