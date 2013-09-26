from chess.movegen import *

from chess.position import Position

import unittest

class TestMoveGen(unittest.TestCase):
    def setUp(self):
        self.pos=Position()
        self.movegen=MoveGenerator(self.pos)
        
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