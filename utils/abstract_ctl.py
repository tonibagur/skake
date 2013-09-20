#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.clock import Clock

from kivy.event import EventDispatcher

from kivy.properties import ObjectProperty,BooleanProperty,StringProperty

from utils.screen import BaseDebugable

class AbstractController(BaseDebugable):
    __stereotype__ = StringProperty('controller')
    item_selection=BooleanProperty(False)
    item_selection_callback=ObjectProperty(None,allownone=True)
    def set_screen_manager(self,screen_manager):
        self.screen_manager=screen_manager
    def createScreens(self):
        raise 'Not implemented'
    def prepareScreen(self):
        pass
    def postShowScreen(self,*largs):
        pass
    def free_mem(self):
        import gc
        print "before",len(gc.garbage)
        print "collected",str(gc.collect()),str(gc.isenabled())
        print "after",len(gc.garbage)

    def freeScreen(self):
        pass

    def showScreen(self,**kwargs):
        from main_ctl import main_ctl
        #self.free_mem()
        self.item_selection=False
        self.item_selection_callback=None
        if 'item_selection' in kwargs:
            self.item_selection=kwargs['item_selection']
        if 'item_selection_callback' in kwargs:
            self.item_selection_callback=kwargs['item_selection_callback']
        if 'not_update' in kwargs and kwargs['not_update']:
            self.screen_manager.current=self.screen_name
        else:
            self.prepareScreen()
            self.screen_manager.current=self.screen_name
            Clock.schedule_once(self.postShowScreen,1)
        main_ctl.freeUnused()
        self.free_mem()
        
    def get_screen(self):
        return self.screen_manager.get_screen(self.screen_name)
