#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import unittest

from chess.move import Move
from chess.position import Position
from chess.piece_codes import *


class TestMove(unittest.TestCase):
    def setUp(self):
        self.pos=Position()
        
    def test_move(self):
        #51 -> 35 = d2 -> d4
        m1=Move(51,35,wP,WHITE,BLACK,False,False,0,0,0,1,xx,False,False,False,False,None,43)
        m1.do(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,bP,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,xx,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,43)
        self.assertEqual(self.pos.turn,BLACK)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,0)
        self.assertEqual(self.pos.move_num,1)
        
        m2=Move(11,27,bP,BLACK,WHITE,False,False,0,0,1,1,xx,False,False,False,False,43,18)
        m2.do(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,18)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,0)
        self.assertEqual(self.pos.move_num,1)
        
        m3=Move(59,43,wQ,WHITE,BLACK,False,False,0,1,1,2,xx,False,False,False,False,18,None)
        m3.do(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,wQ,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,xx,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,BLACK)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,1)
        self.assertEqual(self.pos.move_num,2)
        
        m4=Move(3,19,bQ,BLACK,WHITE,False,False,1,2,2,2,xx,False,False,False,False,None,None)
        m4.do(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,xx,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,bQ,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,wQ,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,xx,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,2)
        self.assertEqual(self.pos.move_num,2)
        
        m5=Move(60,59,wK,WHITE,BLACK,False,False,2,3,2,3,xx,True,True,True,True,None,None)
        m5.do(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,xx,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,bQ,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,wQ,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wK,xx,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,False)
        self.assertEqual(self.pos.w_castle_ks,False)
        self.assertEqual(self.pos.b_castle_qs,False)
        self.assertEqual(self.pos.b_castle_ks,False)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,BLACK)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,3)
        self.assertEqual(self.pos.move_num,3)
        
        m5.undo(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,xx,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,bQ,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,wQ,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,xx,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,2)
        self.assertEqual(self.pos.move_num,2)
        
        m4.undo(self.pos)  
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,wQ,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,xx,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,BLACK)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,1)
        self.assertEqual(self.pos.move_num,2)      
        
        m3.undo(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,xx,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,bP,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,18)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,0)
        self.assertEqual(self.pos.move_num,1)
        
        m2.undo(self.pos)
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,bP,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,xx,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,wP,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,xx,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,43)
        self.assertEqual(self.pos.turn,BLACK)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,0)
        self.assertEqual(self.pos.move_num,1)
        
        m1.undo(self.pos)  
        self.assertEqual(self.pos.b,[bR,bN,bB,bQ,bK,bB,bN,bR,#00..08
                                     bP,bP,bP,bP,bP,bP,bP,bP,#08..15
                                     xx,xx,xx,xx,xx,xx,xx,xx,#16..23
                                     xx,xx,xx,xx,xx,xx,xx,xx,#24..31
                                     xx,xx,xx,xx,xx,xx,xx,xx,#32..39
                                     xx,xx,xx,xx,xx,xx,xx,xx,#40..47
                                     wP,wP,wP,wP,wP,wP,wP,wP,#48..55
                                     wR,wN,wB,wQ,wK,wB,wN,wR #56..63
                                    ])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.fmr,0)
        self.assertEqual(self.pos.move_num,0)