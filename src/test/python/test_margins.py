import sys
sys.path.insert(0, './src/main/python')

from contable import *
import unittest
import contable.margins as margins


class TestMargins(unittest.TestCase):
    
    def setUp(self):
        self.m1 = margins.Margins([2,2,2,2],[2,2,2,2])
        self.m2 = margins.Margins(range(5),range(5))
        self.m3 = margins.Margins([],[])
        self.m4 = margins.Margins([3]*4, [2]*6)
        self.m5 = margins.Margins([3,1,3],[2,3,4])
        self.m6 = margins.Margins([10],[1,2,3,4])
    
    def test_isFeasible(self):
        """isFeasible should correctly determine whether there is a 
        nonnegative integer matrix satisfying the given margins.
        """
        
        self.assertTrue(self.m1.isFeasible())
        self.assertTrue(self.m2.isFeasible())
        self.assertFalse(self.m3.isFeasible())
        self.assertTrue(self.m4.isFeasible())
        self.assertFalse(self.m5.isFeasible())
        self.assertTrue(self.m6.isFeasible())
        
    def test_check(self):
        """check should correctly determine if a matrix satisfies the constraints
        
        If the contable.margins are feasible, check should correctly determine
        whether the given matrix has the desired margins. 
        If the margins are not feasible, the output is undefined.
        """

        M = [[1,1,0,0],
             [1,1,0,0],
             [0,0,1,1],
             [0,0,1,1]]
        self.assertTrue(self.m1.check(M))

        M = [[0,2,0,0],
             [2,0,0,0],
             [0,0,1,1],
             [0,0,1,1]]
        self.assertTrue(self.m1.check(M))
        
        M = [[0,3,0,-1],
             [3,0,-1,0],
             [-1,0,2,1],
             [0,-1,1,2]]
        self.assertFalse(self.m1.check(M))

        M = [[2,0,0,0,1,0],
             [0,2,0,0,0,1],
             [0,0,2,0,1,0],
             [0,0,0,2,0,1]]
        self.assertTrue(self.m4.check(M))
                                      
        self.assertTrue(self.m6.check([1,2,3,4]))
        
class TestMarginsWithCellBounds(unittest.TestCase):

    def setUp(self):
        self.m1 = margins.MarginsWithCellBounds([],[],1)
        self.m2 = margins.MarginsWithCellBounds(range(1,6),range(1,6),1)
        
        #Infeasible problem with non-uniform bounds/margins
        self.m3 = margins.MarginsWithCellBounds([2,1,3],[2,2,1,1], 
                                                [[1,0,1,0],
                                                 [0,0,1,4],
                                                 [0,1,6,2]])
        #Feasible problem with non-uniform bounds/margins                                         
        self.m4 = margins.MarginsWithCellBounds([2,1,3],[2,2,1,1], 
                                                [[1,1,1,2],
                                                 [1,0,1,4],
                                                 [3,1,6,1]])
        #Feasible binary problem
        self.m5 = margins.MarginsWithCellBounds([3,3,2,2,2,1,1,1],[5,4,3,3],1)
    
    def test__flowProblem(self):
        """Is the max-flow of the returned graph correct
        
        This test only checks the value of the flow, not the structure of 
        the graph.
        """
        
        F = self.m2._flowProblem()
        self.assertEqual( F, 15.0)
        
        F = self.m3._flowProblem()
        self.assertEqual(F, 4.0)        

        F = self.m4._flowProblem()
        self.assertEqual(F, 6.0)

        F = self.m5._flowProblem()
        self.assertEqual(F, 15.0)

    
    def test_isFeasible(self):
        """isFeasible should correctly determine whether there is a 
        nonnegative integer matrix satisfying the given margins and cell bounds
        """
        self.assertFalse(self.m1.isFeasible())
        self.assertTrue(self.m2.isFeasible())
        self.assertFalse(self.m3.isFeasible())
        self.assertTrue(self.m4.isFeasible())
        self.assertTrue(self.m5.isFeasible())
        
    def test_check(self):
        """check should determine if a matrix meets the specified row/column
        sums and the cell bounds
        """
        M = [[1,1,0,0],
             [0,0,1,0],
             [1,1,0,1]]
        self.assertTrue(self.m4.check(M))

        M = [[0,2,0,0],
             [0,0,1,0],
             [2,0,0,1]] #does not satisfy the (0,1) cell bound
        self.assertFalse(self.m4.check(M))
        
        
if __name__ == '__main__':
    unittest.main()