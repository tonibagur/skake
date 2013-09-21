#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.i18n import _
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty,ListProperty,BooleanProperty,NumericProperty
from kivy.logger import Logger
from utils.screen import ConeptumScreen
from kivy.uix.boxlayout import BoxLayout
from utils.drag_and_drop import DragNDropWidget,DragOverZone

Builder.load_file('game/game.kv')

class GameScreen(ConeptumScreen):
    board_grid=ObjectProperty()
    board=ListProperty()
    
    def init_board(self):
        self.board_grid.clear_widgets()
        for i in range(64):
            sq=Square(dark_square=color(i),index=i)
            self.board_grid.add_widget(sq)
    
    def on_board(self,*args,**kwargs):
        self.draw()
    
    def draw(self):
        for index,square in enumerate(self.board):
            self.board_grid.children[63-index].clear_widgets()
            if square != 'x':
                p=Piece(piece=square)
                self.board_grid.children[63-index].add_widget(p) 

class Square(BoxLayout,DragOverZone):
    __stereotype__ = StringProperty('widget')
    dark_square=BooleanProperty(True)
    index=NumericProperty(0)

class Piece(BoxLayout,DragNDropWidget):
    piece=StringProperty('')
    
    def get_texture(self):
        route='drawable/'
        if   self.piece=='R':
            return route+'wr.png'
        elif self.piece=='N':
            return route+'wn.png'
        elif self.piece=='B':
            return route+'wb.png'
        elif self.piece=='Q':
            return route+'wq.png'
        elif self.piece=='K':
            return route+'wk.png'
        elif self.piece=='P':
            return route+'wp.png'
        elif self.piece=='r':
            return route+'br.png'
        elif self.piece=='n':
            return route+'bn.png'
        elif self.piece=='b':
            return route+'bb.png'
        elif self.piece=='q':
            return route+'bq.png'
        elif self.piece=='k':
            return route+'bk.png'
        elif self.piece=='p':
            return route+'bp.png'
        else:
            assert False

def fila_col(x):
    return x/8,x%8 
    
def color(i):
    f,c=fila_col(i)
    x1=(f%2)==1
    x2=(c%2)==1
    return (x1 or x2) and not(x1 and x2)
