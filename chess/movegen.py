#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class MoveGeneratorSquare(object):
    rays_from=[]
    rays_through=[]
    rays_to=[]            

class MoveGenerator(object):
    squares=[MoveGeneratorSquare() for i in range(64)]
    
class Ray(object):
    def __init__(self,source,target,ray_type):
        self.target=target
        self.source=source
        self.num_walls=0
        self.ray_type=ray_type