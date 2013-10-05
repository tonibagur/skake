#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chess.piece_codes import *

class Position(object):
    
    def __init__(self,board_vals=None,w_castle_qs=True,w_castle_ks=True,
                 b_castle_qs=True,b_castle_ks=True,ep_sq=None,
                 turn=WHITE,check=False,fmr=0,move_num=0):
        if not board_vals:
            self.b=[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                    bP,bP,bP,bP,bP,bP,bP,bP,#08..15
                    xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                    xx,xx,xx,xx,xx,xx,xx,xx,#24..31
                    xx,xx,xx,xx,xx,xx,xx,xx,#32..39
                    xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                    wP,wP,wP,wP,wP,wP,wP,wP,#48..55
                    wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                    ]
        else:
            self.b=board_vals
        self.w_castle_qs=w_castle_qs
        self.w_castle_ks=w_castle_ks
        self.b_castle_qs=b_castle_qs
        self.b_castle_ks=b_castle_ks
        self.ep_sq=ep_sq
        self.turn=turn
        self.check=check
        self.fmr=fmr
        self.move_num=move_num
        
        self.pieces={
            xx:set(),
            WHITE:set(),
            BLACK:set(),
            bR:set(),
            bN:set(),
            bB:set(),
            bQ:set(),
            bK:set(),
            bP:set(),
            wR:set(),
            wN:set(),
            wB:set(),
            wQ:set(),
            wK:set(),
            wP:set(),
        }
        
        self._init_pieces()
        
    def _init_pieces(self):
        for i,v in enumerate(self.b):
            self.pieces[color(v)].add(i)
            self.pieces[v].add(i)
    
    def set_square(self,square,value):
        assert (0 <= square < 64) and (value in ALL_PIECE_CODES)
        old_val=self.b[square]
        self.pieces[old_val].remove(square)
        if old_val!=xx:
            self.pieces[color(old_val)].remove(square)
        self.b[square]=value
        self.pieces[color(value)].add(square)
        self.pieces[value].add(square)
        
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
        
    def get_index_row_col(self,row,col):
        assert (0 <= row < 8) and (0 <= col < 8)
        row2=7-row
        return row2*8+col
    
    def __iter__(self):
        for x in self.b:
            yield x

    