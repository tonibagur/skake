#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main_ctl import main_ctl
from utils.abstract_ctl import AbstractController

class SimpleController(AbstractController):
    def __init__(self):
        self.screen_manager=main_ctl.screen_manager
