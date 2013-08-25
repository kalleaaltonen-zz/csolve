import unittest
from chess import threatens, Board,free_rows_and_columns

class TestChess(unittest.TestCase):
	def test_threatens(self):
		# .N..
		# ...*
		# *.*.
		# ....
		self.assertItemsEqual(set(threatens("N", 0,1,4,4)), ((1,3), (2,0), (2,2)))

		# ....
		# .***
		# .*K*
		# .***
		self.assertItemsEqual(set(threatens("K", 2,2,4,4)), ((1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)))

		# *...
		# *...
		# *...
		# R***
		self.assertItemsEqual(set(threatens("R", 0,3,4,4)), ((0,0), (0,1), (0,2), (1,3), (2,3), (3,3)))


		# .*.*
		# ..B.
		# .*.*
		# *...
		# ....
		self.assertItemsEqual(set(threatens("B", 1,2,5,4)), ((0,1), (0,3), (2,1), (2,3), (3,0)))

		# *...
		# .*.*
		# ..B.
		# .*.*
		self.assertItemsEqual(set(threatens("B", 2,2,4,4)), ((0,0),(1,1),(1,3),(3,1),(3,3)))


		# *.*.
		# .***
		# **Q*
		# .***
		self.assertItemsEqual(set(threatens("Q", 2,2,4,4)), ((1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3), (0,0), (2,0), (0,2)))

	def test_board(self):
		# ..    NN
		# .. => NN
		b = Board(2,2)
		print b.free
		self.assertTrue(b.add_piece([("N",0,0)]))
		b2 = b.add_piece([("N",0,0),("N",0,1),("N",1,0),("N",1,1)])
		self.assertTrue(b2)
		self.assertEquals(len(b2.free), 0, "\n%s\n\nfree:%s"%(b2, b2.free))
		self.assertFalse(b.add_piece([("Q",0,0),("Q",1,1)]))

	def test_free_rows_and_columns(self):
		b = Board(2,2)
		self.assertEquals(free_rows_and_columns(b.data),(2,2))
		b2 = b.add_piece([("N",0,0)])
		self.assertEquals(free_rows_and_columns(b2.data),(1,1))
		b3 = b2.add_piece([("N",0,1)])
		self.assertEquals(free_rows_and_columns(b3.data),(1,0), b3)

	def test_eq(self):
		a = Board(2,2)
		b = Board(2,2)
		c = a.add_piece([("N",0,0)])
		self.assertTrue(a == a)
		self.assertTrue(a == b)
		self.assertTrue(b == a)
		self.assertTrue(a != c)


	def test_rotations(self):
		b = Board(2,2) #.add_piece([("N",0,0)])
		print b.__dict__
		rots = list(b.rotations())
		for r in rots:
			print r.__dict__
		self.assertTrue(all(a==b for a in rots for b in rots))
		self.assertItemsEqual(rots, [b])	
