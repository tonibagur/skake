#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import weakref


class MoveGenerator(object):
    
    def generate_moves(self,board):
        pass
    

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
        
        self.knight_moves=[]
        
        self.pawn_advance_white=[]
        
        self.pawn_advance_black=[]
        
        #TODO: potser faltaria una referencia especial a setena i segona files per poder calcular
        #rapidament les promocions que no venen de captura
        
        self.pawn_captures_white=[]
        self.pawn_captures_black=[]
        
        self.king_moves=[]
        
        self.row=row
        self.column=column
        
    
class MoveGeneratorBoard(object):
    knight_deltas=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
    king_deltas=[(1,0),(1,1),(0,1),(-1,0),(-1,1),(0,-1),(1,-1),(-1,-1)]
    def __init__(self,pos):
        pos.generator=self
        self.pos=weakref.ref(pos)
        self.squares=[MoveGeneratorSquare(*self.pos().get_row_col(i)) for i in range(64)]
        for i in range(64):
            self.generate_column_moves(i)
            self.generate_row_moves(i)
            self.generate_diag_moves(i)
            self.generate_knight_moves(i)
            self.generate_pawn_advances(i)
            self.generate_pawn_captures(i)
            self.generate_king_moves(i)
            
    def generate_column_moves(self,i):
        f,c = self.pos().get_row_col(i)
        f1=f+1
        while f1<=7:
            self.squares[i].column_moves1.append(self.squares[self.pos().get_index_row_col(f1,c)])
            f1+=1
        self.squares[i].set_column_moves1=set(self.squares[i].column_moves1)
        f2=f-1
        while f2>=0:
            self.squares[i].column_moves2.append(self.squares[self.pos().get_index_row_col(f2,c)])
            f2-=1
        self.squares[i].set_column_moves2=set(self.squares[i].column_moves2)

    def generate_row_moves(self,i):
        f,c = self.pos().get_row_col(i)
        c1=c+1
        while c1<=7:
            self.squares[i].row_moves1.append(self.squares[self.pos().get_index_row_col(f,c1)])
            c1+=1
        self.squares[i].set_row_moves1=set(self.squares[i].row_moves1)
        c2=c-1
        while c2>=0:
            self.squares[i].row_moves2.append(self.squares[self.pos().get_index_row_col(f,c2)])
            c2-=1
        self.squares[i].set_row_moves2=set(self.squares[i].row_moves2)

    def generate_diag_moves(self,i):
        f,c = self.pos().get_row_col(i)

        c1=c+1
        f1=f+1
        while c1<=7 and f1<=7:
            self.squares[i].diag_moves1.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1+=1
            f1+=1
        self.squares[i].set_diag_moves1=set(self.squares[i].diag_moves1)
        c1=c+1
        f1=f-1
        while c1<=7 and f1>=0:
            self.squares[i].diag_moves2.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1+=1
            f1-=1
        self.squares[i].set_diag_moves2=set(self.squares[i].diag_moves2)
        c1=c-1
        f1=f+1
        while c1>=0 and f1<=7:
            self.squares[i].diag_moves3.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1-=1
            f1+=1
        self.squares[i].set_diag_moves3=set(self.squares[i].diag_moves3)
        c1=c-1
        f1=f-1
        while c1>=0 and f1>=0:
            self.squares[i].diag_moves4.append(self.squares[self.pos().get_index_row_col(f1,c1)])
            c1-=1
            f1-=1
        self.squares[i].set_diag_moves4=set(self.squares[i].diag_moves4)
    def generate_knight_moves(self,i):
        f,c = self.pos().get_row_col(i)
        
        for d in self.knight_deltas:
            f2=f+d[0]
            c2=c+d[1]
            if 0<=f2<=7 and 0<=c2<=7:
                self.squares[i].knight_moves.append(self.squares[self.pos().get_index_row_col(f2,c2)])
            self.squares[i].set_knight_moves=set(self.squares[i].knight_moves)
                
    def generate_king_moves(self,i):
        f,c = self.pos().get_row_col(i)
        
        for d in self.king_deltas:
            f2=f+d[0]
            c2=c+d[1]
            if 0<=f2<=7 and 0<=c2<=7:
                self.squares[i].king_moves.append(self.squares[self.pos().get_index_row_col(f2,c2)])
        self.squares[i].set_king_moves=set(self.squares[i].king_moves)

    def generate_pawn_advances(self,i):
        f,c = self.pos().get_row_col(i)
        if f<7:
            self.squares[i].pawn_advance_white.append(self.squares[self.pos().get_index_row_col(f+1,c)])
        if f==2:
            self.squares[i].pawn_advance_white.append(self.squares[self.pos().get_index_row_col(f+2,c)])
        self.squares[i].set_pawn_advance_white=set(self.squares[i].pawn_advance_white)
        if f>0:    
            self.squares[i].pawn_advance_black.append(self.squares[self.pos().get_index_row_col(f-1,c)])
        if f==7:
            self.squares[i].pawn_advance_black.append(self.squares[self.pos().get_index_row_col(f-2,c)])
        self.squares[i].set_pawn_advance_black=set(self.squares[i].pawn_advance_black)
    
    def generate_pawn_captures(self,i):
        f,c = self.pos().get_row_col(i) 
        
        f1=f+1
        c1=c-1
        if 0<=f1<=7 and 0<=c1<=7:
            self.squares[i].pawn_captures_white.append(self.squares[self.pos().get_index_row_col(f1,c1)])        
        f1=f+1
        c1=c+1
        if 0<=f1<=7 and 0<=c1<=7:
            self.squares[i].pawn_captures_white.append(self.squares[self.pos().get_index_row_col(f1,c1)])
        self.squares[i].set_pawn_captures_white=set(self.squares[i].pawn_captures_white)
        f1=f-1
        c1=c-1
        if 0<=f1<=7 and 0<=c1<=7:
            self.squares[i].pawn_captures_black.append(self.squares[self.pos().get_index_row_col(f1,c1)])        
        f1=f-1
        c1=c+1
        if 0<=f1<=7 and 0<=c1<=7:
            self.squares[i].pawn_captures_black.append(self.squares[self.pos().get_index_row_col(f1,c1)])   
        self.squares[i].set_pawn_captures_black=set(self.squares[i].pawn_captures_black)