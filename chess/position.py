#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chess.piece_codes import *

class Position(object):
    b=[bR,bN,bB,bQ,bK,bB,bN,bR,
       bP,bP,bP,bP,bP,bP,bP,bP,
       xx,xx,xx,xx,xx,xx,xx,xx,
       xx,xx,xx,xx,xx,xx,xx,xx,
       xx,xx,xx,xx,xx,xx,xx,xx,
       xx,xx,xx,xx,xx,xx,xx,xx,
       wP,wP,wP,wP,wP,wP,wP,wP,
       wR,wN,wB,wQ,wK,wB,wN,wR
    ]
    w_castle_qs=True
    w_castle_ks=True
    b_castle_qs=True
    b_castle_ks=True
    ep_sq=None
    turn=WHITE
    check=False
    
    def set_square(self,square,value):
        assert (0 <= square < 64) and (value in ALL_PIECE_CODES)
        self.b[square]=value
        
    def get_square(self,square):
        assert (0 <= square < 64)
        return self.b[square]
        
    def get_row_col(self,square):
        assert (0 <= square < 64)
        row=7-square/8
        col=square%8
        return row,col
        
    def get_row_col_value(self,row,col):
        assert (0 <= row < 8) and (0 <= col < 8)
        row2=7-row
        return self.b[row2*8+col]
    
    def set_row_col_value(self,row,col,value):
        assert (0 <= row < 8) and (0 <= col < 8) and (value in ALL_PIECE_CODES) 
        row2=7-row
        self.b[row2*8+col]=value
    
    def __iter__(self):
        for x in self.b:
            yield x

    