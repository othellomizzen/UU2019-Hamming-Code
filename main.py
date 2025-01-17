#!/usr/bin/env python3
# Created on Fri Jun 21 13:35:03 2019
# author: Cassio da Silva Rodrigues, stundentnummer 5593565
from classes.BitMatrix import BitMatrix
import copy
import random
from datetime import datetime
random.seed(datetime.now())


""" This program has three modes; the user inputs a string, and either:
    - flip a random amount of bits of the raw data and display the corrupted data back as
        a text string, followed by using Hamming(7,4) to correct the corrupted message, or;
    - use a general Hamming code and corrupt->correct without displaying the wrong data as text.
    - add a parity bit, flip a random number of bits and parity check for errors
The reason for this is that I cannot think of a meaningful way to convert corrupted 
data back to text when not storing it as nibbles and using Hamming(7,4)

For the purposes of having a general Hamming code to correct data, the first option
is completely unnecessary. However, it is simply fun to see on the screen what the corrupted 
data would translate back into as text. 
See the end of this file for the runtime loop. """

def flipRandomBits(bitList,n,mode=None):
    # flip a single bits in a random amount of groups of a message
    # note: randint and sample generates numbers up to AND INCLUDING the upper bound
    # bitList is a list containing lists with the grouped bits:    
    howManyRandom = random.randint(1,len(bitList)-1)
    groupRandom = random.sample(range(0,len(bitList)),howManyRandom)
    bitRandom = []
    for i in range(0,howManyRandom):
        if n==4:
            if mode == "p":
                bitRandom.append(random.choice([0,1,2,3]))
            else:
                bitRandom.append(random.choice([2,4,5,6]))
        else:
            bitRandom.append(random.randint(0,len(bitList[0])-1))   
    flippedList = copy.deepcopy(bitList)
    for i in range(0,howManyRandom):
        flippedList[groupRandom[i]][bitRandom[i]] = (flippedList[groupRandom[i]][bitRandom[i]]+1)%2
    return flippedList,howManyRandom

def StringToBitList(message,n):
    # converts text message to a list of lists containing the binary conversion,
    # grouped into sublists of length n, to use for Hamming(...,n) codes
    wholeBinaryString = ''.join(format(ord(x), 'b').zfill(8) for x in message)    
    bitList = []
    amountExtrabits = len(wholeBinaryString)%n
    # when the groups do not divide evenly, add a number of 0s to the first group
    if amountExtrabits != 0:
        newrow = (n-amountExtrabits)*[0]
        newrow += [int(i) for i in wholeBinaryString[0:amountExtrabits]]
        bitList.append(newrow)
    for k in range(0,len(wholeBinaryString)//n):
        bitList.append([int(i) for i in wholeBinaryString[amountExtrabits+ k*n:amountExtrabits+ (k+1)*n]])
    return bitList

def EncodedBitListToString(bitList,n):
    #convert a bitlist back to string
    wholeBinaryString = ''
    #add every bit minus the parity ones to a string:
    for group in bitList:
        for i in range(1,len(group)+1):
            if (i & (i - 1)) != 0:  #if i not a power of two, it is not a parity bit:
                wholeBinaryString += str(group[i-1])
    #now remove the added 0-bits from Stringtobitlist
    amountExtrabits = (n*len(bitList))%8
    if amountExtrabits != 0:
        wholeBinaryString = wholeBinaryString[amountExtrabits:]
    #now group by byte:
    byteList = []
    for i in range(0,len(wholeBinaryString)//8):
        byteList.append(wholeBinaryString[i*8:(i+1)*8])  
            
    return ''.join(chr(int(i,2)) for i in byteList)

def runHammingGeneral(message,n,mode=None):
    if mode == 'p':
        G,H = BitMatrix.ParityMatrices()
    else:
        G,H = BitMatrix.Generator(n)
    dataToEncode = StringToBitList(message,n) #-> convert each letter to a byte, groups bits by n
            # for uneven divisions like: n=5, '011 11010'
            # add 0's AT THE FRONT: -> '00011 11010'
    #encode:
    encodedList = []
    for bitgroup in dataToEncode:
        bitgroupEntries = [int(i) for i in bitgroup]
        bitgroupVector = BitMatrix(bitgroupEntries,1)
        product = G*bitgroupVector
        encodedList.append(product.entries)
    
    wrongdata,howManyRandom = flipRandomBits(encodedList,n,mode)
    print(howManyRandom, "bit(s) were corrupted.")
    if n== 4 and mode != 'p':
        print("Message after being corrupted: ")
        print(EncodedBitListToString(wrongdata,n) ,'\n')
            
    if mode == 'p':
        # Check how many errors have occured with parity check
        howManyWrong = 0
        for group in wrongdata:
            bitgroupVector = BitMatrix(group,1)
            syndromeVector = H*bitgroupVector
            if not all(bit == 0 for bit in syndromeVector.entries):
                howManyWrong += 1
        print(howManyWrong, 'bits were successfully detected as incorrect.')
    else:
        # go through all groups and correct the wrong ones:
        correctedList = []
        for group in wrongdata:
            bitgroupVector = BitMatrix(group,1)
            syndromeVector = H*bitgroupVector
            correctedVector = BitMatrix.correct(bitgroupVector,syndromeVector)
            correctedList.append(correctedVector.entries)
            
        # convert back to a string, also remove added 0s from StringToBitList
        output = EncodedBitListToString(correctedList,n) 
        print('Message after being corrupted and corrected: ')
        print(output, '\n')
    
    

""" ---------- RUNTIME ---------- """

print("This program takes a user-provided string, changes random bits in the input, "
      "then corrects it using Hamming codes. \n")
running = True
while running:
    print("Do you wish to add a parity bit or use Hamming codes? Input P for "
          "parity, input anything else for Hamming: ")
    parityMode = input()
    n = 4
    if parityMode != 'P' and parityMode != 'p':
        needInt = True
        while needInt:
            print("In groups of how many bits should the data be split "
              "(ex. use 4 for Hamming(7,4))?: ")
            hammingMode = input()
            try:
                n = int(hammingMode)
            except ValueError:
                print("You did not input an integer! Try again: ")
            else:
                needInt = False
    
    print("Input your message: ")
    message = input()
    start = datetime.now()
    runHammingGeneral(message,n,parityMode.lower())
    timedelta = datetime.now() - start
    print('Time elapsed:', timedelta.total_seconds()*1000,'milliseconds.')
    print("Do you wish to try another string? Input Y to go again, " 
          "input anything else to quit: ")
    replay = input()
    if replay not in ["Y","y"]:
        running = False
