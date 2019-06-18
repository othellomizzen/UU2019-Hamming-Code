#!/usr/bin/env python3
# Created on Thu Jun  6 15:35:16 2019
# author: Cassio da Silva Rodrigues, stundentnummer 5593565

"""
notation for binary numbers: 0b(X)  where (X) is the binary representation
0b101 + 0b001 = 6
bin(0b101 + 0b001) = '0b101'
int('101',2) + int('001',2) = 6



"""

class BitMatrix:
    """
    definition for an nxm matrix, n rows and m columns
    initialisation takes a list with all elements in row order: row1+row2+...
        and the amount of columns (row length)
    """
    
    
    def __init__(self,entries,m,mode="Binary"):
        self.m = m
        self.n = len(entries)//m
        #store all entries in both row and column form, for easier access later
        if mode=="Binary":
            self.entries = BitMatrix.mod2(entries)
        elif mode=="NonBinary":
            self.entries = entries
        self.rows,self.columns = BitMatrix.calculateRowsColumns(self.entries,m)   
    
    def __str__(self):
        matrixString = ' '.join(str(e) for e in self.rows[0]) 
        for i in range(1,len(self.rows)):
            rowstring = ' '.join(str(e) for e in self.rows[i]) 
            matrixString += '\n' + rowstring
        return matrixString
    
    def __add__(self,other):
        if self.n != other.n or self.m != other.m:
            raise Exception('Matrices do not have the same dimensions!')
        return BitMatrix.linearCombination(1,self,1,other)
    
    def __mul__(self,other):
        if type(other) == int or type(other) == float:
            return BitMatrix.linearCombination(other,self)
        else: #so, if other is a matrix
            if self.m != other.n:
                raise Exception('Matrix dimensions are not compatible for multiplication!')
            else:
                resultEntries = BitMatrix.matrixMultiplication(self,other)
                return BitMatrix(resultEntries,other.m)
    
    def __rmul__(self,other):
        return self.__mul__(other) 
    
    
    
    
    @staticmethod
    def linearCombination(a,X,b=None,Y=None):
        #this calculates aX+bY for X,Y matrices, so no matrix multiplication 
        Xentries = X.entries
        if a != 1: #this if statement is potentially unnecessary, is for efficiency's sake
            Xentries = [a*Xentries[i] for i in range(0,len(Xentries))]
        if Y == None: #a*X
            return BitMatrix(Xentries,X.m)
        
        #now for the case Y != None:
        Yentries = Y.entries        
        if b != 1: #for efficiency just as above
            Yentries = [b*Yentries[i] for i in range(0,len(Yentries))]
        
        resultEntries = [Xentries[i]+Yentries[i] for i in range(0,len(Xentries))]
        return BitMatrix(resultEntries,X.m)
    
    @staticmethod
    def matrixMultiplication(A,B):
        #this calculates X*Y (with * being dot product), not Y*X
        #note, for very large matrices, Strassen or other Fast Matrix algorithms might be better
        resultentries = []
        for i in range(0,A.n):
            newrow = []
            for j in range(0,B.m):
                newelement = sum([A.rows[i][k]*B.rows[k][j] for k in range(0,A.m)])
                newrow.append(newelement)
            resultentries += newrow
        return resultentries
        
    @staticmethod
    def calculateRowsColumns(entries,m):
        #when updating matrix via the format Entries, use this to update rows/columns format
        n = len(entries)//m
        rows = []
        columns = []
        for i in range(0,n):
            rows.append(entries[i*m:(i+1)*m])
        for i in range(0,m):
            columns.append([entries[i+m*j] for j in range(0,n)])
        return rows,columns
    
    @staticmethod
    def calculateEntries(rows):
        #when updating matrix via ROWS format, use this to calculate entries(/columns?) format
        entries = []
        for sublist in rows:
            for item in sublist:
                entries.append(item)
        return entries

    @staticmethod
    def mod2(entries):
        #changes all matrix entries to be modulo 2, to work in binary
        return [entries[i]%2 for i in range(0,len(entries))]
    
    @staticmethod
    def ParityMatrix():
        #this creates a 5x4 parity matrix G to multiply with a nibble x; adds a parity to x
        entries = [1,0,0,0,
                   0,1,0,0,
                   0,0,1,0,
                   0,0,0,1,
                   1,1,1,1]
        return BitMatrix(entries,4)
    
    @staticmethod
    def Generator74():
        #this creates a Hamming code generator G for Hamming(7,4)
        entries = [1,1,0,1,
                   1,0,1,1,
                   1,0,0,0,
                   0,1,1,1,
                   0,1,0,0,
                   0,0,1,0,
                   0,0,0,1]
        return BitMatrix(entries,4)
    
    @staticmethod
    def ParityCheck74():
        #this creates a Hamming parity check matrix H for Hamming(7,4)
        entries = [1,0,1,0,1,0,1,
                   0,1,1,0,0,1,1,
                   0,0,0,1,1,1,1]
        return BitMatrix(entries,7)
    
    def Generator(n):
        #n = amount of data bits (4 for Hamming(7,4))        
        # calculate the new total length (+parity bits) we need:
        i = 0
        tempLength = n
        while tempLength > 0:
            i += 1
            if (i & (i - 1)) != 0:  #if i is NOT a power of 2
                tempLength -= 1
        
        totalLength = i
        parityLength = totalLength - n
        
        # Calculating the entries for ParityCheck matrix H:
        rowsH = []
        for k in range(1,parityLength+1):
            newrow = totalLength*[0]
            for l in range(1,totalLength+1):
                if BitMatrix.isKthBitSet(l,k):
                    newrow[l-1] = 1
            rowsH.append(newrow)
            
        """
        entriesG = []
        
        currentParityBit = 0
        currentDataBit = 0
        for k in range(1,totalLength+1):
            #add the k-th row to entriesG
            
            if (k & (k - 1)) == 0:  #if k is a power of 2,
                currentParityBit += 1
                #add the currentParityBit-th row of rowsH, but remove all "power of 2" entries
            else: #if k is NOT a power of 2,
                currentDataBit += 1
                #add the currentDataBit-th row of the nxn Identity Matrix
        """    
            
            
            
        entriesH = [val for sublist in rowsH for val in sublist]
        return BitMatrix(entriesH,totalLength)
        
        
        
        
        
    @staticmethod
    def isKthBitSet(n, k): 
        #specific code taken from https://www.geeksforgeeks.org/check-whether-k-th-bit-set-not/
        if n & (1 << (k - 1)): 
            return True
        else: 
            return False      
    
    @staticmethod
    def eye(n):
        #create identity matrix - is this needed?
        pass
    
    




