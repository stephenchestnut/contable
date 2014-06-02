"""Classes for randomly sampling contingency tables

Classes:
   Sampler: abstract base class for samplers
   BinaryExactRowsExpectedColumns: sample binary contingency tables

"""
from abc import ABCMeta, abstractmethod
import contable.margins as margins
from random import random
from scipy.optimize import fsolve
import collections
import numpy as np
import pdb

class Sampler(object):
    """ Abstract base class for sampling algorithms

    This is an abstract base class that implements repeated sampling
    and rejection sampling for its derivative classes.

    Args:
        marg (Margins): set of margins for the target instance
   
    Methods:
        sample: (abstract) sample one matrix
        samples: sample n matrices
    
    """
    __metaclass__ = ABCMeta

    margins = margins.Margins([],[])

    @abstractmethod
    def __init__(self, marg):
        pass

    @abstractmethod
    def sample(self):
        """Sample one matrix"""
        pass

    def samples(self, n):
        """Sample n matrices"""
        l = []
        for ii in range(n):
            l.append(self.sample())
        return l

    def rejectionsample(self, maxiter=100 ):
        """Sample one matrix with exact row and columns sums"""
        ii = 1
        while ii <= maxiter:
            s = self.sample()
            if self.margins.check(s):
                return s
        return None
            
class BoundedExactRowsExpectedColumns(Sampler):
    """ Sample binary contingency tables    
    
    Sample from a distribution on contingency tables with cell bounds.  The
    sampled tables have the correct row sums and the column sums are correct
    in expectation.  The sampler produces matries with the following 
    properties:
        (1) Row sums equal margins.r
        (2) The expected column sums are margins.c
        (3) The rows are independent
        (4) The matrices are sampled uniformly conditionally given the 
            column sums
        (5) The value of cell (i,j) is at most margins.B[i][j]
    The sampling algorithm uses dynamic programming to sample each
    row with weighted subset sampling.  The weights are determined 
    by root-finding during initialization.
    
    Args:
        marg:MarginsWithCellBounds describing the instance
        
    Vars:
        w: array of margins.n weights for the sampling
        table: dynamic programming table
        
    Methods:
        colMeans: expected sum of each column
        sample: pseudorandomly generate a matrix
    """
    w = []
    table = []

    def colMeans(self):
        """Return the expected sum of each column"""

        return self._computeColMeans(self.w)

    def _computeColMeans(self, w):
        """Expected sum of each column for a given set of weights"""

        """The strategy is as follows:
            We compute the expected values one column at a time.
            For a particular column colj and row rowi we must compute the
            probability of a 1,2,..., or cell_bound[rowi][colj] in that column
            In order to compute the probability, we need to know the total 
            weight of all r[rowi] multisubsets (for the denominator) and the
            total weight of all r[rowi]-1,r[rowi]-2,.., and r[rowi]-bb
            multisubsets (for the numerators).  We can get all of this
            information from one call to the table generator by reordering
            the columns so that colj is first."""
            

        w = list(w)
        # expected sum of column colj
        c = [0.0] * self.margins.n
        for colj in range(self.margins.n):
            # contribution from rowi
            for rowi in range(self.margins.m):
                ri = self.margins.r[rowi]
                Bi = list(self.margins.B[rowi])
                t = self._computeTable(w[colj:(colj+1)] + w[0:colj] + w[(colj+1):], 
                                   ri, 
                                   Bi[colj:(colj+1)] + Bi[0:colj] + Bi[(colj+1):])
                # contribution when (i,j) has value bb
                mul = 1.0
                for bb in range(1, 1 + np.min([Bi[colj], ri])):
                    mul *= w[colj] #w[colj] ** bb
                    c[colj] += bb * mul * t[1][ri-bb] / t[0][ri] # bb * Pr[ entry rowi,colj equals bb]
        return c
                

    def _computeWeights(self):
        """Find weights that meet the column sums constraint"""
        #c = np.array(self.margins.c,dtype=float)
        #if np.allclose(self._computeColMeans(c), c):
        #    return c
            
        def f(w):
            w = list(w)
            return np.array(self._computeColMeans(w)) - np.array(self.margins.c)
        w = fsolve(f, np.array(self.margins.c,dtype=float))
        return w

    def _computeTable(self, w, k, b):
        """Create a dynamic programming table for weighted subset sampling
        
        The weight of a subset is the product of the weights of its elements.
        This method computes the sum of the weights of all of the l-element
        multi-subsets that obey the bounds in b, for each 0 <= l <= k.
        
        Args:
            w: array of weights
            k: maximum size subset to consider
            b: array with bounds on number of times to take each element
            
        Return:
            t: array where entry i,j is the total weight of all j-element
                multi-subsets of w_i,w_{i+1},...,w_{n-1} that satisfy bounds
        """
        
        t = [ [1.0] + [0.0]*k ]
        n = len(w)
        for ii in range(n):
            tii = [ t[-1][0] ]
            for jj in range(1,k+1):
                acc = 0.0
                mul = 1.0
                for bb in range(1+np.min((jj,b[n-1-ii]))):
                    acc += t[-1][jj-bb] * mul
                    mul *= w[n-1-ii]
                tii.append(acc)
            t.append(tii)
        t.reverse()
        return t

    def __init__(self, marg):
        """Solve for the weights and initialize the table"""
        
        self.margins = marg
        self.w = self._computeWeights()
        self.table = []
        for rowi in range(self.margins.m):
            self.table.append(self._computeTable(self.w, 
                                                 self.margins.r[rowi], 
                                                 self.margins.B[rowi]))
                                                 
    def _sampleRow(self, rowsum, table): 
        """Sample one row of the matrix by randomly walking its table"""
        
        remaining = rowsum
        n = len(table)-1
        row = [0]*n
        for colj in range(n):
            U = random()
            X = 0
            p = table[colj+1][remaining] / table[colj][remaining] #Pr(jth entry = 0)
            mul = 1.0
            while U > p:
                X += 1
                mul *= self.w[colj]
                p += mul * table[colj+1][remaining-X] / table[colj][remaining] #Pr(jth entry = X)
            remaining -= X
            row[colj]=X
        return row
    
    def sample(self):
        """Sample a matrix with independent rows"""
        
        mat = []
        for rowi in range(self.margins.m):
            mat.append(self._sampleRow(self.margins.r[rowi],self.table[rowi]))
        return mat

class BinaryExactRowsExpectedColumns(BoundedExactRowsExpectedColumns):
    """Sampling binary matrics with given row sums and column sums in expectation
    
    A specialization of BoundedEx...umns to the case where the bounds are all 1.
    Some speed is gained because only one dynamic programming table must be
    maintained (rather than margins.m of them)
    """
    
    def __init__(self,marg):
        self.margins = marg
        self.w = self._computeWeights()
        self.table = self._computeTable(self.w, max(self.margins.r), [1]*self.margins.n)
        
    def _computeColMeans(self,w):
        """Compute column means using the fact that rows with identical sums make identical contributions"""
        
        w = list(w)
        c = np.array([0.0] * self.margins.n)
        countDict = collections.Counter(self.margins.r)
        for colj in range(self.margins.n):
            t = self._computeTable(w[colj:(colj+1)] + w[0:colj] + w[(colj+1):], 
                                   max(self.margins.r), 
                                   [1] * self.margins.n)
            for ri in countDict:
                c[colj] += countDict[ri] * w[colj] * t[1][ri-1] / t[0][ri]
        return c
    
    def sample(self):
        mat = []
        for rowsum in self.margins.r:
            mat.append(self._sampleRow(rowsum,self.table))
        return mat