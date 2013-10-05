#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import weakref

from chess.move import Move


class MoveGenerator(object):
    
    def __init__(self):
        self.helper=MoveGeneratorBoard()
    
    def generate_moves(self,board):
        moves=[]
        if board.check:
            raise Exception('Not implemented')
        else:
            moves+=self.generate_rook_moves(board)
        return moves

    def generate_moves_rook(self,board):
        piece='wR' if board.turn=='WHITE' else 'bR'
        rooks=board.pieces[piece]
        moves=[]
        for s in rooks:
            moves+=self.generate_moves_rook_sq(board,s)
        return moves

    
    def generate_moves_rook_sq(self,board,s):
        moves=[]
        next_turn=oposite(board.turn)
        if not self.pinned_diag(board,s) and not self.pinned_row(board,s):
            for dest in self.helper[s].row_moves1:
                dest_val=board.squares[dest]
                dest_color=color(dest_val)
                if board.turn==dest_color:
                    break
                if next_turn==dest_color:
                    m=self.build_move()
        return moves
                  
    
    def build_move(self,board,source_square,dest_square,piece_type,
                   check,fmr_reset,captured_piece,ep=None):
        w_castle_ks_chg=False
        w_castle_qs_chg=False      
        b_castle_ks_chg=False
        b_castle_qs_chg=False  
        if piece_type=='wK':
            if board.w_castle_ks:
                w_castle_ks_chg=True
            if board.w_castle_qs:
                w_castle_qs_chg=True
        if piece_type=='bK':
            if board.b_castle_ks:
                b_castle_ks_chg=True
            if board.b_castle_qs:
                b_castle_qs_chg=True
        '''Note: This part of the implementation is not CHESS960 friendly'''
        if piece_type=='wR':
            if board.w_castle_ks and source_square==63:
                w_castle_ks_chg=True
            if board.w_castle_qs and source_square==56:
                w_castle_qs_chg=True
        if piece_type=='bR':
            if board.b_castle_ks and source_square==7:
                b_castle_ks_chg=True
            if board.b_castle_qs and source_square==0:
                b_castle_qs_chg=True
        '''End of note'''
        return Move(source_square,dest_square,piece_type,oposite(board.turn),
                    board.check,check,board.fmr,0 if fmr_reset else board.fmr+1,
                    board.move_num,board.move_num if board.turn=='BLACK' else board.move_num+1,
                    captured_piece,w_castle_ks_chg,w_castle_qs_chg,
                    b_castle_ks_chg,b_castle_qs_chg,board.ep_sq,ep)
                    
                    

class MoveGeneratorSquare(object):
    
    def __init__(self,row,column,square):
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
        self.square=square
        
    
class MoveGeneratorBoard(object):
    knight_deltas=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
    king_deltas=[(1,0),(1,1),(0,1),(-1,0),(-1,1),(0,-1),(1,-1),(-1,-1)]
    def __init__(self,pos):
        pos.generator=self
        self.pos=weakref.ref(pos)
        self.squares=[MoveGeneratorSquare(*self.pos().get_row_col2(i)) for i in range(64)]
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