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