#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEVICE='default'

def get_device(size):
    global DEVICE
    print str(size)
    if size==[1024,552]:
        DEVICE = "samsung7"
    elif size==[1280,752]:
        DEVICE = "samsung10"
    elif size==[1024,768]:
        DEVICE = "ipad2"
    else:
        DEVICE = "default"
    return DEVICE
        
def get_format(ftype,device=None):
    if not device:
        device = DEVICE
    # ratio aprox ipad_font = 1.5*normal font
    if ftype=='font12':
        if device=='ipad2':
            return "18sp"
        else:
            return "12sp"
    elif ftype=='font14':
        if device=='ipad2':
            return "22sp"
        else:
            return "14sp"
    elif ftype=='font18':
        if device=='ipad2':
            return "27sp"
        else:
            return "18sp"
    elif ftype=='font20':
        if device=='ipad2':
            return "30sp"
        else:
            return "20sp"
    elif ftype=='font30':
        if device=='ipad2':
            return "46sp"
        else:
            return "30sp"
    else:
        raise 'unknown format object'
