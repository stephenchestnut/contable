import sys
sys.path.insert(0, './src/main/python')

from contable import *
import numpy as np
import unittest
import contable.margins as margins
import contable.samplers as samplers
import contable.tabletools as tabletools


class TestBoundedExactRowsExpectedColumns(unittest.TestCase):
    
    def setUp(self):
        self.m = [margins.MarginsWithCellBounds([3,2,1],[2,2,1,1],1),
                  margins.MarginsWithCellBounds([2,2,2,2],[2,2,2,2],[[0,1,1,1],
                                                                     [1,0,1,1],
                                                                     [1,1,0,1],
                                                                     [1,1,1,0]]),
                  margins.MarginsWithCellBounds([2,1,3],[2,2,1,1],[[1,1,1,2],
                                                                   [1,4,1,0],
                                                                   [2,1,6,1]]),
                  margins.MarginsWithCellBounds([10],[1,2,3,4],[[1,2,3,4]])]
        self.sam = []
        for mii in self.m:
            self.sam.append(samplers.BoundedExactRowsExpectedColumns(mii))
    
    def test___init__(self):
        """Check that __init__ assigns what it should
        
        Correctness of the assigned values is checked elsewhere
        """
                
        def test_table_dimensions(table,m,n,h):
            """Test the dimensions of a Bounded...umns.table

            Args:
                table: sampler.Bou..umns.table to test
                m: number of subtables
                n: number of columns in each subtable
                h: vector with number of rows in subtable for each of the m
            """
            
            self.assertEqual(len(table),m)
            for ii in range(len(table)):
                self.assertEqual(len(table[ii]),n)
                for row in table[ii]:
                    self.assertEqual(len(row),h[ii])
                    
        for (m,sam) in zip(self.m,self.sam):
            self.assertEqual(m,sam.margins)  #margins are correct
            test_table_dimensions(sam.table, #table has correct sizes
                              m.m,
                              m.n + 1,
                              np.array(m.r)+1)
                              
    def test_table(self):
        """The table computed should be correct"""

        # Test the entire table for sam[1]        
        sam = self.sam[1]
        w = sam.w[0]
        
        self.assertTrue(np.allclose(sam.w, w))
        
        c = [[1., 3 * w , 3 * w * w],
             [1., 2 * w , w * w],
             [1.,     w , 0.],
             [1.,     0., 0.]]
             
        for ii in range(4):
            tab = []
            for jj in range(4):
                tab.append(c[jj])
                if ii == jj:
                    tab.append(c[jj])
            self.assertTrue(np.allclose(tab, sam.table[ii]))
                
        #check table for sam[2], final row
        sam = self.sam[2]
        w = sam.w
        tab = [[1.,     sum(w), w[0] * sum(w) + w[1] * (w[2] + w[3]) + w[2]*w[2] + w[2]*w[3], w[0] * w[0] * sum(w[1:]) + w[0] * (w[1] * (w[2] + w[3]) + w[2]*w[2] + w[2]*w[3]) + w[1] * w[2] * (w[2] + w[3]) + w[2] * w[2] * w[3] + w[2] ** 3],
               [1., sum(w[1:]),                 w[1] * (w[2] + w[3]) + w[2]*w[2] + w[2]*w[3],                                                                                    w[1] * w[2] * (w[2] + w[3]) + w[2] * w[2] * w[3] + w[2] ** 3],
               [1.,w[2] + w[3],                                        w[2]*w[2] + w[2]*w[3],                                                                                                                  w[2] * w[2] * w[3] + w[2] ** 3],
               [1.,       w[3],                                                           0.,                                                                                                                                              0.],
               [1.,         0.,                                                           0.,                                                                                                                                              0.]]
        self.assertTrue(np.allclose(tab,sam.table[2]))
        
    def test_sample(self):
        """Sample many matrices and test that the distribution is correct"""

        print('')
        print('H0: sampling distribution is correct')
        print('HA: sampling distribution is not correct')
        for ii in [0,1,2]:
            print('Bounded table instance ' + str(ii) + 
            ' chi-square test p-value: ' + '{:.3f}'.format(
                            tabletools.test_this_sampler( self.sam[ii], 10000)))
        print('')
        
        return 0
                    
class TestBinaryExactRowsExpectedColumns(unittest.TestCase):
    
    def setUp(self):
        self.m = [margins.MarginsWithCellBounds([3,2,1],[2,2,1,1],1),
                  margins.MarginsWithCellBounds([2,2,2,2],[2,2,2,2],1)]
        self.sam = []
        for mii in self.m:
            self.sam.append(samplers.BinaryExactRowsExpectedColumns(mii))
                              
        
    def test_sample(self):
        """Sample many matrices and test that the distribution is correct"""

        print('')    
        print('H0: sampling distribution is correct')
        print('HA: sampling distribution is not correct')
        for ii in [0,1]:
            print('Binary table instance ' + str(ii) + 
            ' chisquare test p-value: ' + '{:.3f}'.format(
                            tabletools.test_this_sampler( self.sam[ii], 100)))
        print('')
        
        return 0