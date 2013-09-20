import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, DictProperty, NumericProperty, BooleanProperty
from kivy.lang import Builder

from utils.job import JobLoading
from utils.i18n import _
from utils.form_dialog_ctl import FormValidator
from utils.form_dialog_ctl import form_dialog_ctl
from utils.list_dialog_ctl import list_dialog_ctl
from utils.simple_controller import SimpleController
import traceback
from utils.forms import Form
from utils.datetimepicker import DateTimePicker
from kivy.logger import Logger

Builder.load_file('utils/form_fields.kv')


class JobDedo(JobLoading):
    job_id='_dedo'

    def do_job(self,callback):
        try:
            self.options=callback()
            self.job_state='finished'
        except:
            self.str_error=traceback.format_exc()
            self.job_state='error'
            Logger.log(self.str_error)
    

class DedoController(SimpleController):
    dedo=ObjectProperty()
    
    def on_job_finished_dedo(self,sender):
        self.options=sender.options
        list_dialog_ctl.choose_option(self.dedo.title_dialog,self.options ,self.callback_dialog,self.dedo.width_dialog, self.dedo.height_dialog,self.dedo.header_widget,self.dedo.header_widget_height) 
    def callback_dialog(self,option,option_text):
        if option:
            self.dedo.form.data[self.dedo.field_name]=(option,option_text)
            self.dedo.displayed_text=option_text
        else:
            self.dedo.displayed_text=''
            if self.dedo.field_name in self.dedo.form.data:
                del self.dedo.form.data[self.dedo.field_name]
                
class Dedo(BoxLayout):
    __stereotype__ = StringProperty('widget')
    field_name=StringProperty('')
    title=StringProperty('')
    title_dialog=StringProperty('Seleccione un valor')
    controller=ObjectProperty(None)
    form = ObjectProperty(None)
    displayed_text=StringProperty('')
    header_widget_height = NumericProperty(0)
    header_widget = ObjectProperty(None)
    width_dialog= NumericProperty(400)
    height_dialog = NumericProperty(500)
    display_text = BooleanProperty(True)
 
    def __init__(self,*args,**kwargs):
        super(Dedo,self).__init__(*args,**kwargs)
        self.ctl=DedoController() 
        self.ctl.dedo=self
    
    def press_dedo(self):
        j = JobDedo()
        j.controller=self.ctl
        callback=getattr(self.controller,'get_list_'+self.field_name)
        j.start_job(callback)

class DedoActController(DedoController):
    
    def callback_dialog(self,option,option_text):
        if option:
            self.dedo.form.data[self.dedo.field_name]=(option,option_text)
            self.dedo.displayed_text=option_text
            from utils.form_dialog_ctl import form_dialog_ctl
            from utils.form_dialog_ctl import FormValidator 
            from utils.form_dialog_ctl import Form 
            form_dialog_ctl.show_dialog('',LapizForm(),FormValidator(),self.callback_dialog2,400,200)

        else:
            self.dedo.displayed_text=''
            if self.dedo.field_name in self.dedo.form.data:
                del self.dedo.form.data[self.dedo.field_name]

    def callback_dialog2(self,data):
        if data:
            self.dedo.form.data['causa_interv2']=data['texto']
            self.dedo.displayed_text=self.dedo.displayed_text+' '+data['texto']
            
        else:
            self.dedo.displayed_text=''
            if self.dedo.field_name in self.dedo.form.data:
                del self.dedo.form.data[self.dedo.field_name]


class DedoActuacion(Dedo):

   def __init__(self,*args,**kwargs):
        super(DedoActuacion,self).__init__(*args,**kwargs)
        self.ctl=DedoActController() 
        self.ctl.dedo=self
        
        
 

class DedoControllerSearch(SimpleController):
    def callback_row(self,row):
        if row and self.dedo.display_text:
            self.dedo.form.data[self.dedo.field_name]=(row[self.dedo.field_search_id],row[self.dedo.field_search_name])
            self.dedo.displayed_text=row[self.dedo.field_search_name]
        elif row:
            self.dedo.form.data[self.dedo.field_name]=(row[self.dedo.field_search_id],row[self.dedo.field_search_name])
        else:
            self.dedo.displayed_text=''
            if self.dedo.field_name in self.dedo.form.data:
                del self.dedo.form.data[self.dedo.field_name]
        n_update = False
        if self.dedo.popup_ctl!=None:
            n_update = True
            self.dedo.popup_ctl.show_popup()
        self.dedo.controller.showScreen(item_selection=False,not_update=n_update)
        
class DedoControllerSearchFI(DedoControllerSearch):
    def callback_row(self,row):
        super(DedoControllerSearchFI,self).callback_row(row)
        self.dedo.controller_provider.frozen=False
        


class DedoSearch(Dedo):
    controller_provider=ObjectProperty(None)
    field_search_id=StringProperty('')
    field_search_name=StringProperty('')
    popup_ctl = ObjectProperty(None)
    def __init__(self,*args,**kwargs):
        super(Dedo,self).__init__(*args,**kwargs)
        self.ctl=DedoControllerSearch() 
        self.ctl.dedo=self
    def press_dedo(self):
        if self.popup_ctl!=None:
            self.popup_ctl.hide_popup()
        self.controller_provider.showScreen(item_selection=True,item_selection_callback=self.ctl.callback_row)


