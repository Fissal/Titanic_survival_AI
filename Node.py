from Parameters import *
from Passenger import *
from Feature import *
import math
import copy
from string import whitespace
import string

"""
    This class represents a node of a decision tree.
    Usage: node = Node(list_of_passengers)
    node.isLeaf() returns whether the node is leaf.
"""
class Node:
    """
    Node constructor class.
    You may need to modify this function.
    Hint:	Adding an entropy criterion to stop splitting
    """
    def __init__(self, passengers, level=0):
        self.passengers = passengers
        self.level = level
        if self.level < MAX_DEPTH and len(passengers) > MIN_ITEMS:
            self.bestFeature = self.getBestFeature()
            self.split(self.bestFeature)

    """
    Returns whether this node has any branches.
    Three reasons not having any branches:
    (1. MAX_DEPTH, 2. MIN_ITEMS, 3. ENTROPY GAIN)
    """
    def isLeaf(self):
        if self.branches == None or len(self.branches) == 0:
            return True
        return False

    def survivalProbability(self):
        global survived
        survived, died = 0,0
        for p in self.passengers:
            if p.survived:
                survived += 1
                # print survived
            else:
                died += 1
        return float(survived) / (survived + died)
        # print survived

    """
    Returns number of passengers in this node.
    """
    def getNumSamples(self):
        return len(self.passengers)

    def getBranches(self):
        return self.branches

    def split(self, feature):
        branch1 = []
        branch2 = []
        for p in self.passengers:
            result = p.split(feature)
            if result:
                branch1.append(copy.deepcopy(p))
            else:
                branch2.append(copy.deepcopy(p))

        self.branches = (Node(branch1,self.level+1), Node(branch2,self.level+1))

    """
    This function finds the best feature which has the maximum entropy
    gain ratio.
    """


    def getBestFeature(self):
        bestFeature = None
        features = Feature.getAllFeatures()
        for i in range(len(features)):
            counter = 0
            Br_1 = [] # This is for Branch #1
            Br_2 = [] # This is for Branch #2
            for j in range(len(self.passengers)):
                p = self.passengers[j]
                f = features[i]
                Re = p.split(f)
                if Re:
                    Br_1.append(copy.deepcopy(p))
                    counter+=1
                else:
                    Br_2.append(copy.deepcopy(p))
            # print "feature:", f.thresholdValue, "how many numbers are true",counter,"are out of", self.getNumSamples(), "Rest = ",(int(self.getNumSamples())-int(counter))

            q = (float(counter)/float(self.getNumSamples()))
            w = (float(float(self.getNumSamples())- float(counter))/float(self.getNumSamples()))
            E_F = self.getEntropy(q,w) #Father's Entropy


            Sur_Co = 0
            for MAL in Br_1:
                 Sur = MAL.survived
                 if Sur:
                     Sur_Co += 1
            print "survived = ",float(Sur_Co),"are out of", float(len(Br_1)),"Rest = ",(float(len(Br_1))-float(Sur_Co))

            if Sur_Co == 0:
                   continue
            else:
                child_1_A = (float(Sur_Co)/float(len(Br_1)))
                child_1_B = (float(len(Br_1))-float(Sur_Co))/float(len(Br_1))
            Child_1 = self.getEntropy(child_1_A,child_1_B) #Entropy of Children

            ####################

            Sur_Co1 = 0
            for SAL in Br_2:
                Sur1 = SAL.survived
                if Sur1:
                    Sur_Co1+=1
            # print "survived = ",float(Sur_Co1),"are out of", float(len(Br_2)),"Rest = ",(float(len(Br_2))-float(Sur_Co1))
            if Sur_Co1 == 0:
                  continue
            else:
                  child_2_A = (float(Sur_Co1)/float(len(Br_2)))
                  child_2_B = (float(len(Br_2))-float(Sur_Co1))/float(len(Br_2))
            Child_2 = self.getEntropy(child_2_A, child_2_B) #Entropy of Children

            ####################

            average_Of_children = ((float(len(Br_1))/float(self.getNumSamples()))*Child_1)+((float(len(Br_2))/float(self.getNumSamples()))*Child_2) #The average of children's Entropy
            Gain_the_information = (float(E_F) - float(average_Of_children))
            bestFeature = Gain_the_information

        return bestFeature

    @staticmethod
    def getEntropy(a,b):
        if a == 0 or b == 0:
            return 0
        return -(a*math.log(a) + b*math.log(b))