#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from chess.movegen import *

from chess.position import Position

import unittest

from chess.piece_codes import *

class TestMoveGenRook1(unittest.TestCase):
    def setUp(self):
        self.b=[xx,xx,xx,xx,xx,xx,bK,xx, #00..07
                xx,xx,xx,xx,xx,xx,xx,xx, #08..15
                xx,xx,xx,xx,xx,xx,xx,xx, #16..23
                xx,xx,xx,xx,xx,xx,xx,xx, #24..31
                xx,xx,xx,xx,xx,xx,xx,xx, #32..39
                xx,xx,xx,xx,xx,xx,xx,xx, #40..47
                xx,xx,xx,xx,xx,xx,xx,xx, #48..55
                xx,xx,xx,wR,xx,xx,wK,xx  #56..63
                ] 
        self.pos=Position(self.b,False,False,False,False,None,WHITE,0,0)
        self.mg=MoveGenerator(self.pos)
    
    def test_move_gen_rook1(self):
        moves=self.mg.generate_moves_rook(self.pos)
        self.assertEqual(set([59]),set([x.source_square for x in moves]))
        self.assertEqual(set([56,57,58,60,61,51,43,35,27,19,11,3]),set([x.dest_square for x in moves]))
        self.assertEqual(len(moves),12)

class TestMoveGenRook2(unittest.TestCase):
    def setUp(self):
        self.b=[xx,xx,xx,xx,xx,bK,bR,xx, #00..07
                xx,xx,xx,xx,xx,xx,xx,xx, #08..15
                xx,xx,xx,xx,xx,xx,xx,xx, #16..23
                xx,xx,xx,xx,xx,xx,xx,xx, #24..31
                xx,xx,xx,xx,xx,xx,xx,xx, #32..39
                xx,xx,xx,xx,xx,xx,xx,xx, #40..47
                xx,xx,xx,xx,xx,xx,wR,xx, #48..55
                xx,xx,xx,xx,xx,xx,wK,xx  #56..63
                ] 
        self.pos=Position(self.b,False,False,False,False,None,WHITE,0,0)
        self.mg=MoveGenerator(self.pos)
    
    def test_move_gen_rook2(self):
        moves=self.mg.generate_moves_rook(self.pos)
        self.assertEqual(len(moves),6)
        
class TestMoveGenRook3(unittest.TestCase):
    def setUp(self):
        self.b=[xx,xx,xx,xx,xx,bK,xx,xx, #00..07
                xx,xx,xx,xx,xx,xx,xx,xx, #08..15
                xx,xx,xx,xx,xx,xx,xx,xx, #16..23
                xx,xx,bB,xx,xx,xx,xx,xx, #24..31
                xx,xx,xx,xx,xx,xx,xx,xx, #32..39
                xx,xx,xx,xx,xx,xx,xx,xx, #40..47
                xx,xx,xx,xx,xx,wR,xx,xx, #48..55
                xx,xx,xx,xx,xx,xx,wK,xx  #56..63
                ] 
        self.pos=Position(self.b,False,False,False,False,None,WHITE,0,0)
        self.mg=MoveGenerator(self.pos)
    
    def test_move_gen_rook2(self):
        moves=self.mg.generate_moves_rook(self.pos)
        self.assertEqual(len(moves),0)


