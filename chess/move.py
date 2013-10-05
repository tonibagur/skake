#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from chess.piece_codes import *

class Move(object):
    
    def __init__(self,source_square,dest_square,piece_type,
                 last_color,next_color,
                 last_check,next_check,last_check_moves,next_check_moves,
                 last_fmr,next_fmr,
                 last_move_num,next_move_num,captured_piece=xx,
                 w_castle_ks_chg=False,w_castle_qs_chg=False,
                 b_castle_ks_chg=False,b_castle_qs_chg=False,
                 ep_sq_old=None,ep_sq_next=None):
        self.source_square=source_square
        self.dest_square=dest_square
        self.piece_type=piece_type
        self.last_color=last_color
        self.next_color=next_color
        self.captured_piece=captured_piece
        self.w_castle_ks_chg=w_castle_ks_chg
        self.w_castle_qs_chg=w_castle_qs_chg
        self.b_castle_ks_chg=b_castle_ks_chg
        self.b_castle_qs_chg=b_castle_qs_chg
        self.ep_sq_old=ep_sq_old
        self.ep_sq_next=ep_sq_next
        self.last_check=last_check
        self.next_check=next_check
        self.last_check_moves=last_check_moves
        self.next_check_moves=next_check_moves
        self.last_fmr=last_fmr
        self.next_fmr=next_fmr
        self.last_move_num=last_move_num
        self.next_move_num=next_move_num
        
    def do(self,board):
        board.set_square(self.source_square,xx)
        board.set_square(self.dest_square,self.piece_type)
        board.turn=self.next_color
        board.w_castle_qs=not self.w_castle_qs_chg and board.w_castle_qs
        board.w_castle_ks=not self.w_castle_ks_chg and board.w_castle_ks
        board.b_castle_qs=not self.b_castle_qs_chg and board.b_castle_qs
        board.b_castle_ks=not self.b_castle_ks_chg and board.b_castle_ks
        board.ep_sq=self.ep_sq_next
        board.check=self.next_check
        board.fmr=self.next_fmr
        board.move_num=self.next_move_num
        
    def undo(self,board):
        board.set_square(self.source_square,self.piece_type)
        board.set_square(self.dest_square,self.captured_piece)
        board.turn=self.last_color
        board.w_castle_qs=(not self.w_castle_qs_chg and board.w_castle_qs) or self.w_castle_qs_chg
        board.w_castle_ks=(not self.w_castle_ks_chg and board.w_castle_ks) or self.w_castle_ks_chg 
        board.b_castle_qs=(not self.b_castle_qs_chg and board.b_castle_qs) or self.b_castle_qs_chg
        board.b_castle_ks=(not self.b_castle_ks_chg and board.b_castle_ks) or self.b_castle_ks_chg
        board.ep_sq=self.ep_sq_old
        board.check=self.last_check
        board.fmr=self.last_fmr
        board.move_num=self.last_move_num