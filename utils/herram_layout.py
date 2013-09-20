from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,StringProperty
from kivy.lang import Builder

Builder.load_file('utils/herram_layout.kv')


class HerramLayout(BoxLayout):
    __stereotype__ = StringProperty('widget')
    controller=ObjectProperty()
    pass
