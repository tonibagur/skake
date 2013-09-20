#!/usr/bin/env python
# -*- coding: utf-8 -*-

import StringIO
from kivy.graphics.texture import Texture
from PIL import Image,ImageDraw,ImagePath
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
import base64
import weakref
from kivy.properties import StringProperty

class ImageReloader(EventDispatcher):
    __stereotype__ = StringProperty('other')
    image=ObjectProperty()
    def __init__(self,*args,**kwargs):
        super(ImageReloader,self).__init__(*args,**kwargs)
        self.texture=weakref.ref(kwargs['texture'])
    
    def __call__(self,*args,**kwargs):
        print "Reloading Texture"
        self.texture().blit_buffer(self.image.convert("RGB").tostring("raw", "RGB"),colorfmt='rgb')

def get_texture_from_b64(b64_data,size=None):
    jpg_data=base64.b64decode(b64_data)
    return get_texture_from_jpeg(jpg_data,size)
    
def set_texture_from_b64(t,b64_data,size=None):
    if b64_data:
        jpg_data=base64.b64decode(b64_data)
        set_texture_from_jpeg(t,jpg_data,size)
    else:
        t.texture_dtr=None
    
def get_pil_from_b64(b64_data):
    jpg_data=base64.b64decode(b64_data)
    buff=StringIO.StringIO()
    buff.write(jpg_data)
    buff.seek(0)
    i = Image.open(buff)
    return i
    
def get_b64_from_pil(pil_image,fmt='PNG'):
    buff=StringIO.StringIO()
    pil_image.save(buff,format=fmt)
    buff.seek(0)
    return base64.b64encode(buff.read())
    
def get_texture_from_jpeg(jpg_data,size=None):    
    buff=StringIO.StringIO()
    buff.write(jpg_data)
    buff.seek(0)
    i = Image.open(buff)
    if size:
        i.thumbnail(size, Image.ANTIALIAS)
    t = Texture.create(size=i.size,colorfmt='rgb',mipmap=True)
    t.flip_vertical()
    t.blit_buffer(i.convert("RGB").tostring("raw", "RGB"),colorfmt='rgb')
    t.add_reload_observer(ImageReloader(image=i,texture=t))
    return t

def set_texture_from_jpeg(it,jpg_data,size=None):    
    buff=StringIO.StringIO()
    buff.write(jpg_data)
    buff.seek(0)
    i = Image.open(buff)
    if size:
        i.thumbnail(size, Image.ANTIALIAS)
    if not it.texture_dtr:
        it.texture_dtr= Texture.create(size=i.size,colorfmt='rgb',mipmap=True)
        it.texture_dtr.flip_vertical()  
    it.texture_dtr.blit_buffer(i.convert("RGB").tostring("raw", "RGB"),colorfmt='rgb')
    it.texture_dtr.add_reload_observer(ImageReloader(image=i,texture=it.texture_dtr))

class DrawConeptum(ImageDraw.ImageDraw):
    __stereotype__ = StringProperty('other')
    
    def line(self, xy, fill=None, width=0):
        ink, fill = self._getink(fill)
        if ink is None:
            return
        if width <= 1:
            self.draw.draw_lines(xy, ink)
        else:
            # hackelihack!
            xy = ImagePath.Path(xy)
            self.draw.draw_lines(xy, ink)
            xy.transform((1, 0, -1, 0, 1, 0))
            self.draw.draw_lines(xy, ink)
            xy.transform((1, 0, 0, 0, 1, -1))
            self.draw.draw_lines(xy, ink)
            xy.transform((1, 0, 1, 0, 1, 0))
            self.draw.draw_lines(xy, ink)
    
