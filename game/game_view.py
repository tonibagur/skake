#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.i18n import _
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty,ListProperty,BooleanProperty
from kivy.logger import Logger
from utils.screen import ConeptumScreen
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('game/game.kv')

class GameScreen(ConeptumScreen):
    board_grid=ObjectProperty()
    board=ListProperty()
    
    def init_board(self):
        self.board_grid.clear_widgets()
        for i in range(64):
            sq=Square(dark_square=color(i))
            self.board_grid.add_widget(sq)
    
    def draw(self,b):
        self.board=b
        for index,square in enumerate(b):        
            print index,sqare

def fila_col(x):
    return x/8,x%8 
    
def color(i):
    f,c=fila_col(i)
    x1=(f%2)==1
    x2=(c%2)==1
    return (x1 or x2) and not(x1 and x2)

class Square(BoxLayout):
    __stereotype__ = StringProperty('widget')
    dark_square=BooleanProperty(True)
        
