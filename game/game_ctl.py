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


b=['r','n','b','q','k','b','n','r',
   'p','p','p','p','p','p','p','p',
   'x','x','x','x','x','x','x','x',
   'x','x','x','x','x','x','x','x',
   'x','x','x','x','x','x','x','x',
   'x','x','x','x','x','x','x','x',
   'P','P','P','P','P','P','P','P',
   'R','N','B','Q','K','B','N','R'
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