class TestMoveGenBoard(unittest.TestCase):
    def setUp(self):
        self.pos=Position()
        self.movegen=MoveGeneratorBoard(self.pos)
        
    def test_move_column(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                self.assertEqual(len(mgsq.column_moves1),7-i)
                self.assertEqual(len(mgsq.column_moves2),i)
                self.assertEqual(mgsq.row,i)
                self.assertEqual(mgsq.column,j)
                q=i+1
                for m in mgsq.column_moves1:
                    self.assertEqual(m.column,mgsq.column)
                    self.assertEqual(m.row,q)
                    q+=1
                q=i-1
                for m in mgsq.column_moves2:
                    self.assertEqual(m.column,mgsq.column)
                    self.assertEqual(m.row,q)
                    q-=1
        
    def test_move_row(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                self.assertEqual(len(mgsq.row_moves1),7-j)
                self.assertEqual(len(mgsq.row_moves2),j)
                self.assertEqual(mgsq.row,i)
                self.assertEqual(mgsq.column,j)
                q=j+1
                for m in mgsq.row_moves1:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,mgsq.row)
                    q+=1
                q=j-1
                for m in mgsq.row_moves2:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,mgsq.row)
                    q-=1
                    
    def test_move_diag(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                self.assertEqual(len(mgsq.diag_moves1),min(7-i,7-j))
                self.assertEqual(len(mgsq.diag_moves2),min(i,7-j))
                self.assertEqual(len(mgsq.diag_moves3),min(7-i,j))
                self.assertEqual(len(mgsq.diag_moves4),min(i,j))
                self.assertEqual(mgsq.row,i)
                self.assertEqual(mgsq.column,j)
                r=i+1
                q=j+1
                for m in mgsq.diag_moves1:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,r)
                    r+=1
                    q+=1
                r=i-1
                q=j+1
                for m in mgsq.diag_moves2:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,r)
                    r-=1
                    q+=1
                r=i+1
                q=j-1
                for m in mgsq.diag_moves3:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,r)
                    r+=1
                    q-=1
                r=i-1
                q=j-1
                for m in mgsq.diag_moves4:
                    self.assertEqual(m.column,q)
                    self.assertEqual(m.row,r)
                    r-=1
                    q-=1
                    
                    
    def test_move_knights(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                candidates=[x for x in self.movegen.knight_deltas if 0<=(i+x[0])<=7 and 0<=(j+x[1])<=7]
                self.assertEqual(len(mgsq.knight_moves),len(candidates))
                self.assertEqual(mgsq.row,i)
                self.assertEqual(mgsq.column,j)
                for q,s in enumerate(mgsq.knight_moves):
                    self.assertEqual(s.row,i+candidates[q][0])
                    self.assertEqual(s.column,j+candidates[q][1])

    def test_move_king(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                candidates=[x for x in self.movegen.king_deltas if 0<=(i+x[0])<=7 and 0<=(j+x[1])<=7]
                self.assertEqual(len(mgsq.king_moves),len(candidates))
                self.assertEqual(mgsq.row,i)
                self.assertEqual(mgsq.column,j)
                for q,s in enumerate(mgsq.king_moves):
                    self.assertEqual(s.row,i+candidates[q][0])
                    self.assertEqual(s.column,j+candidates[q][1])

                    
    def test_pawn_advances(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                if i!=2:
                    self.assertLess(len(mgsq.pawn_advance_white),2)
                else:
                    self.assertEqual(mgsq.pawn_advance_white[1].row,i+2)
                    self.assertEqual(mgsq.pawn_advance_white[1].column,j)
                if i!=7:
                    self.assertLess(len(mgsq.pawn_advance_black),2)
                else:
                    self.assertEqual(mgsq.pawn_advance_black[1].row,i-2)
                    self.assertEqual(mgsq.pawn_advance_black[1].column,j)
                if i==7:
                    self.assertEqual(len(mgsq.pawn_advance_white),0)
                else:
                    self.assertEqual(mgsq.pawn_advance_white[0].row,i+1)
                    self.assertEqual(mgsq.pawn_advance_white[0].column,j)
                if i==0:
                    self.assertEqual(len(mgsq.pawn_advance_black),0)
                else:
                    self.assertEqual(mgsq.pawn_advance_black[0].row,i-1)
                    self.assertEqual(mgsq.pawn_advance_black[0].column,j)
                    
    def test_pawn_captures(self):
        for i in range(8):
            for j in range(8):
                mgsq=self.movegen.squares[self.pos.get_index_row_col(i,j)]
                if i == 0:
                    self.assertEqual(len(mgsq.pawn_captures_black),0)
                    if j==0:
                        self.assertEqual(len(mgsq.pawn_captures_white),1)
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            self.assertEqual(q.column,j+1)
                    elif j<7:
                        self.assertEqual(len(mgsq.pawn_captures_white),2)
                        s=set()
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            s.add(q.column)
                        self.assertEqual(s,set([j+1,j-1]))
                    else:
                        self.assertEqual(len(mgsq.pawn_captures_white),1)
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            self.assertEqual(q.column,j-1)
                elif i < 7:
                    if j==0:
                        self.assertEqual(len(mgsq.pawn_captures_black),1)
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            self.assertEqual(q.column,j+1)
                        self.assertEqual(len(mgsq.pawn_captures_white),1)
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            self.assertEqual(q.column,j+1)
                    elif j<7:
                        self.assertEqual(len(mgsq.pawn_captures_black),2)
                        s=set()
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            s.add(q.column)
                        self.assertEqual(s,set([j+1,j-1]))
                        self.assertEqual(len(mgsq.pawn_captures_white),2)
                        s=set()
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            s.add(q.column)
                        self.assertEqual(s,set([j+1,j-1]))
                    else:
                        self.assertEqual(len(mgsq.pawn_captures_black),1)
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            self.assertEqual(q.column,j-1)
                        self.assertEqual(len(mgsq.pawn_captures_white),1)
                        for q in mgsq.pawn_captures_white:
                            self.assertEqual(q.row,i+1)
                            self.assertEqual(q.column,j-1)
                else:
                    self.assertEqual(len(mgsq.pawn_captures_white),0)
                    if j==0:
                        self.assertEqual(len(mgsq.pawn_captures_black),1)
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            self.assertEqual(q.column,j+1)
                    elif j<7:
                        self.assertEqual(len(mgsq.pawn_captures_black),2)
                        s=set()
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            s.add(q.column)
                        self.assertEqual(s,set([j+1,j-1]))
                    else:
                        self.assertEqual(len(mgsq.pawn_captures_black),1)
                        for q in mgsq.pawn_captures_black:
                            self.assertEqual(q.row,i-1)
                            self.assertEqual(q.column,j-1)
    
    def test_move_sets(self):
        move_types=['column_moves1',
                    'column_moves2',
                    'row_moves1',
                    'row_moves2',
                    'diag_moves1',
                    'diag_moves2',
                    'diag_moves3',
                    'diag_moves4',
                    'knight_moves',
                    'king_moves',
                    'pawn_advance_white',
                    'pawn_advance_black',
                    'pawn_captures_white',
                    'pawn_captures_black',
                    ]
        for i in range(63):
            sq=self.movegen.squares[i]
            for t in move_types:
                self.assertEqual(set(getattr(sq,t)),getattr(sq,'set_'+t))