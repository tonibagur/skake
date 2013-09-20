#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from game.game_ctl import game_ctl

from utils.i18n import _
from utils.abstract_ctl import AbstractController
from kivy.logger import Logger
from datetime import datetime
from kivy.clock import Clock
import traceback

class MainCtl(AbstractController):
    controllers=[game_ctl]

    def setScreenManager(self,manager):
        self.screen_manager=manager
        for c in self.controllers:
            c.set_screen_manager(manager)
            c.createScreens()

    def freeUnused(self):
        for c in self.controllers:
            if hasattr(c,'screen_name') and c.screen_name!=self.screen_manager.current:
                c.freeScreen()
            

    def scheduleTicks(self):
        self.last_time=datetime.now()
        Clock.schedule_interval(self.tick_clock, 30)
        
    def flush_time(self):
        n=datetime.now()
        delta=n-self.last_time
        seconds=delta.days*86400+delta.seconds
        self.last_time=n
        return seconds

    def tick_clock(self,*args,**kwargs):
        n=datetime.now()
        delta=n-self.last_time
        Logger.debug("Tick: time elapsed:" + str(delta)) 
        ok=False
        try:
            ok=self.screen_manager.current_screen.tick_clock(delta.days*86400+delta.seconds)
        except:
            print traceback.print_exc()
        if ok:
            self.last_time=n
        else:
            Logger.debug("Error registering time")
            
    def on_rol(self,value,sender):
        for c in self.controllers:
            c.rol=self.rol
            
    def on_platform(self,value,sender):
        for c in self.controllers:
            c.platform=self.platform
    def on_device(self,value,sender):
        for c in self.controllers:
            c.device=self.device
            
    def on_home_folder(self,value,sender):
        for c in self.controllers:
            c.home_folder=self.home_folder
    def on_debug(self,value,sender):
        for c in self.controllers:
            c.debug=self.debug
    
    def goto_first_view(self):
        game_ctl.showScreen()


main_ctl=MainCtl()

