# Stephen R. Chestnut
# Johns Hopkins University
# May 2014

import numpy as np
import networkx as nx

class Margins(object):
    """Set of margins for a contingency table sampling instance.

    A set of margins defines the sampling problem.  Subclasses of this class
    implement feasibility checking and matrix checking for various types
    of constraints on the matrix.  To avoid corner cases are considered
    infeasible unless unless the numbers of rows and columns are both positive.

    Example:
        x = Margins([2,2,2,2], [2,2,2,2])

    Args:
        row_sums: integer array with desired row sums
        col_sums: integer array with desired column sums

    Methods:
        isFeasible: True if there is a matrix with these row and column sums
        check(X): True if the numpy array X has row sums r and column sums c
    """
    r=np.array([])
    c=np.array([])
    m=0
    n=0

    def __init__(self, row_sums, col_sums):
        self.r = np.array(row_sums)
        self.c = np.array(col_sums)
        self.m = len(self.r)
        self.n = len(self.c)

    def isFeasible(self):
        """Check if any integer matrix has these row and column sums"""
        return (self.m>0) and (self.n>0) and (sum(self.r) == sum(self.c))

    def check(self, X):
        """Check if the numpy double array X has these margins"""
        
        Y = np.matrix(X)
        return (np.all(np.sum(Y,axis=0) == self.c) 
            and (np.all(np.sum(Y,axis=1).transpose() == self.r))
            and np.all(Y >= 0))
            #transpose b/c np.matrix differentiates between column and row vectors
                
class MarginsWithCellBounds(Margins):
    """Margins for contingency table instance with cell bounds
    
    Margins for a set of contingency tables with given row sums,
    column sums, and cell bounds.  The cell bounds should specificy a 
    nonnegative integer upper bound for each entry in the matrix.

    Example:
        cell_bounds = [ [1,0,1], [1,1,1], [1,1,0] ]
        row_sums = [1,2,1]
        col_sums = [2,1,1]
        MarginsWithCellBounds(row_sums, col_sums, cell_bounds)

    Args:
        row_sums: integer array with m desired row sums
        col_sums: integer array with n desired column sums
        cell_bounds: mxn array describing nonnegative integer cell bounds
            or a single integer to be used as the bound for every cell

    Methods:
        isFeasible: True if there is a binary matrix with these 
                    row and column sums
        check(A): True if A is binary with row sums r and column sums c
    """
    B = np.array([]) 

    def __init__(self, row_sums, col_sums, cell_bounds):
        """Create the margins with cell_bounds"""

        if type(cell_bounds) is int:
            cell_bounds = cell_bounds * np.ones((len(row_sums),len(col_sums)),dtype=int)
            
        super(MarginsWithCellBounds, self).__init__(row_sums,col_sums)
        self.B = np.array(cell_bounds)


    def _flowProblem(self):
        """Create and run the network for the feasibility flow problem"""
        D = nx.DiGraph()
        
        #nodes are rows/columns, edges are row->column,
        #B defines edge capacities
        D.add_nodes_from(range(self.m+self.n))
        for ii in range(self.m):
            for jj in range(self.n):
                if self.B[ii][jj]>0:
                    D.add_edge(ii,self.m+jj,capacity=self.B[ii][jj])
                    
        #source and sink nodes, row/column sums define capacities on the
        # source/sink edges
        D.add_node('s')
        D.add_node('t')
        for ii in range(self.m):
            D.add_edge('s',ii,capacity=self.r[ii])
        for jj in range(self.n):
            D.add_edge(jj+self.m,'t',capacity=self.c[jj])

        return nx.max_flow(D,'s','t',capacity='capacity')
        
    
    def isFeasible(self):
        """Check if the margins and cell bounds are feasible

        Use networkx.max_flow to determine feasibility as follows.  Create
        a bipartite graph with cell_bounds for its biadjacency matrix.
        Add a node s adjacent to the row vertices and a node t adjacent 
        to the column vertices.  Place capacities 1 on the original graph
        edges, row_sums on the edges from s, and col_sums on edges to t.
        If the max flow has value sum(row_sums) then the problem is feasible.
        """
        
        return ( (self._flowProblem() == sum(self.r)) and
                super(MarginsWithCellBounds, self).isFeasible() )
    
    def check(self, X):
        """Check if the numpy double array X has these margins and is binary"""
        
        return (super(MarginsWithCellBounds, self).check(X) 
                and np.all(X <= self.B))
                
def load(name):
    """Load an instance by name"""
    
    files = {'forum1' : ['../../../dat/forums/r1.txt',
                         '../../../dat/forums/c1.txt'],
             'synapse': ['../../../dat/neurons/spineSynapseMatrix.csv',
                         '../../../dat/neurons/spineTouchMatrix.csv']}
                         
    if name is 'synapse':
        ssm = np.loadtxt(open(files['synapse'][0],"rb"),delimiter=",",dtype=int)
        B   = np.loadtxt(open(files['synapse'][1],"rb"),delimiter=",").astype(int)
        ssm = ssm.astype(int)
        r = np.sum(ssm,axis=1)
        c = np.sum(ssm,axis=0)
        for ii in range(len(B)):
            for jj in range(len(B[0])):
                if abs(B[ii][jj]) > 0.0:
                    B[ii][jj]=1
                else:
                    B[ii][jj]=0
    else:
        r = np.loadtxt(files[name][0],dtype=int)
        c = np.loadtxt(files[name][1],dtype=int)
        B = 1
        
    return MarginsWithCellBounds(r,c,B)
                        