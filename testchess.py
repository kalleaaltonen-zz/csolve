import unittest
from chess import threatens

class TestTransform(unittest.TestCase):
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
		self.assertItemsEqual(set(threatens("B", 1,2,4,4)), ((0,1), (0,3), (2,1), (2,3), (3,0)))

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

