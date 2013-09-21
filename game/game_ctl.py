#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from utils.info_ctl import info_ctl
from utils.i18n import _
from utils.abstract_ctl import AbstractController
from kivy.properties import StringProperty,ObjectProperty
from game.game_view import GameScreen
import traceback
from kivy.logger import Logger
from piece_codes import *


b=[bR,bN,bB,bQ,bK,bB,bN,bR,
   bP,bP,bP,bP,bP,bP,bP,bP,
   xx,xx,xx,xx,xx,xx,xx,xx,
   xx,xx,xx,xx,xx,xx,xx,xx,
   xx,xx,xx,xx,xx,xx,xx,xx,
   xx,xx,xx,xx,xx,xx,xx,xx,
   wP,wP,wP,wP,wP,wP,wP,wP,
   wR,wN,wB,wQ,wK,wB,wN,wR
  ]
   
class GameCtl(AbstractController):
    screen_name='game'

    def createScreens(self):
        self.screen_manager.add_widget(GameScreen(name=self.screen_name))
    def prepareScreen(self):
        screen = self.screen_manager.get_screen(self.screen_name)
        screen.init_board()
        screen.board = b
        screen.draw_board()


game_ctl=GameCtl()

