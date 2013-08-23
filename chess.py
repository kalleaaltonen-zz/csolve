from itertools import chain,product

# R Rook
# N knight
# B Bishop
# Q Queen
# K King
PIECES = set("RNBQK")

def prune(iter,bx,by):
    return ((x,y) for (x,y) in iter if x >= 0 and y >= 0 and x < bx and y < bx)

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

class Board(object):
    def __init__(self,bx,by,data=None,free=None):
        self.bx = bx
        self.by = by
        self.data = data or [list('.'*bx) for j in range(by)]
        self.free = free or set(product(range(bx), range(by)))
    def __repr__(self):
        return "\n".join("".join(row) for row in self.data)
        #for j in range(self.by):
        #    val.append("".join([ self.pieces.get((i,j), "." if (i,j) in self.free else ",") for i in range(self.bx)]))
        #return "\n".join(val)
    def add_piece(self, piece, x, y): 
        if (x,y) not in self.free:
            print "(%i,%i) not in free" % (x,y)
            return None

        # Check if this piece threatens someone
        threats =  set(threatens(piece,x,y,bx,by))
        if any(self.data[i][j] != '.' for (i,j) in threats):
            print "%s at (%i,%i) threatens someone" % (piece,x,y)
            return None

        newFree = self.free - threats - {(x,y)}
        newData = list(self.data)
        newData[x][y] = piece
        return Board(self.bx, self.by, data=newData, free=newFree)


pieces = ["N", "N"]
def main():

	print "main"

if __name__ == "__main__":
	main()
