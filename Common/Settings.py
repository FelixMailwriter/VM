# -*- coding:utf-8 -*-
import os
import sys
import locale
import gettext 


_=None

class Translate(object):
    
    def __init__(self):
        pass
    
    def lang_init(self, loc=''):
        if loc=='':
            _locale, _encoding = locale.getdefaultlocale()  # Default system values
        else:
            _locale=loc
            
        path = os.path.abspath(sys.argv[0])
        d=gettext.textdomain()
        gettext.install(d, unicode=True, codeset='utf-8')
        path = os.path.join(os.path.dirname(path),'locale')
        lang = gettext.translation(d, path, [_locale])

        return lang.ugettext
    
    def setLang(self, loc):
        global _
        _=self.lang_init(loc)
        
        


        