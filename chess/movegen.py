#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import weakref

class MoveGeneratorSquare(object):
    def __init__(self,row,column):
        self.row_moves1=[]
        self.row_moves2=[]
        
        self.column_moves1=[]
        self.column_moves2=[]
        
        self.diag_moves1=[]
        self.diag_moves2=[]
        self.diag_moves3=[]
        self.diag_moves4=[]
        
        self.knights=[]
        
        self.pawn_advance1_white=None
        self.pawn_advance2_white=None
        
        self.pawn_advance1_black=None
        self.pawn_advance2_black=None
        
        self.pawn_captures_white_from=[]
        self.pawn_captures_white_from=[]
        
        self.kings=[]
        
        self.row=row
        self.column=column
        
    
class MoveGenerator(object):
    def __init__(self,pos):
        pos.generator=self
        self.pos=weakref.ref(pos)
        self.squares=[MoveGeneratorSquare(*self.pos().get_row_col(i)) for i in range(64)]
        for i in range(64):
            self.generate_column_moves(i)
            self.generate_row_moves(i)
            self.generate_diag_moves(i)
            
    def generate_column_moves(self,i):
        f,c = self.pos().get_row_col(i)
        f1=f+1
        while f1<=7:
            self.squares[i].column_moves1.append(self.squares[self.pos().get_index_row_col(f1,c)])
            f1+=1
        f2=f-1
        while f2>=0:
            self.squares[i].column_moves2.append(self.squares[self.pos().get_index_row_col(f2,c)])
            f2-=1

    def generate_row_moves(self,i):
        f,c = self.pos().get_row_col(i)
        c1=c+1
        while c1<=7:
            self.squares[i].row_moves1.append(self.squares[self.pos().get_index_row_col(f,c1)])
            c1+=1
        c2=c-1
        while c2>=0:
            self.squares[i].row_moves2.append(self.squares[self.pos().get_index_row_col(f,c2)])
            c2-=1

    def generate_diag_moves(self,i):
        f,c = self.pos().get_row_col(i)

        c1=c+1
        f1=f+1
        while c1<=7 and f1<=7:
            self.squares[i].diag_moves1.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1+=1
            f1+=1

        c1=c+1
        f1=f-1
        while c1<=7 and f1>=0:
            self.squares[i].diag_moves2.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1+=1
            f1-=1

        c1=c-1
        f1=f+1
        while c1>=0 and f1<=7:
            self.squares[i].diag_moves3.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1-=1
            f1+=1
        
        c1=c-1
        f1=f-1
        while c1>=0 and f1>=0:
            self.squares[i].diag_moves4.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1-=1
            f1-=1