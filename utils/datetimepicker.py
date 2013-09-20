import kivy

kivy.require('1.4.0')
#from utils.i18n import _
from i18n import _
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.app import App

from datetime import date, timedelta

from functools import partial
from kivy.properties import StringProperty,ObjectProperty,BooleanProperty
#from utils.forms import Form
from forms import Form
import calendar
import time, datetime

def _(text):
    #TODO, fix this issue, when col_data is initialized there is not running app
    return text  

class DateTimePicker(BoxLayout,Form):
    __stereotype__ = StringProperty('widget')
    date=ObjectProperty(date.today())
    time=ObjectProperty(datetime.datetime.now().time())
    show_time = BooleanProperty(False)
    
    def on_date(self,sender,value):
        self.data['date']=self.transform_date_oerp(value)
        self.data['date_display']=self.transform_date_human(value)
        self.populate_date_header()
        self.populate_date_body()
    
    def __init__(self, *args, **kwargs):
        super(DateTimePicker, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.date_widget = BoxLayout(orientation = 'vertical')
        self.month_names = (_('Enero'),
                            _('Febrero'), 
                            _('Marzo'), 
                            _('Abril'), 
                            _('Mayo'), 
                            _('Junio'), 
                            _('Julio'), 
                            _('Agosto'), 
                            _('Septiembre'), 
                            _('Octubre'),
                            _('Noviembre'),
                            _('Diciembre'))
        if kwargs.has_key("month_names"):
            self.month_names = kwargs['month_names']
        self.date_header = BoxLayout(orientation = 'horizontal',size_hint = (1, 0.2))
        self.date_body = GridLayout(cols = 7)         
        self.date_widget.add_widget(self.date_header)
        self.date_widget.add_widget(self.date_body)
        self.add_widget(self.date_widget)
        self.time_widget = BoxLayout(orientation = 'horizontal',size_hint = (0.5, 1))
            
        self.populate_date_body()
        self.populate_date_header()

        if kwargs.has_key("init_vals"):   
            if kwargs["init_vals"].has_key('show_time'):
                self.show_time = kwargs["init_vals"]['show_time']
            if kwargs["init_vals"].has_key('date') and kwargs["init_vals"]['date']!='':
                self.date=datetime.datetime.strptime(kwargs["init_vals"]['date'],'%Y-%m-%d %H:%M').date()
                if self.show_time:
                    self.time=datetime.datetime.strptime(kwargs["init_vals"]['date'],'%Y-%m-%d %H:%M').time()
        self.data['date']=self.transform_date_oerp(self.date)
        self.data['date_display']=self.transform_date_human(self.date) 
        self.data['time'] = str(self.time)
        if self.show_time:
            label_aux1 = Label(text='',size_hint = (0.1, 1)) 
            self.add_widget(label_aux1)
            self.add_widget(self.time_widget)
            self.populate_time()

    def populate_date_header(self, *args, **kwargs):
        self.date_header.clear_widgets()
        previous_month = Button(text = "<")
        previous_month.bind(on_press=partial(self.move_previous_month))
        next_month = Button(text = ">")
        next_month.bind(on_press=partial(self.move_next_month))
        month_year_text = self.month_names[self.date.month -1] + ' ' + str(self.date.year)
        current_month = Label(text=month_year_text, size_hint = (2, 1))

        self.date_header.add_widget(previous_month)
        self.date_header.add_widget(current_month)
        self.date_header.add_widget(next_month)

    def populate_date_body(self, *args, **kwargs):
        self.date_body.clear_widgets()
        date_cursor = date(self.date.year, self.date.month, 1)
        for filler in range(date_cursor.isoweekday()-1):
            self.date_body.add_widget(Label(text=""))
        while date_cursor.month == self.date.month:
            date_label = Button(text = str(date_cursor.day))
            date_label.bind(on_press=partial(self.set_date,day=date_cursor.day))
            if self.date.day == date_cursor.day:
                date_label.background_normal, date_label.background_down = date_label.background_down, date_label.background_normal
            self.date_body.add_widget(date_label)
            date_cursor += timedelta(days = 1)

    def populate_time(self, *args, **kwargs):
        self.data['time'] = str(self.time)
        self.time_widget.clear_widgets()
        next_hour = Button(text = "+")
        next_hour.bind(on_press=partial(self.move_next_hour))
        previous_hour = Button(text = "-")
        previous_hour.bind(on_press=partial(self.move_previous_hour))
        next_minute = Button(text = "+")
        next_minute.bind(on_press=partial(self.move_next_minute))
        previous_minute = Button(text = "-")
        previous_minute.bind(on_press=partial(self.move_previous_minute))
        hour_text = str(self.time.hour).zfill(2)
        minute_text = str(self.time.minute).zfill(2)
        current_hour = Label(text=hour_text)
        current_minute = Label(text=minute_text)

        self.hour_widget = BoxLayout(orientation = 'vertical')
        self.minute_widget = BoxLayout(orientation = 'vertical')  
        label_aux1 = Label(text='') 
        label_aux2 = Label(text='') 
        self.hour_widget.add_widget(label_aux1)
        self.minute_widget.add_widget(label_aux2)    
        self.hour_widget.add_widget(next_hour)
        self.hour_widget.add_widget(current_hour)
        self.hour_widget.add_widget(previous_hour)
        self.minute_widget.add_widget(next_minute)
        self.minute_widget.add_widget(current_minute)
        self.minute_widget.add_widget(previous_minute)
        label_aux1 = Label(text='') 
        label_aux2 = Label(text='') 
        self.hour_widget.add_widget(label_aux1)
        self.minute_widget.add_widget(label_aux2)  

        time_widget_aux = BoxLayout(orientation = 'vertical',size_hint_x=0.2)
        label_aux1 = Label(text='')        
        label_aux2 = Label(text=':')
        label_aux3 = Label(text='') 
        time_widget_aux.add_widget(label_aux1)
        time_widget_aux.add_widget(label_aux2)
        time_widget_aux.add_widget(label_aux3)


        self.time_widget.add_widget(self.hour_widget)
        self.time_widget.add_widget(time_widget_aux)
        self.time_widget.add_widget(self.minute_widget)


    def set_date(self, *args, **kwargs):
        self.date = date(self.date.year, self.date.month, kwargs['day'])
        self.populate_date_body()
        self.populate_date_header()

    def move_next_month(self, *args, **kwargs):
        if self.date.month == 12:
            self.date = date(self.date.year + 1, 1,min(self.date.day,calendar.monthrange(self.date.year,1)[1]) )
        else:
            self.date = date(self.date.year, self.date.month + 1,min(self.date.day,calendar.monthrange(self.date.year, self.date.month +1)[1]))
        self.populate_date_header()
        self.populate_date_body()

    def move_previous_month(self, *args, **kwargs):
        if self.date.month == 1:
            self.date = date(self.date.year - 1, 12, min(self.date.day,calendar.monthrange(self.date.year,12)[1]))
        else:
            self.date = date(self.date.year, self.date.month -1, min(self.date.day,calendar.monthrange(self.date.year, self.date.month -1)[1]))
        self.populate_date_header()
        self.populate_date_body()

    def move_next_hour(self, *args, **kwargs):
        self.time = datetime.time((self.time.hour+1)%24,self.time.minute,self.time.second)
        self.populate_time()

    def move_previous_hour(self, *args, **kwargs):
        self.time = datetime.time((self.time.hour-1)%24,self.time.minute,self.time.second)
        self.populate_time()

    def move_next_minute(self, *args, **kwargs):
        self.time = datetime.time(self.time.hour,(self.time.minute+1)%60,self.time.second)
        self.populate_time()

    def move_previous_minute(self, *args, **kwargs):
        self.time = datetime.time(self.time.hour,(self.time.minute-1)%60,self.time.second)
        self.populate_time()

    def transform_date_oerp(self, date):
        select_date = str(date.year)+'-'+str(date.month).zfill(2)+'-'+str(date.day).zfill(2)
        return select_date

    def transform_date_human(self, date):
        select_date = str(date.day).zfill(2)+'-'+str(date.month).zfill(2)+'-'+str(date.year)
        return select_date


#class MyApp(App):

    #def build(self):
        #return DateTimePicker()

#if __name__ == '__main__':
    #MyApp().run()
