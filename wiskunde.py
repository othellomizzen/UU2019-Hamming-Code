#!/usr/bin/env python3
# Created on Mon May 27 22:15:35 2019
# author: Cassio da Silva Rodrigues, stundentnummer 5593565
import math


class breuk:
    
    def __init__(self,teller=0,noemer=1):
        #assume for the moment noemer!=0 , raise exception if so?
        self.teller,self.noemer = self.simplify(teller,noemer)
        
    def __str__(self):
        #should fractions with noemer=1 return just teller? 
        if self.noemer == 1:
            return str(self.teller)
        else:
            return str(self.teller) + '/' + str(self.noemer)
    
    def __float__(self):
        return float(self.teller/self.noemer)
    
    def __int__(self):
        return int(self.teller//self.noemer)

    def __add__(self,other):
        return self.add(self,other)
    
    def __mul__(self,other):
        return self.multiply(self,other)
    
    def __radd__(self,other):
        return self.__add__(other)
        
    def __rmul__(self,other):
        return self.__mul__(other)    
    
    def __sub__(self,other):
        if isinstance(other,breuk):
            temp = self.multiply(other,-1)
            result = self.add(self,temp)
        elif type(other) == int:
            result = self.add(self,-1*other)
        return result
    
    def __truediv__(self,other):
        temp = self.inverse(other)
        return self.multiply(self,temp)
    
    #for rsub and rtruediv, the operand order matters, so we do these manually:
    def __rsub__(self,other):
        temp = self.multiply(self,-1)
        return self.add(temp,other)
    
    def __rtruediv__(self,other):
        temp = self.inverse(self)
        return self.multiply(temp,other)
    
    def __lt__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller < temp2.teller
    
    def __le__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller <= temp2.teller
        
    def __gt__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller > temp2.teller
        
    def __ge__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller >= temp2.teller
        
    def __eq__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller == temp2.teller
        
    def __ne__(self,other):
        temp1,temp2 = self.samenoemer(self,other)
        return temp1.teller != temp2.teller
    
    def __neg__(self):
        result = breuk()
        result.teller,result.noemer = -self.teller,self.noemer
        return result
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        result = breuk()
        result.teller,result.noemer = abs(self.teller),self.noemer
        return result
    




    #the following methods perform calculations and return a breuk() object
    
    def multiply(self,first,second):
        #assume first is breuk, second may be either breuk or int
        if isinstance(second,breuk):
            resultTeller = first.teller*second.teller
            resultNoemer = first.noemer*second.noemer
        elif type(second) == int:
            resultTeller = second*first.teller
            resultNoemer = first.noemer
        result = breuk()
        result.teller,result.noemer = self.simplify(resultTeller,resultNoemer)
        return result
        
    def add(self,first,second):
        if isinstance(second,breuk):
            resultTeller = first.teller*second.noemer + second.teller*first.noemer
            resultNoemer = first.noemer*second.noemer
        elif type(second) == int:
            resultTeller = first.teller + second*first.noemer
            resultNoemer = first.noemer
        result = breuk()
        result.teller,result.noemer = self.simplify(resultTeller,resultNoemer)
        return result
    
    def inverse(self,first):
        #assume no floats
        result = breuk()
        if isinstance(first,breuk):
            result.teller,result.noemer = first.noemer,first.teller
        elif type(first) == int:
            result.teller,result.noemer = 1,first
        return result
    
    def samenoemer(self,first,second):
        #convert two breuk objects to share the same noemer; for comparisons
        if isinstance(second,breuk):
            temp = second
        elif type(second) == int:
            temp = breuk()
            temp.teller,temp.noemer = second,1
        result1,result2 = breuk(),breuk()
        result1.teller,result1.noemer = first.teller*temp.noemer,first.noemer*temp.noemer
        result2.teller,result2.noemer = temp.teller*first.noemer,temp.noemer*first.noemer
        return result1,result2
    
    def simplify(self,teller,noemer):
        #simplify returns a tuple and NOT a breuk object
        #otherwise you couldn't simplify a breuk on __init__ without infinite recursion
        gcd = math.gcd(teller,noemer)
        resultTeller = int(teller/gcd)
        resultNoemer = int(noemer/gcd)
        if resultNoemer < 0:
            resultTeller *= -1
            resultNoemer *= -1
        return resultTeller,resultNoemer
        



        
        
