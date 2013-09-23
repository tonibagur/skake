#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class MoveGeneratorSquare(object):
    columns_from=[]
    columns_through=[]
    columns_to=[]   
    
    rows_from=[]  
    rows_through=[]
    rows_to=[]
    
    #TODO: is it interesting to separe diags in two types?
    diags_from=[] 
    diags_through=[]
    diags_to=[]
    
    knights_from=[]        
    knights_to=[]
    
    pawns_advance_from=[]
    pawns_advance_to=[]
    
    pawns_capture_from=[]
    pawns_capture_to=[]
    
    kings_from=[]
    kings_to=[]
    
class MoveGenerator(object):
    squares=[MoveGeneratorSquare() for i in range(64)]
    
class Ray(object):
    def __init__(self,source,target,ray_type):
        self.target=target
        self.source=source
        self.num_walls_white=0
        self.num_walls_black=0
        self.ray_type=ray_type