import kivy

kivy.require('1.4.0')
from utils.i18n import _
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.app import App

from datetime import date, timedelta,datetime

from functools import partial
from kivy.properties import StringProperty,ObjectProperty
from utils.forms import Form
import calendar

class DatePicker(BoxLayout,Form):
    date=ObjectProperty(date.today())
    __stereotype__ = StringProperty('widget')
    
    def on_date(self,sender,value):
        self.data['date']=self.transform_date_oerp(value)
        self.data['date_display']=self.transform_date_human(value)
        self.populate_header()
        self.populate_body()
    
    def __init__(self, *args, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.orientation = "vertical"
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
        self.header = BoxLayout(orientation = 'horizontal', 
                                size_hint = (1, 0.2))
        self.body = GridLayout(cols = 7)
        self.add_widget(self.header)
        self.add_widget(self.body)

        self.populate_body()
        self.populate_header()
        if kwargs.has_key("init_vals"):
            if kwargs["init_vals"].has_key('date') and kwargs["init_vals"]['date']!='':
                self.date=datetime.strptime(kwargs["init_vals"]['date'],'%Y-%m-%d')
        self.data['date']=self.transform_date_oerp(self.date)
        self.data['date_display']=self.transform_date_human(self.date)

    def populate_header(self, *args, **kwargs):
        self.header.clear_widgets()
        previous_month = Button(text = "<")
        previous_month.bind(on_press=partial(self.move_previous_month))
        next_month = Button(text = ">")
        next_month.bind(on_press=partial(self.move_next_month))
        month_year_text = self.month_names[self.date.month -1] + ' ' + str(self.date.year)
        current_month = Label(text=month_year_text, size_hint = (2, 1))

        self.header.add_widget(previous_month)
        self.header.add_widget(current_month)
        self.header.add_widget(next_month)

    def populate_body(self, *args, **kwargs):
        self.body.clear_widgets()
        date_cursor = date(self.date.year, self.date.month, 1)
        for filler in range(date_cursor.isoweekday()-1):
            self.body.add_widget(Label(text=""))
        while date_cursor.month == self.date.month:
            date_label = Button(text = str(date_cursor.day))
            date_label.bind(on_press=partial(self.set_date,day=date_cursor.day))
            if self.date.day == date_cursor.day:
                date_label.background_normal, date_label.background_down = date_label.background_down, date_label.background_normal
            self.body.add_widget(date_label)
            date_cursor += timedelta(days = 1)

    def set_date(self, *args, **kwargs):
        self.date = date(self.date.year, self.date.month, kwargs['day'])
        self.populate_body()
        self.populate_header()

    def move_next_month(self, *args, **kwargs):
        if self.date.month == 12:
            self.date = date(self.date.year + 1, 1,min(self.date.day,calendar.monthrange(self.date.year,1)[1]) )
        else:
            self.date = date(self.date.year, self.date.month + 1,min(self.date.day,calendar.monthrange(self.date.year, self.date.month +1)[1]))
        self.populate_header()
        self.populate_body()

    def move_previous_month(self, *args, **kwargs):
        if self.date.month == 1:
            self.date = date(self.date.year - 1, 12, min(self.date.day,calendar.monthrange(self.date.year,12)[1]))
        else:
            self.date = date(self.date.year, self.date.month -1, min(self.date.day,calendar.monthrange(self.date.year, self.date.month -1)[1]))
        self.populate_header()
        self.populate_body()

    def transform_date_oerp(self, date):
        select_date = str(date.year)+'-'+str(date.month).zfill(2)+'-'+str(date.day).zfill(2)
        return select_date

    def transform_date_human(self, date):
        select_date = str(date.day).zfill(2)+'-'+str(date.month).zfill(2)+'-'+str(date.year)
        return select_date


# class MyApp(App):

    # def build(self):
        # return DatePicker()

# if __name__ == '__main__':
    # MyApp().run()
