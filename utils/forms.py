#!/usr/bin/env python
# -*- coding: utf-8 -*-
from i18n import _
from kivy.event import EventDispatcher
from kivy.properties import DictProperty,NumericProperty,ListProperty,StringProperty


class Form(EventDispatcher):
    __stereotype__ = StringProperty('other')
    data=DictProperty({})
    def __init__(self,*args,**kwargs):
        super(Form,self).__init__(*args,**kwargs)
        if 'init_vals' in kwargs:
            self.data=kwargs['init_vals']
    def value_changed(self,field_name,value):
        if value != '':
            self.data[field_name]=str(value)
        elif field_name in self.data:
            del self.data[field_name]
    

class Filter(Form):
    filters=ListProperty([])
    def on_data(self,sender,value):
        self.filters=[]
        for k in self.data:
            if type(self.data[k])==tuple:
                try:
                    self.filters.append((k,'=',int(self.data[k][0])))
                except:
                    self.filters.append((k,'ilike',"%"+self.data[k][0]+"%"))
            elif type(self.data[k]) in (str,unicode):
                #TODO: Pensar solucio generica fecha
                if k in 'fecha_inicio':
                    self.filters.append(('fecha_ficha','>=',self.data[k]))
                elif k in 'fecha_fin':
                    self.filters.append(('fecha_ficha','<=',self.data[k]))
                else:
                    self.filters.append((k,'ilike','%'+self.data[k]+'%'))
            elif type(self.data[k])==type(None):
                self.filters.append((k,'=',False))


class Pager(EventDispatcher):
    __stereotype__ = StringProperty('other')
    num_pag=NumericProperty(1)
    num_reg = NumericProperty()
    offset = NumericProperty(10)


    def next_page(self):
        if self.num_pag*self.offset <= self.num_reg or (self.num_pag*self.offset > self.num_reg and self.num_pag*self.offset-self.num_reg < self.offset):
            self.num_pag = self.num_pag+1
            self.controller.refresh_data()

    def previous_page(self):
        if self.num_pag > 1:
            self.num_pag = self.num_pag-1
            self.controller.refresh_data()

    def press_change_offset(self):       
        vals=[]
        val = 20
        while val <= 2000:
            vals.append({'name':str(val),'id':val})
            val = val+20
        options=[{'option_id':str(vals[i]['id']),'option':vals[i]['name']} for i in range(len(vals))]
        from utils.list_dialog_ctl import ListDialogCtl
        ListDialogCtl().choose_option(_('Seleccione número de filas:'),options,self.test_option,600,600,None,0)
        
    def test_option(self, option_id, option_text):
        if option_id:
            self.offset = int(option_id)
            self.controller.refresh_data()   
        