class DedoSearchFI(DedoSearch):
    
    def press_dedo(self):
        self.ctl=DedoControllerSearchFI()
        self.ctl.dedo=self
        if self.popup_ctl!=None:
            self.popup_ctl.hide_popup()
        if self.controller.ficha_interv == None: 
            self.controller.crear_fi()
        else:
            self.controller_provider.showScreen(item_selection=True,item_selection_callback=self.ctl.callback_row)



class LapizForm(BoxLayout,Form):
    __stereotype__ = StringProperty('widget')
    pass
    
    
class LapizController(SimpleController):
    lapiz=ObjectProperty()
        
    def callback_dialog(self,data):
        if data and 'texto' in data:
            self.lapiz.form.data[self.lapiz.field_name]=data['texto']
            self.lapiz.displayed_text=data['texto']
        else:
            self.lapiz.displayed_text=''
            if self.lapiz.field_name in self.lapiz.form.data:
                del self.lapiz.form.data[self.lapiz.field_name]        
    
    def callback_dialog_num(self,data):
        if data and 'val_actual' in data:
            self.lapiz.form.data[self.lapiz.field_name]=data['val_actual']
            self.lapiz.changed_value()
 
    def callback_dialog_txt(self,data):
        if data and 'texto' in data:
            self.lapiz.form.data[self.lapiz.field_name]=data['texto']
            self.lapiz.changed_value()
    
class Lapiz(BoxLayout):
    __stereotype__ = StringProperty('widget')
    field_name=StringProperty('')
    title=StringProperty('')
    title_dialog=StringProperty('Introduzca el texto:')
    controller=ObjectProperty(None)
    form = ObjectProperty(None)
    displayed_text=StringProperty('')
    display_text=BooleanProperty(True)
    
    def __init__(self,*args,**kwargs):
        super(Lapiz,self).__init__(*args,**kwargs)
        self.ctl=LapizController() 
        self.ctl.lapiz=self
        self.form_num_val = None
        self.form_lapiz = None
    
    def press_lapiz(self):
        form_dialog_ctl.show_dialog(self.title_dialog,LapizForm(init_vals={'texto':self.form.data[self.field_name] if self.field_name in self.form.data else ''}),FormValidator(),self.ctl.callback_dialog,400,200)      



class DateForm(DateTimePicker):
    pass

class DateController(SimpleController):
    date=ObjectProperty()
        
    def callback_dialog(self,data):
        if data and 'date' in data:
            self.date.form.data[self.date.field_name]=data['date']
            self.date.displayed_text=data['date_display']
        else:
            self.date.displayed_text=''
            if self.date.field_name in self.date.form.data:
                del self.date.form.data[self.date.field_name]        
        
class DateField(BoxLayout):
    __stereotype__ = StringProperty('widget')
    field_name=StringProperty('')
    title=StringProperty('')
    title_dialog=StringProperty('Introduzca el texto:')
    controller=ObjectProperty(None)
    form = ObjectProperty(None)
    displayed_text=StringProperty('')
    
    def __init__(self,*args,**kwargs):
        super(DateField,self).__init__(*args,**kwargs)
        self.ctl=DateController() 
        self.ctl.date=self
    
    def press_date(self):
        form_dialog_ctl.show_dialog(self.title_dialog,DateForm(init_vals={'date':self.form.data[self.field_name] if self.field_name in self.form.data else ''}),FormValidator(),self.ctl.callback_dialog)      

        
class CheckField(BoxLayout):
    __stereotype__ = StringProperty('widget')
    field_name=StringProperty('')
    title=StringProperty('')
    form = ObjectProperty(None)
    def press_check(self, active):
        if active:
            d=self.form.data.copy()
            d[self.field_name]=None
            self.form.data=d     
        else:
            if self.field_name in self.form.data:
                del self.form.data[self.field_name]  
                
class HideWidget(BoxLayout):
    __stereotype__ = StringProperty('widget')
    visible = BooleanProperty(True)
    hide_widget=ObjectProperty(None)
    
    def add_widget(self, widget, index=0):
        self.hide_widget = widget
        if self.visible:
            super(HideWidget, self).add_widget(self.hide_widget, index)
            
    def on_visible(self, sender, value):
        self.clear_widgets()
        if self.visible:
            super(HideWidget, self).add_widget(self.hide_widget, 1)

  
class FrmNumVal(BoxLayout, Form):
    val_anterior = StringProperty('0')
    val_actual = StringProperty('0')

class FrmEdit(BoxLayout, Form):
    controller = ObjectProperty()
    controller_dtr=ObjectProperty()
    popup_ctl=ObjectProperty(None)
    pass
class LayoutState(BoxLayout):
    __stereotype__ = StringProperty('widget')
    imagen=StringProperty('')

from utils.form_dialog_ctl import FormValidator
from kivy.uix.widget import Widget
class NumValidator(FormValidator,Widget):
    
    def validate(self):
        from utils.form_fields import Number
        if not Number().is_number(self.form.data['texto']):
            return False,_('el valor introducido debe ser un numero')
        return True,''

class Number: 
    __stereotype__ = StringProperty('other')
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
   
    def is_int(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    
