wR=1
wN=2
wB=3
wQ=4
wK=5
wP=6
bR=7
bN=8
bB=9
bQ=10
bK=11
bP=12
xx=13

def color(code):
    if not (0<code<=bP):
        return xx
    else:
        return 'WHITE' if 1<=code<=6 else 'BLACK'

WHITE='WHITE'
BLACK='BLACK'
EMPTY=-1

ALL_PIECE_CODES=[wR,wN,wB,wQ,wK,wP,bR,bN,bB,bQ,bK,bP,xx]
