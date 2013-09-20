#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from utils.i18n import _
from kivy.properties import ObjectProperty,StringProperty
from utils.abstract_ctl import AbstractController

from kivy.lang import Builder
Builder.load_file('utils/info.kv')

class ErrorLayout(BoxLayout):
    __stereotype__ = StringProperty('widget')
    
    lbl=ObjectProperty(None)
    trace=ObjectProperty(None)
    btn=ObjectProperty(None)
    sc=ObjectProperty(None)
   
    def show_hide_trace(self):
        if self.sc.size[1] == 0:
            self.sc.size = (self.sc.size[0],150)
        else:
            self.sc.size = (self.sc.size[0],0) 

class MessageLayout(BoxLayout):
    __stereotype__ = StringProperty('widget')
    lbl=ObjectProperty(None)
    sc=ObjectProperty(None)
   
class InfoCtl(AbstractController):
    def error(self,titol,msg,trace):
        e=ErrorLayout()
        e.lbl.text=msg
        e.trace.text = trace
        e.btn.text=_('Aceptar')
        from utils.format import get_format
        popup = Popup(title_size=get_format('font14'),title=titol,
                      content=e,
                      size_hint=(None, None), size=(400, 400))
        e.btn.bind(on_press=popup.dismiss)
        popup.open()

    def createScreens(self):
        pass
    
    def show_message(self,titol,msg,aceptar_function=None,w=400,h=400):
        e=MessageLayout()
        self.aceptar_function=aceptar_function
        e.lbl.text=msg
        e.btn.text=_('Aceptar')
        from utils.format import get_format
        self.popup = Popup(title_size=get_format('font14'),title=titol,
                      content=e,
                      size_hint=(None, None), size=(w, h))
        e.btn.bind(on_press=self.on_press_aceptar)
        self.popup.open()
    def on_press_aceptar(self,instance):
        self.popup.dismiss()
        if self.aceptar_function:
            self.aceptar_function()


info_ctl=InfoCtl()
