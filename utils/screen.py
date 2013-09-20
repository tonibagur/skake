#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,StringProperty,NumericProperty
from kivy.event import EventDispatcher
from kivy.app import App
from kivy.logger import Logger


class BaseDebugable(EventDispatcher):
    __stereotype__ = StringProperty('other')
    platform=StringProperty('')
    debug=BooleanProperty('')
    customer=StringProperty('')
    device=StringProperty('')
    home_folder=StringProperty('')
    rol=StringProperty('')

class Debugable(BaseDebugable):
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

class ConeptumScreen(Screen,Debugable):
    __stereotype__ = StringProperty('screen')
    lost_time=NumericProperty()
    def get_user_dir(self):
        return App.get_running_app().user_data_dir
    
    def tick_clock(self,seconds):
        self.lost_time=self.lost_time + seconds
        Logger.debug("Lost time:"+str(self.lost_time))
        return True
        
    def set_trace(self):
        import pdb
        pdb.set_trace()

