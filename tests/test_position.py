import unittest

from chess.position import Position
from chess.piece_codes import *
from exceptions import AssertionError


'''Class to use(replacing unittest.TestCase) if we want to run a test_case inside our debugger framework'''
class dummyTest(object):
    def assertEqual(self,a,b):
        if a!=b:
            print a,"!=",b

class Test_Position_PosInicial(unittest.TestCase):
#class Test_Position_PosInicial(dummyTest): 
    def setUp(self):
        self.pos=Position()
        self.b=[bR,bN,bB,bQ,bK,bB,bN,bR,
                bP,bP,bP,bP,bP,bP,bP,bP,
                xx,xx,xx,xx,xx,xx,xx,xx,
                xx,xx,xx,xx,xx,xx,xx,xx,
                xx,xx,xx,xx,xx,xx,xx,xx,
                xx,xx,xx,xx,xx,xx,xx,xx,
                wP,wP,wP,wP,wP,wP,wP,wP,
                wR,wN,wB,wQ,wK,wB,wN,wR
               ]        
    def test_initial_values(self):

        for i,p in enumerate(self.pos):
            self.assertEqual(p,self.b[i])
        self.assertEqual(self.pos.w_castle_qs,True)
        self.assertEqual(self.pos.w_castle_ks,True)
        self.assertEqual(self.pos.b_castle_qs,True)
        self.assertEqual(self.pos.b_castle_ks,True)
        self.assertEqual(self.pos.ep_sq,None)
        self.assertEqual(self.pos.turn,WHITE)
        self.assertEqual(self.pos.check,False)
        self.assertEqual(self.pos.pieces[xx],set(range(16,48)))
        
    def test_set_get_squares_out_of_range(self):
        self.assertRaises(AssertionError,self.pos.set_square,-1,wB)
        self.assertRaises(AssertionError,self.pos.set_square,64,wB)
        self.assertRaises(AssertionError,self.pos.set_square,0,-1)
        self.assertRaises(AssertionError,self.pos.set_square,0,1000)
        self.assertRaises(AssertionError,self.pos.get_square,-1)
        self.assertRaises(AssertionError,self.pos.get_square,64)
        
    def test_set_get_square(self):
        self.assertEqual(self.pos.get_square(48),wP)
        self.pos.set_square(48,xx)
        self.pos.set_square(40,wP)
        self.assertEqual(self.pos.get_square(48),xx)
        self.assertEqual(self.pos.get_square(40),wP)
        self.assertEqual(self.pos.get_square(8),bP)
        self.pos.set_square(8,xx)
        self.pos.set_square(16,wP)
        self.assertEqual(self.pos.get_square(8),xx)
        self.assertEqual(self.pos.get_square(16),wP)  
        self.assertEqual(self.pos.get_square(63),wR)
        self.pos.set_square(63,xx)
        self.assertEqual(self.pos.get_square(63),xx)
              
    def test_get_row_col_out_of_range(self):
        self.assertRaises(AssertionError,self.pos.get_row_col,-1)
        self.assertRaises(AssertionError,self.pos.get_row_col,-2)
        self.assertRaises(AssertionError,self.pos.get_row_col,64)
        self.assertRaises(AssertionError,self.pos.get_row_col,65)
        
    def test_get_row_col(self):
        f,c = self.pos.get_row_col(0)
        self.assertEqual(f,7)
        self.assertEqual(c,0)
        f,c = self.pos.get_row_col(3)
        self.assertEqual(f,7)
        self.assertEqual(c,3)        
        f,c = self.pos.get_row_col(56)
        self.assertEqual(f,0)
        self.assertEqual(c,0)    
        f,c = self.pos.get_row_col(63)
        self.assertEqual(f,0)
        self.assertEqual(c,7)  
        f,c = self.pos.get_row_col(50)
        self.assertEqual(f,1)
        self.assertEqual(c,2) 
        
    def test_get_row_col_value_out_of_range(self):
        self.assertRaises(AssertionError,self.pos.get_row_col_value,-2,0)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,-1,0)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,0,-1)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,0,-2)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,8,0)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,9,0)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,0,8)
        self.assertRaises(AssertionError,self.pos.get_row_col_value,0,9)
        
    def test_get_row_col_value(self):
        self.assertEqual(self.pos.get_row_col_value(0,0),wR)
        self.assertEqual(self.pos.get_row_col_value(0,1),wN)
        self.assertEqual(self.pos.get_row_col_value(0,2),wB)
        self.assertEqual(self.pos.get_row_col_value(0,3),wQ)
        self.assertEqual(self.pos.get_row_col_value(0,4),wK)
        self.assertEqual(self.pos.get_row_col_value(0,7),wR)
        self.assertEqual(self.pos.get_row_col_value(0,6),wN)
        self.assertEqual(self.pos.get_row_col_value(0,5),wB)
        self.assertEqual(self.pos.get_row_col_value(1,0),wP)
        self.assertEqual(self.pos.get_row_col_value(1,1),wP)
        self.assertEqual(self.pos.get_row_col_value(1,2),wP)
        self.assertEqual(self.pos.get_row_col_value(1,3),wP)
        self.assertEqual(self.pos.get_row_col_value(1,4),wP)
        self.assertEqual(self.pos.get_row_col_value(1,7),wP)
        self.assertEqual(self.pos.get_row_col_value(1,6),wP)
        self.assertEqual(self.pos.get_row_col_value(1,5),wP)
        self.assertEqual(self.pos.get_row_col_value(7,0),bR)
        self.assertEqual(self.pos.get_row_col_value(7,1),bN)
        self.assertEqual(self.pos.get_row_col_value(7,2),bB)
        self.assertEqual(self.pos.get_row_col_value(7,3),bQ)
        self.assertEqual(self.pos.get_row_col_value(7,4),bK)
        self.assertEqual(self.pos.get_row_col_value(7,7),bR)
        self.assertEqual(self.pos.get_row_col_value(7,6),bN)
        self.assertEqual(self.pos.get_row_col_value(7,5),bB)
        self.assertEqual(self.pos.get_row_col_value(6,0),bP)
        self.assertEqual(self.pos.get_row_col_value(6,1),bP)
        self.assertEqual(self.pos.get_row_col_value(6,2),bP)
        self.assertEqual(self.pos.get_row_col_value(6,3),bP)
        self.assertEqual(self.pos.get_row_col_value(6,4),bP)
        self.assertEqual(self.pos.get_row_col_value(6,7),bP)
        self.assertEqual(self.pos.get_row_col_value(6,6),bP)
        self.assertEqual(self.pos.get_row_col_value(6,5),bP)
        for i in range(2,6):
            for j in range(2,6):
                self.assertEqual(self.pos.get_row_col_value(i,j),xx) 
        
    def test_set_row_col_value_out_of_range(self):
        self.assertRaises(AssertionError,self.pos.set_row_col_value,-2,0,xx)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,-1,0,wB)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,-1,bB)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,-2,wK)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,8,0,bK)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,9,0,wQ)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,8,bQ)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,9,bP)
        
        self.assertRaises(AssertionError,self.pos.set_row_col_value,7,0,-4)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,7,7,-1)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,7,-2)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,5,6,-3)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,7,0,0)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,7,0,14)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,7,-1)
        self.assertRaises(AssertionError,self.pos.set_row_col_value,0,7,14)
        
    def test_set_row_col_value(self):
        self.pos.set_row_col_value(0,0,xx)
        self.assertEqual(self.pos.get_row_col_value(0,0),xx)
        self.assertEqual(self.pos.get_square(56),xx)
        
        self.pos.set_row_col_value(0,7,wK)
        self.assertEqual(self.pos.get_row_col_value(0,7),wK)
        self.assertEqual(self.pos.get_square(63),wK)
        
        self.pos.set_row_col_value(1,7,wQ)
        self.assertEqual(self.pos.get_row_col_value(1,7),wQ)
        self.assertEqual(self.pos.get_square(55),wQ)
        
        self.pos.set_row_col_value(1,3,wB)
        self.assertEqual(self.pos.get_row_col_value(1,3),wB)
        self.assertEqual(self.pos.get_square(51),wB)
        
        self.pos.set_row_col_value(7,7,xx)
        self.assertEqual(self.pos.get_row_col_value(7,7),xx)
        self.assertEqual(self.pos.get_square(7),xx)
        
        self.pos.set_row_col_value(6,7,bK)
        self.assertEqual(self.pos.get_row_col_value(6,7),bK)
        self.assertEqual(self.pos.get_square(15),bK)
        
        self.pos.set_row_col_value(6,0,bQ)
        self.assertEqual(self.pos.get_row_col_value(6,0),bQ)
        self.assertEqual(self.pos.get_square(8),bQ)
        
        self.pos.set_row_col_value(6,3,bB)
        self.assertEqual(self.pos.get_row_col_value(6,3),bB)
        self.assertEqual(self.pos.get_square(11),bB)
            
    def test_get_index_row_col(self):
        self.assertRaises(AssertionError,self.pos.get_index_row_col,-1,0)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,0,-1)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,-2,0)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,0,-2)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,8,0)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,0,8)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,9,0)
        self.assertRaises(AssertionError,self.pos.get_index_row_col,0,9)
        self.assertEqual(self.pos.get_index_row_col(7,0),0)
        self.assertEqual(self.pos.get_index_row_col(7,7),7)
        self.assertEqual(self.pos.get_index_row_col(0,0),56)
        self.assertEqual(self.pos.get_index_row_col(0,7),63)
        self.assertEqual(self.pos.get_index_row_col(5,0),16)
        
