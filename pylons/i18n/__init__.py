"""
Setuptools extensions and tools to add multiple language support
"""

import setuptools, sys, os, re

class LangExtract(setuptools.Command):

    description = "extract strings for internationalisation"
    user_options = []
    boolean_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
        
    def run(self):
        project = re.compile('[^a-zA-Z0-9_]').sub('', self.distribution.get_name().lower())
        oldsys = sys.argv
        sys.argv.pop(1)
        path = '%s/i18n/%s.pot'%(project, project)
        
        if os.path.exists(path):
            print "Error: File %s already exists"%path
            sys.exit()

        sys.argv.append('-K')
        sys.argv.append('-k')
        sys.argv.append('_')
        sys.argv.append('-o')
        sys.argv.append('%s.pot'%project)
        sys.argv.append('-p')
        sys.argv.append('%s/i18n/'%project)
        sys.argv.append('*')
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
        print "\nSucessfully created langauage template in %s\n"%path
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
        oldsys = sys.argv
        sys.argv = sys.argv[:1]
        sys.argv.append('-o')
        sys.argv.append('%s/i18n/%s/LC_MESSAGES/%s.mo'%(project,lang,project))
        sys.argv.append('%s/i18n/%s/%s.po'%(project,lang,project))
        if not os.path.exists('%s/i18n/%s'%(project,lang)) or not os.path.exists('%s/i18n/%s/%s.po'%(project,lang,project)):
            print "Error: Could not find the directory %s"%'%s/i18n/%s'%(project,lang)
            sys.exit()
        if not os.path.exists('%s/i18n/%s/LC_MESSAGES'%(project,lang)):
            os.mkdir('%s/i18n/%s/LC_MESSAGES'%(project,lang))
        import pylons.i18n.msgfmt
        pylons.i18n.msgfmt.main()
        print "Sucessfully generated '%s' catalog"%lang
        sys.argv = oldsys
        
    def run(self):
        project = re.compile('[^a-zA-Z0-9_]').sub('', self.distribution.get_name().lower())
        if not self.lang:
            print "No langauge specified, compiling all languages"
            for lang in os.listdir('%s/i18n/'%(project)):
                if os.path.isdir('%s/i18n/%s'%(project,lang)) and lang != '.svn':
                    self.compile_lang(lang)
        else:
            self.compile_lang(self.lang)