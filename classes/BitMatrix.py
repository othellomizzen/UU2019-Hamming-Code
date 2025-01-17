#!/usr/bin/env python3
# Created on Thu Jun  6 15:35:16 2019
# author: Cassio da Silva Rodrigues, stundentnummer 5593565


class BitMatrix:
    """ definition for an nxm matrix, n rows and m columns
    initialisation takes a list with all elements in row order: row1+row2+...
        and the amount of columns (row length)
    Used mainly for matrix-vector multiplication in main.py, but it can also
    be used just by itself if one wishes to perform matrix operations/Hamming
    code tests outside of the runtime loop in main.py """    
    
    def __init__(self,entries,m,mode="Binary"):
        self.m = m
        self.n = len(entries)//m
        if mode=="Binary":
            self.entries = BitMatrix.mod2(entries)
        elif mode=="NonBinary":
            #this non-binary mode can be used to work with general matrices,
            #outside of the scope of the Hamming code
            self.entries = entries
        #store all entries in both row and column form, for easier access later
        #useful for the matrix multiplication formula
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
        #this calculates A*B (with * being dot product), not B*A
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
    def mod2(entries):
        #changes all matrix entries to be modulo 2, to work in binary
        return [entries[i]%2 for i in range(0,len(entries))]
    
    
    """ The following group of methods is not used to work with the matrices 
    directly, but rather the Hamming code-related calculations and declarations. """
    
    @staticmethod
    def ParityMatrices():
        #this creates a 5x4 parity matrix G to multiply with a nibble x; adds a parity to x
        #also creates a 1x5 matrix H to check for (an odd amount of) errors, Hy=H(Gx) should be 0
        entriesG = [1,0,0,0,
                   0,1,0,0,
                   0,0,1,0,
                   0,0,0,1,
                   1,1,1,1]
        entriesH = [1,1,1,1,1]
        return (BitMatrix(entriesG,4),BitMatrix(entriesH,5))
        
    def Generator(n):
        #Creates the generator and parity check matrices G and H 
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
            
        # Calculating the entries for the Generator matrix G:    
        entriesG = []
        currentParityBit = 0
        currentDataBit = 0
        for k in range(1,totalLength+1):
            #add the k-th row to entriesG:
            if (k & (k - 1)) == 0:  #if k is a power of 2,
                newrow = []
                currentParityBit += 1
                #add the currentParityBit-th row of rowsH, but remove all "power of 2" entries
                for index in range(1,totalLength+1):
                    if (index & (index - 1)) != 0:
                        newrow.append(rowsH[currentParityBit-1][index-1])
            else: #if k is NOT a power of 2,
                currentDataBit += 1
                newrow = n*[0]
                #add the currentDataBit-th row of the nxn Identity Matrix
                newrow[currentDataBit-1] = 1
             
            entriesG += newrow
            
            
        entriesH = [val for sublist in rowsH for val in sublist]
        return (BitMatrix(entriesG,n),BitMatrix(entriesH,totalLength))
        
    @staticmethod
    def correct(dataToCorrect,syndromeVector):    
        if all(i == 0 for i in syndromeVector.entries):
            return dataToCorrect #if syndrome vector is zero, no correction is needed!
        
        #syndromeVector.entries is a list of the form [1,0,1,1]
        #read FROM LEFT TO RIGHT to get a bit position to change: above is 1101 = 13 in binary
        #then flip the sign of that position in dataToCorrect.entries, return new vector
        wrongIndexBin = ''
        for k in reversed(syndromeVector.entries):
            wrongIndexBin += str(k)
        wrongIndex = int(wrongIndexBin,2) -1 #convert binary to int index
        correctedData = dataToCorrect.entries.copy()
        correctedData[wrongIndex] = (correctedData[wrongIndex] +1)%2
        
        return BitMatrix(correctedData,1)
        
    @staticmethod
    def isKthBitSet(n, k): 
        #specific code taken from https://www.geeksforgeeks.org/check-whether-k-th-bit-set-not/
        if n & (1 << (k - 1)): 
            return True
        else: 
            return False      
        