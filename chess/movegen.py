#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import weakref

from chess.move import Move

from chess.piece_codes import *


class MoveGenerator(object):
    
    def __init__(self,pos):
        self.helper=MoveGeneratorBoard(pos)
    
    def generate_moves(self,board):
        moves=[]
        if board.check:
            raise Exception('Not implemented')
        else:
            moves+=self.generate_rook_moves(board)
        return moves

    def generate_moves_rook(self,board):
        piece=wR if board.turn == WHITE else bR
        rooks=board.pieces[piece]
        moves=[]
        for s in rooks:
            moves+=self.generate_moves_rook_sq(board,piece,s)
        return moves

    
    def generate_moves_rook_sq(self,board,piece_type,s,only_captures=False):
        moves=[]
        if not self.pinned_diag(board,s) and not self.pinned_row(board,s):
            moves+=self.generate_moves_ray(board,piece_type,s,
                                           self.helper.squares[s].column_moves1,only_captures)
            moves+=self.generate_moves_ray(board,piece_type,s,
                                           self.helper.squares[s].column_moves2,only_captures)
        if not self.pinned_diag(board,s) and not self.pinned_column(board,s):
            moves+=self.generate_moves_ray(board,piece_type,s,
                                           self.helper.squares[s].row_moves1,only_captures)
            moves+=self.generate_moves_ray(board,piece_type,s,
                                           self.helper.squares[s].row_moves2,only_captures)
        return moves
        
    def discovered_check(self,board,square):
        pass
    
    def pinned_diag(self,board,square):
        return self.pinned_diag_1_4(board,square) or self.pinned_diag_2_3(board,square)

    def pinned_diag_1_4(self,board,square):
        return self.pinned_ray(board,square,self.helper.squares[square].diag_moves1,
                               self.helper.squares[square].diag_moves4,(wB,wQ),(bB,bQ))

    def pinned_diag_2_3(self,board,square):
        return self.pinned_ray(board,square,self.helper.squares[square].diag_moves2,
                               self.helper.squares[square].diag_moves3,(wB,wQ),(bB,bQ))
                               
    def pinned_row(self,board,square):
        return self.pinned_ray(board,square,self.helper.squares[square].row_moves1,
                               self.helper.squares[square].row_moves2,(wR,wQ),(bR,bQ))
                               
    def pinned_column(self,board,square):
        return self.pinned_ray(board,square,self.helper.squares[square].column_moves1,
                               self.helper.squares[square].column_moves2,(wR,wQ),(bR,bQ))
    
    def pinned_ray(self,board,square,ray1,ray2,w_attack,b_attack):
        p1 = self.first_piece_ray(board,ray1)
        p2 = self.first_piece_ray(board,ray2)
        if board.turn==WHITE:
            return (p1==wK and p2 in b_attack) or (p2==wK and p1 in b_attack)
        else:
            return (p1==bK and p2 in w_attack) or (p2==bK and p1 in w_attack)
            
    def first_piece_ray(self,board,ray):
        last_val=xx
        for sq in ray:
            last_val=board.get_square(sq.square)
            if last_val!=xx:
                break
        return last_val
    
    def generate_moves_ray(self,board,piece_type,s,ray,only_captures=False):
        moves=[]
        next_turn=oposite(board.turn)
        for dest in ray:
            dest_val=board.get_square(dest.square)
            dest_color=color(dest_val)
            if board.turn==dest_color:
                break
            elif next_turn==dest_color:
                check_list=[]#TODO: Implement check
                check=len(check_list)>0
                moves.append(self.build_move(board,s,dest.square,piece_type,check,
                                            check_list,True,dest_val,None))
                break
            else:
                check_list=[]#TODO: Implement check
                check=len(check_list)>0
                if not only_captures:
                    moves.append(self.build_move(board,s,dest.square,piece_type,check,
                                                check_list,False,xx,None))  
        return moves
    
    def build_move(self,board,source_square,dest_square,piece_type,
                   check,check_moves,fmr_reset,captured_piece,ep=None):
        w_castle_ks_chg=False
        w_castle_qs_chg=False      
        b_castle_ks_chg=False
        b_castle_qs_chg=False  
        if piece_type==wK:
            if board.w_castle_ks:
                w_castle_ks_chg=True
            if board.w_castle_qs:
                w_castle_qs_chg=True
        if piece_type==bK:
            if board.b_castle_ks:
                b_castle_ks_chg=True
            if board.b_castle_qs:
                b_castle_qs_chg=True
        '''Note: This part of the implementation is not CHESS960 friendly'''
        if piece_type==wR:
            if board.w_castle_ks and source_square==63:
                w_castle_ks_chg=True
            if board.w_castle_qs and source_square==56:
                w_castle_qs_chg=True
        if piece_type==bR:
            if board.b_castle_ks and source_square==7:
                b_castle_ks_chg=True
            if board.b_castle_qs and source_square==0:
                b_castle_qs_chg=True
        '''End of note'''
        return Move(source_square,dest_square,piece_type,oposite(board.turn),
                    board.check,check,board.check_moves,check_moves,board.fmr,
                    0 if fmr_reset else board.fmr+1,board.move_num,
                    board.move_num if board.turn=='BLACK' else board.move_num+1,
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