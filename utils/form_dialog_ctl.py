#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from i18n import _
from kivy.properties import ObjectProperty,StringProperty,NumericProperty,ListProperty,BooleanProperty
from abstract_ctl import AbstractController
from forms import Form 
from utils.job import JobLoading
import traceback
from kivy.logger import Logger


from kivy.lang import Builder

from kivy.app import App

try:
    Builder.load_file('utils/form_dialog.kv')
except:
    pass



class FormDialog(BoxLayout):
    __stereotype__ = StringProperty('widget')
    btn=ObjectProperty(None)
    btn_goma=ObjectProperty(None)
    goma_visible=BooleanProperty(False)
    controller=ObjectProperty(None)

class FormDialogCtl(AbstractController):
    goma_visible=BooleanProperty(False)
    
    def show_dialog(self,titol,wf,validator,form_callback,width=400,height=500):
        self.form_callback=form_callback
        self.wf = wf
        self.validator = validator
        self.l=FormDialog(goma_visible=self.goma_visible)
        self.l.formulario.add_widget(wf)
        self.l.controller=self
        self.titol = titol
        self.w=width
        self.h=height
        from utils.format import get_format
        self.popup = Popup(title_size=get_format('font14'),title=titol,
                      content=self.l,
                      size_hint=(None, None), size=(width, height),pos_hint={'center_x':0.5,'center_y':0.75}  
    )
        self.popup_temp =False
        self.result='ko'
        self.option_text=''
        self.l.btn.bind(on_press=self.validate)
        self.l.btn_goma.bind(on_press=self.goma_press)
        self.popup.bind(on_dismiss=self.sendData)
        self.popup.open()


    def goma_press(self,sender):
        self.result = 'goma'
        self.popup.dismiss()

    def validate(self,sender):
        self.j = JobValidator()
        self.j.controller=self
        self.j.start_job(self.validator) 
    def sendData(self,sender):
        self.deshabilitar_focus(self.wf)
        if self.popup_temp:
            return
        if self.result=='ko':
            return self.form_callback(None)
        elif self.result=='goma':
            self.wf.data['state']='borrando'
            return self.form_callback(self.wf.data)
        else:
            return self.form_callback(self.wf.data)

    def deshabilitar_focus(self, wf):
        for c in wf.children:
            if str(type(c)) == "<class 'kivy.uix.textinput.TextInput'>":
                c.focus = False
            elif len(c.children) > 0:
                self.deshabilitar_focus(c)


    def hide_popup(self):
        self.popup_temp = True
        self.popup.dismiss()

    def show_popup(self):
        self.popup_temp =False
        self.l.parent.remove_widget(self.l)
        from utils.format import get_format
        self.popup = Popup(title_size=get_format('font14'),title=self.titol,
                      content=self.l,
                      size_hint=(None, None), size=(self.w, self.h))
        self.l.btn.bind(on_press=self.validate)
        self.popup.bind(on_dismiss=self.sendData)
        self.popup.open()

    def createScreens(self):
        pass

    def on_job_finished_validator(self,sender):
        if self.j.result:
            self.result = 'ok'
            self.popup.dismiss()
        else:
            from utils.info_ctl import info_ctl
            info_ctl.error(_('Error el valor'),self.j.message,'')
            Logger.error("formulari invalid,TODO:implement feedback")
    

form_dialog_ctl=FormDialogCtl()



class FormValidator:
    form = ObjectProperty()
    __stereotype__ = StringProperty('other')
    

    def validate(self):
        return True,''

#TODO: Possiblement seria millor heretar directament de Job i redefinir certs aspectes del comportament
class JobValidator(JobLoading):
    job_id='_validator'
    def do_job(self,validator):
        try:
            self.result,self.message=validator.validate()
            self.job_state='finished'
        except:
            self.str_error=traceback.format_exc()
            self.job_state='error'
            Logger.error(self.str_error)


Builder.load_string('''
<WidgetForm>:
    orientation:'vertical'
    Label:
        text:'test WidgetForm'
    Button:
        text:'test Button'
''')

class WidgetForm(BoxLayout,Form):
    __stereotype__ = StringProperty('widget')
    

def validator(wf):
    return True

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
        wf = WidgetForm()
        FormDialogCtl().show_dialog('Hola mon',wf,validator,test)


if __name__ in ('__main__'):
    app = Main()
    app.run()
