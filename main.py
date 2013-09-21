#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import prof

from utils.i18n import _

from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition
from kivy.app import App

from kivy.properties import BooleanProperty,StringProperty
from kivy.utils import platform as core_platform

import os
import gettext
from utils.format import get_device


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


dir = os.path.dirname(__file__)
languagePath = os.path.join(dir, 'language')
gettext.bindtextdomain('multilingual', languagePath)


from main_ctl import main_ctl

__coneptum_debug__=False
__customer__='coneptum'
__device__='default_device'
__monitor_time__=False


class MyScreenManager(ScreenManager):
    all_widgets_disabled=BooleanProperty(False)
    debug=BooleanProperty(__coneptum_debug__)
    platform=StringProperty(core_platform())
    customer=StringProperty(__customer__)
    device=StringProperty(__device__)
    home_folder=StringProperty('')
    rol=StringProperty('')
    
    def on_debug(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'debug'):
                widget.debug=self.debug
    def on_platform(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'platform'):
                widget.platform=self.platform
                
    def on_customer(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'customer'):
                widget.customer=self.customer  
                
    def on_size(self,sender,value):
        self.device=get_device(self.size)

    def on_device(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'device'):
                widget.device=self.device  
                
    def on_home_folder(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'home_folder'):
                widget.home_folder=self.home_folder 

    def on_rol(self,*args,**kwargs):
        for widget in self.children:
            if hasattr(widget,'rol'):
                widget.rol=self.rol

    def dispatch(self,*args,**kwargs):
        if not self.all_widgets_disabled:
            return super(MyScreenManager,self).dispatch(*args,**kwargs)
        else:
            return None
    def add_widget(self,widget,*args):
        super(MyScreenManager,self).add_widget(widget,*args)
        if hasattr(widget,'debug'):
            widget.debug=self.debug
        if hasattr(widget,'platform'):
            widget.platform=self.platform
        if hasattr(widget,'customer'):
            widget.customer=self.customer
        if hasattr(widget,'home_folder'):
            widget.home_folder=self.home_folder  
        if hasattr(widget,'rol'):
            widget.rol=self.rol       
        if hasattr(widget,'device'):
            widget.device=self.device   

class EscacApp(App):
    
    def run(self):
        try:
            super(EscacApp,self).run()
        except:
            import traceback
            error=traceback.format_exc()
            print error
            subject ='Error no controlado en la aplicación Railkivy'
            
            

    def build(self):
        self.platform=core_platform()
        self.setup()
        self.set_language('es_ES')
        self.root = MyScreenManager(transition=FadeTransition(),home_folder=self.user_data_dir)
        main_ctl.setScreenManager(self.root)
        if __monitor_time__:
            main_ctl.scheduleTicks()
        main_ctl.goto_first_view()
        debug=BooleanProperty(__coneptum_debug__)
        self.customer=__customer__
        self.home_folder=''
        return self.root

    def setup(self):
        if self.platform not in ('ios','android'):
            from kivy.config import Config
            Config.set('graphics', 'width', '1000')
            Config.set('graphics', 'height', '700')
            Config.write()

    def set_language(self,selectedLanguage):
        self.t = gettext.translation('multilingual', languagePath, languages=[selectedLanguage], fallback=True)
        _ = self.t.ugettext #The 'u' in 'ugettext' is for Unicode - use this to keep Unicode from breaking the app
        #self.root.greeting = _('Hello!')

    def get_text(self, *args):
        return self.t.gettext(*args)

    def on_pause(self):
        return True

    def on_resume(self):
        return True

if __name__ == '__main__':
    EscacApp().run()
