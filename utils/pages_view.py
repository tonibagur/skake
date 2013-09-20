import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty,NumericProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

Builder.load_file('utils/pages_view.kv')

class PagesView(BoxLayout):
    __stereotype__ = StringProperty('widget')
    title = StringProperty()
    pag = ObjectProperty()
    layout_pages = ObjectProperty()
    num_pages = NumericProperty(0)
    def __init__(self, **kwargs):
        super(PagesView, self).__init__(**kwargs)
    def newPage(self,page):
        self.layout_pages.add_widget(page)
        self.num_pages = self.num_pages+1

class Bolas(BoxLayout):
    __stereotype__ = StringProperty('widget')
    n=NumericProperty()
    i=NumericProperty()
    def on_n(self,instance,value):
        self.clear_widgets()
        for k in range(0,value):
            bola = Bola()
            if self.i == k:
                bola.c = True
            self.add_widget(bola) 

    def on_i(self,instance,value):
        bolas=self.children
        for k in range(0,self.n):
            if k==self.n-value-1:
                bolas[k].c=True
            else:
                bolas[k].c=False

class Bola(Label):
    __stereotype__ = StringProperty('widget')
    c=BooleanProperty(False)
           




