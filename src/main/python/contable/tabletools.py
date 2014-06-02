import numpy as np
from scipy.stats import chisquare

def build_all_matrices(r,B):
    """ Build all len(r)xn matrices with row sums r and bounds B
    
    Args:
        r: list of row sums for desired matrices
        n: number of columns
        B: cell bounds
        
    Output: list of all matrices (roworder) with nonnegative
        integer entries that have row sums r and satisfy the cell
        bounds B
    """
    def build_rows(rowsum, bounds):
        """ Build all rows that have sum rowsum and the given bounds"""
        
        def row_acc(acc, rembounds):
            if len(rembounds) == 0:
                return acc
            else:
                newacc = []
                for partrow in acc:
                    for val in range(1+np.min([rowsum - int(sum(partrow)), rembounds[0]])):
                        newacc.append( partrow + [val])
                return row_acc(newacc, rembounds[1:])
        
        def correctsum(l): return sum(l)==rowsum
        
        return filter(correctsum, row_acc([[]],bounds))
        
    def mats_acc(acc, remrowlists):
        """Build all matrices from a list of the possibilities for each row"""

        if len(remrowlists)==0:
            return acc
        else:
            newacc = []                
            for row in remrowlists[0]:
                for mat in acc:
                    newacc.append( mat + [row])
            return mats_acc(newacc, remrowlists[1:])
            
    rowlists = []
    for ii in range(len(r)):
        rowlists.append( build_rows(r[ii],B[ii]))
    return mats_acc([[]], rowlists)
    
def test_this_sampler(sam, num_samples):
    """Test a single sampler an report p-value from a chisquare test"""
    
    allMats = build_all_matrices(sam.margins.r, sam.margins.B)
    #compute a probability for each matrix in allMats
    p = []
    for mat in allMats:
        colsums = np.sum(mat,axis=0)
        wt = 1.0
        for ii in range(len(colsums)):
            wt *= sam.w[ii] ** colsums[ii]
        p.append(wt)
    p = np.array(p)
    p /= np.sum(p)
    
    counts = [0]*len(allMats)
    for nn in range(num_samples):
        randmat = sam.sample()
        counts[ allMats.index(randmat) ] += 1
    counts = np.array(counts,dtype=float)
    #phat = counts / num_samples
    #stderrors = (p-phat) / np.sqrt( p * (1-p) / num_samples)

    (garb, pval) = chisquare(counts, p*num_samples)        
    
    return pval