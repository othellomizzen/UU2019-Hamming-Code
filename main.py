#!/usr/bin/env python3
# Created on Fri Jun 21 13:35:03 2019
# author: Cassio da Silva Rodrigues, stundentnummer 5593565
from classes.BitMatrix import BitMatrix
import copy
import random
from datetime import datetime
random.seed(datetime.now())



"""
This program shall have two modes; the user inputs a string, and either:
    - flip one of the bits of the raw data and display the corrupted data back as a text string,
        followed by using Hamming(7,4) to correct the corrupted message, or;
    - use a general Hamming code and corrupt->correct without displaying the wrong data as text.
The reason for this is that I cannot think of a meaningful way to convert corrupted data back
to text when not storing it as nibbles and using Hamming(7,4)

Simply for the purposes of having a general Hamming code to correct data, the first option
is completely unnecessary. However, it is simply fun to see on the screen what the corrupted 
data would translate back into as text.
"""




# The following functions convert between text<->nibble and flip bits

def StringToNibbleList(message):
    wholeBinaryString = ''.join(format(ord(x), 'b').zfill(8) for x in message)    
    nibbleList = []
    for i in range(0,len(message)*2):
        nibbleList.append([int(bit) for bit in wholeBinaryString[i*4:(i+1)*4]])
    return nibbleList

def NibbleListToString(nibbleList):
    byteList = []
    for i in range(0,len(nibbleList)//2):
        #add two nibbles to make a byte, then store as string
        newByte = ''.join([str(k) for k in nibbleList[i*2]+nibbleList[i*2 +1]])
        byteList.append(newByte)
    return ''.join(chr(int(i,2)) for i in byteList)


def flipRandomBit(bitList):
    #note: randint generates numbers up to AND INCLUDING the upper bound
    #bitList is a list containing lists with the grouped bits:
    #can be both raw data (such is nibbles) and already encoded (such as Hamming(7,4))
    groupRandom = random.randint(0,len(bitList)-1)
    bitRandom = random.randint(0,len(bitList[0])-1)
    flippedList = copy.deepcopy(bitList)
    flippedList[groupRandom][bitRandom] = (flippedList[groupRandom][bitRandom]+1)%2
    return flippedList






"""
def encodeMessage74(message):
    nibbleList = StringToNibbleList(message)
    G,H = BitMatrix.Generator(4)
    encodedList = []
    for nibble in nibbleList:
        nibbleEntries = [int(i) for i in nibble]
        nibbleVector = BitMatrix(nibbleEntries,1)
        product = G*nibbleVector
        encodedList.append(product.entries)
    return encodedList


def correctMessage74(encoded):
    G,H = BitMatrix.Generator(4)
    for group in encoded:
        groupVector = BitMatrix(group,1)
        product = H*groupVector
        if sum(product.entries) > 0:
            pass #FINISH
            
"""






def runHammingGeneral(message,n):
    # G,H = BitMatrix.Generator(n)
    # bitList = StringToBitList(message,n) -> convert each letter to a byte, groups bits by n
                ## uneven divisions like: n=5, '011 11010'
                ## add 0's AT THE FRONT: -> '00011 11010'
    # if n==4:
        # corruptedBitList = flipRandomBit(bitList)
        # print("Message with one random incorrect bit: ")
        # print(BitListToString(corruptedBitList) ,'\n')
        # dataToEncode = corruptedBitList
    # else:
        # dataToEncode = bitList
        
    ## encode:
    #encodedList = []
    #for bitgroup in dataToEncode:
        #bitgroupEntries = [int(i) for i in group]
        #bitgroupVector = BitMatrix(bitgroupEntries,1)
        #product = G*bitgroupVector
        #encodedList.append(product.entries)
    #return encodedList
    
    # if n== 4:
        # wrongdata = encodedList
    # else:
        # wrongdata = flipRandomBit(encodedList)
        
    ## go through all groups and correct the wrong ones:
    # correctedList = []
    # for group in encoded:
        # bitgroupVector = BitMatrix(group,1)
        # syndromeVector = H*bitgroupVector
        # correctedVector = BitMatrix.correct(bitgroupVector,syndromeVector)
        # correctedList.append(correctedVector.entries)
        
    # output = BitListToString(correctedList,n)
            ## convert back to a string, start counting from behind to remove zeros added before
    # print(output)
    
    
    pass




""" ---------- RUNTIME ---------- """


print("This program takes a user-provided string, changes a random bit in the input, "
      "then corrects it using Hamming codes. \n")
running = True
while running:
    #print("Type 1 to use the Hamming(7,4) code "
    #      "or type 2 to use a Hamming code of specified length: ")
    print("In groups of how many bits should the data be split "
          "(ex. use 4 for Hamming(7,4))?: ")
    mode = input()
    try:
        n = int(mode)
    except ValueError:
        print("You did not input an integer! Try again: ")
    else:
        print("Input your message: ")
        message = input()
        runHammingGeneral(message,n)
        print("Do you wish to try another string? Input Y to go again, " 
              "input anything else to quit: ")
        replay = input()
        if replay not in ["Y","y"]:
            running = False
        
    






