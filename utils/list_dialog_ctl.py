#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from i18n import _
from kivy.properties import ObjectProperty,StringProperty,NumericProperty,ListProperty
from abstract_ctl import AbstractController

from grid import DataGridAdapter
from grid import DataGridField
from kivy.logger import Logger


from kivy.lang import Builder

from kivy.app import App

try:
    Builder.load_file('utils/list_dialog.kv')
except:
    pass



class ListDialog(BoxLayout):
    __stereotype__ = StringProperty('widget')
    adapter=ObjectProperty(None)
    btn=ObjectProperty(None)
    header_height_hint=NumericProperty(0.)
    datagrid=ObjectProperty(None)
    controller=ObjectProperty(None)
    header_container=ObjectProperty(None)
    header_widget_height=NumericProperty(10)

class ButtonListDialog(ToggleButton):
    __stereotype__ = StringProperty('widget')
    option_id=StringProperty(None)


class ListDialogAdapter(DataGridAdapter):
    cols_data=ListProperty([('option','Option',1)])
    data=ListProperty([{'option_id':'o'+str(i),'option':'Option'+str(i)} for i in range(20)])
    controller=ObjectProperty()
    option_id = StringProperty('')
    text = StringProperty('')
     
    def get_col_widget(self,col):
        return Label(text='')

    def get_element(self,row,col,num_elem,f=None):
        if not f:
            btn=ButtonListDialog(text=row['option'],group='dialog',option_id=row['option_id'])
            if row['option_id'] == self.option_id:
                self.option_changed(btn)
            btn.bind(on_press=self.option_changed)
            return btn
        else:
            w=self.get_col_element(col,f)
            w.text=row['option']
            w.group='dialog'
            w.option_id=row['option_id']
            if row['option_id'] == self.option_id:
                self.option_changed(w)
            w.bind(on_press=self.option_changed)
            return w

    def option_changed(self,sender,**kwargs):
        sender.state='down'
        self.controller.set_option(sender.option_id,sender.text)
        self.controller.result='ok'
        self.selected_option=sender.option_id

class ListDialogCtl(AbstractController):
    def set_option(self,option_id,option_text):
        self.option_id=option_id
        self.option_text=option_text
        self.l.btn.disabled=False
    def choose_option(self,titol,options,option_callback,width=400,height=500,header_widget=None,header_widget_height=10,option_sel=''):
        if not option_sel or option_sel == '':
            option_sel = options[0]['option_id']
        self.option_callback=option_callback
        self.l=ListDialog()
        self.l.controller=self 
        text_list = [x for x in options if x['option_id']==option_sel]
        text = (text_list and text_list[0]['option']) or ''
        print 'TEXT ' +str(text)
        self.result='ko'
        self.option_id=None
        self.option_text=''
        self.l.adapter=ListDialogAdapter(grid=self.l.datagrid,option_id=str(option_sel),text=text)
        self.l.adapter.controller=self
        self.l.adapter.data=options
        self.l.datagrid.header_height_hint=0.
        self.l.header_widget_height=header_widget_height
        if header_widget:
            header_widget.parent=None
            self.l.header_container.add_widget(header_widget)
        else:
            self.l.header_container.add_widget(Label())
            self.l.header_widget_height=10
        from utils.format import get_format
        self.popup = Popup(title_size=get_format('font14'),title=titol,
                      content=self.l,
                      size_hint=(None, None), size=(width, height))
        self.visto = False
        self.l.btn.bind(on_press=self.visto_pressed)
        self.popup.bind(on_dismiss=self.sendOption)
        self.popup.open()

    def visto_pressed(self, sender):
        self.visto = True
        self.popup.dismiss()


    def refreshOptions(self,options):
        self.l.adapter.data=options

    def sendOption(self,sender):

        if self.result=='ko' or not self.visto:
            return self.option_callback(None,'')
        else:
            return self.option_callback(self.option_id,self.option_text)

    def createScreens(self):
        pass
    

list_dialog_ctl=ListDialogCtl()


def test_option(option_id):
    Logger.debug(str(option_id)+"has chosen")

class Main(App):
    def get_text(self,t):
        return t

    def build(self):
        # fields,col_hints,data,class,adapter
        b=Button(text='hello')
        b.bind(on_press=self.dialog)
        self.root=b
        return self.root
    def dialog(self,*args,**kwargs):
        ListDialogCtl().choose_option('Hola mon',[{'option_id':i,'option':'Option '+str(i)} for i in range(30)],test_option,600,600,Label(text='Custom widget'),40)


if __name__ in ('__main__'):
    app = Main()
    app.run()
