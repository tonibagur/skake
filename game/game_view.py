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
from piece_codes import *

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
        #self.draw()
        pass
    
    def draw_board(self):
        for index,square in enumerate(self.board):
            self.board_grid.children[63-index].clear_widgets()
            if square != xx:
                print index,square
                p=Piece(piece=square,droppable_zone_objects=self.board_grid.children,drag_over_objects=self.board_grid.children,index=index,reference_widget=self,screen=self)
                self.board_grid.children[63-index].add_widget(p) 
                
    def move_to(self,piece,square):
        self.board[piece.index]=xx
        self.board[square.index]=piece.piece
        self.draw_board()

class Square(BoxLayout,DragOverZone):
    __stereotype__ = StringProperty('widget')
    dark_square=BooleanProperty(True)
    index=NumericProperty(0)
    color_square=ListProperty([0,0,0])
    def __init__(self,*args,**kwargs):
        super(Square,self).__init__(*args,**kwargs)
        if 'dark_square' in kwargs:
            self.color_square = (0.7,0.7,0.7) if kwargs['dark_square'] else (1,1,1)
        else:
            self.color_square = (0,0,0)
    def on_drag_over(self,*args,**kwargs):
        #super(Square,self).on_drag_over(*args,**kwargs)
        self.color_square=(0.7,0.7,0.7) if self.dark_square else (1,1,1)
        if self.drag_over:
            self.color_square[0]-=0.2
            self.color_square[1]-=0.2
    

class Piece(BoxLayout,DragNDropWidget):
    piece=NumericProperty()
    screen=ObjectProperty()
    index=NumericProperty()
    
    def get_texture(self):
        route='drawable/'
        if   self.piece==wR:
            return route+'wr.png'
        elif self.piece==wN:
            return route+'wn.png'
        elif self.piece==wB:
            return route+'wb.png'
        elif self.piece==wQ:
            return route+'wq.png'
        elif self.piece==wK:
            return route+'wk.png'
        elif self.piece==wP:
            return route+'wp.png'
        elif self.piece==bR:
            return route+'br.png'
        elif self.piece==bN:
            return route+'bn.png'
        elif self.piece==bB:
            return route+'bb.png'
        elif self.piece==bQ:
            return route+'bq.png'
        elif self.piece==bK:
            return route+'bk.png'
        elif self.piece==bP:
            return route+'bp.png'
        else:
            import pdb
            pdb.set_trace()
            assert False
            
    def move_to(self,dest,*args,**kwargs):
        self.screen.move_to(self,dest)

def fila_col(x):
    return x/8,x%8 
    
def color(i):
    f,c=fila_col(i)
    x1=(f%2)==1
    x2=(c%2)==1
    return (x1 or x2) and not(x1 and x2)
