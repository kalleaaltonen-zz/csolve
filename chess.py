from itertools import chain,product,combinations
import copy
import operator
import string
import datrie

# R Rook
# N knight
# B Bishop
# Q Queen
# K King
PIECES = set("RNBQK")

def prune(iter,bx,by):
    return ((x,y) for (x,y) in iter if x >= 0 and y >= 0 and x < bx and y < by)

def threatens(piece, x, y, bx, by):
    if piece == "R":
        return chain(((x,j) for j in range(by) if j != y), 
                     ((i,y) for i in range(bx) if i != x))
    elif piece == "K":
        return prune(((x+i-1,y+j-1) for i in range(3) for j in range(3) if (i,j) != (1,1)), bx, by)
    elif piece == "N":
        a=([-1,1],[-2,2])
        return prune(((x+i,y+j) for (i,j) in chain(product(*a), product(*a[::-1]))), bx, by)
    # (1,1) = (0,0), (2,2)
    elif piece == "B":
        return prune(chain(((x+i,y+i) for i in range(-bx,bx) if i!=0), ((x+i,y-i) for i in range(-bx,bx) if i!=0)), bx, by)
    elif piece == "Q":
        return chain(threatens("R",x,y,bx,by), threatens("B",x,y,bx,by))
    else:
        print('unknown piece %s', piece)

FLIP = lambda a: list(reversed(a))
NOFLIP = lambda a: a
ROTATE0 = lambda a: a
ROTATE90 = lambda a: [list(t) for t in zip(*a[::-1])]
ROTATE180 = lambda a: ROTATE90(ROTATE90(a))
ROTATE270 = lambda a: ROTATE90(ROTATE90(ROTATE90(a)))


class Board(object):
    def __init__(self,bx,by,data=None,free=None):
        self.bx = bx
        self.by = by
        self.data = data or [list('.'*by) for j in range(bx)]
        if free == None and not data:
            self.free = set(product(range(bx), range(by)))
        else:
            self.free = free
        self.repr = "\n".join("".join(row) for row in self.data)
    def __repr__(self):
        return self.repr
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__repr__() == other.__repr__())
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return self.__repr__().__hash__()
    def rotations(self):
        """ Doesn't translate free lists 
        """
        return set(Board(self.bx,self.by,data=list(fs[0](fs[1](self.data)))) for fs in product([FLIP, NOFLIP], [ROTATE0,ROTATE90,ROTATE180,ROTATE270]))
    def get_canonical(self):
        return min(r.__repr__() for r in self.rotations())
    def is_canonical(self):
        return self.__repr__() == get_canonical(self)
    def add_piece(self, moves):
        if not moves or any(move[1:] not in self.free for move in moves):
            #print "not in free %s free=%s" % (moves,self.free)
            return None

        # Check if this piece threatens someone
        threats = set(chain( *[threatens(*(t+(self.bx,self.by))) for t in moves]))

        if any(self.data[i][j] != '.' for (i,j) in threats):
            #print "threatens someone"
            return None

        # Check if the new pieces threaten each other
        if any(move[1:] in threats for move in moves):
            #print "threatens %s eachother %s", (moves, threats)
            return None
        newFree = self.free - threats - set(move[1:] for move in moves)

        newData = copy.deepcopy(self.data)
        for (p,x,y) in moves:
            newData[x][y] = p
        return Board(self.bx, self.by, data=newData, free=newFree)

def impact(piece, x,y):
    return len(list(threatens(piece, x/2, y/2, x, y)))

def get_ordering(pieces, board):
    #return sorted(pieces, key=lambda x: impact(x[0], board.bx, board.by))
    return sorted(pieces, key=lambda x: x[1]*100-impact(x[0], board.bx, board.by), reverse=True)
    #return sorted(pieces, key=lambda x: list("BNKRQ").index(x[0]), reverse=True)
    #return sorted(pieces, key=lambda x: x[1]*impact(x[0], board.bx, board.by)/len(list(combinations, x[1])), reverse=False)

def free_rows_and_columns(data):
    return (sum( 1 for row in data if all(square == '.' for square in row)),
            sum( 1 for row in zip(*data[::-1]) if all( square == '.' for square in row)))

def filterNode(n,pieces):
    if len(n.free) < sum(p[1] for p in pieces):
        #print "%s %s %s"%(len(n.free), sum(p[1] for p in pieces), pieces)
        return False

    queens_and_rooks = sum(p[1] for p in pieces if p[0] in {'Q','R'})

    if queens_and_rooks > min(free_rows_and_columns(n.data)):
        #print "Filter because queens and rooks"
        return False

    return True

def solve(board,pieces):
    candidates=[board]
    next_candidates = iter([])
    pieces = get_ordering(pieces, board)
    print "pieces %s" % (pieces,)
    trie = datrie.Trie("%s.\n"%pieces)
    trie = {}

    while pieces:
        (piece, count) = pieces.pop()
        print "processing %s %i" % (piece, count)
        #print hpy().heap()
        for c in candidates:
            cform = unicode(c.get_canonical().__repr__())
            if cform not in trie:
                #print cform
                trie[cform] = True
                moves = ( [(piece,) + t for t in c] for c in combinations(c.free, count))
                next_candidates = chain(next_candidates, [c.add_piece(move) for move in moves])

#                next_candidates.extend()
            #print "canditates now %i" % len(next_candidates)
        candidates = (n for n in next_candidates if n != None and filterNode(n, pieces))
        #print "next_candidates %i" % len(candidates)
        next_candidates = iter([])
    return candidates

def solve_dfs(board, pieces): 
    stack = [(board, pieces)]
    solutions = []
    #discovered = {}
    discovered = datrie.Trie("%s.\n"%pieces)
    print "order: %s" % pieces
    while stack:
        b, ps = stack.pop()
        (p, count), left = ps[0], ps[1:]
        moves = ( [(p,) + t for t in c] for c in combinations(b.free, count))
        for move in moves:
            c = b.add_piece(move)
            if not c:
                continue
            cform = unicode(c.get_canonical().__repr__())
            if cform in discovered:
                continue
            discovered[cform] = True
            if not filterNode(c, left):
                #print "filtered!"
                continue

            if not left:
                solutions.append(c)
                print "%s\nstack size: %i solutions found: %i" % (c, len(stack), len(solutions))
                continue
            stack.append((c, left))
    return solutions

def start(bx, by, pieces):
    board = Board(bx,by)
    results = solve_dfs(board,get_ordering(pieces, board)) # set( reduce(operator.xor ,(b.rotations() for b in solve(board,pieces))))
    print "===== RESULTS =============="
    #for r in results:
    #    print "%s\n\n" % r
    print len(list(results))

if __name__ == "__main__":
    #start(7,8,[("K",3),('Q',1),('B',2),('R',2), ('N',3)])
    start(6,6,[("K",2),('Q',1),('B',3),('R',2), ('N',1)])
    #start(5,5,[('Q',1), ('R', 1), ('N',4)])
    start(3,3,[('K',1), ('R', 2)])

