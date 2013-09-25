'''
Created on 2011-3-3
 
@author: vertusd
'''
import gc
class GcHelper(object):
    '''
     Gc Helper Class, for memery leakage locating
    '''
 
 
    def __init__(self):
            pass
    @staticmethod   
    def gcHistogram(): 
            """Returns per-class counts of existing objects.""" 
            result = {} 
            for o in gc.get_objects(): 
                    t = type(o) 
                    count = result.get(t, 0) 
                    result[t] = count + 1 
            return result 
    @staticmethod   
    def diffHists(h1, h2): 
        """Prints differences between two results of gcHistogram().""" 
        for k in h1: 
                if h1[k] != h2[k]: 
                        print "%s: %d -> %d (%s%d)" % ( 
                                k, h1[k], h2[k], h2[k] > h1[k] and "+" or "", h2[k] - h1[k]) 