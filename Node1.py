from Parameters import *
from Passenger import *
from Feature import *
import math
import copy

"""
This class respresents a node of a decision tree.
Usage: node = Node(list_of_passengers)
node.isLeaf() returns whether the node is leaf.
"""
class Node1:
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
        survived, died = 0,0
        for p in self.passengers:
            if p.survived:
                survived += 1
            else:
                died += 1
        return float(survived) / (survived + died)

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
        # print features
        for i in range(len(features)):
            counter = 0
            branch1 = []
            branch2 = []
            for j in range(len(self.passengers)):
                p = self.passengers[j]
                f = features[i]
                result = p.split(f)
                if result:
                    branch1.append(copy.deepcopy(p))
                    #print f.thresholdValue, "branch1", p, result
                    counter+=1
                else:
                    branch2.append(copy.deepcopy(p))
                    #print f.thresholdValue, "branch2", p, result
            print "feature", f.thresholdValue, counter, self.getNumSamples(), (int(self.getNumSamples())-int(counter))
            a = (float(counter)/float(self.getNumSamples()))
            b = (float(float(self.getNumSamples())- float(counter))/float(self.getNumSamples()))
            entro_father = self.getEntropy(a,b)
            the_feature = f.thresholdValue

            surviving_counter1 = 0
            for pure in branch1:
                surviving = pure.survived
                if surviving:
                    surviving_counter1+=1
            #print surviving_counter1, float(len(branch1)),float(surviving_counter1),(float(len(branch1))-float(surviving_counter1))
            if surviving_counter1 == 0:#if there is 0 survivals ignore
                continue
            else:
                a_child_1 = (float(surviving_counter1)/float(len(branch1)))
                b_child_1 = (float(len(branch1))-float(surviving_counter1))/float(len(branch1))
            child_1_entro = self.getEntropy(a_child_1,b_child_1)


            surviving_counter2 = 0
            for impure in branch2:
                surviving2 = impure.survived
                if surviving2:
                    surviving_counter2+=1
            #print surviving_counter2, float(len(branch2)), float(surviving_counter2),(float(len(branch2))-float(surviving_counter2))
            if surviving_counter2 == 0:
                continue
            else:
                a_child_2 = (float(surviving_counter2)/float(len(branch2)))
                b_child_2 = (float(len(branch2))-float(surviving_counter2))/float(len(branch2))
            child_2_entro = self.getEntropy(a_child_2,b_child_2)

            average_entro_children = ((float(len(branch1))/float(self.getNumSamples()))*child_1_entro)+((float(len(branch2))/float(self.getNumSamples()))*child_2_entro)
            information_gain = (float(entro_father) - float(average_entro_children))

            return bestFeature

    @staticmethod
    def getEntropy(a,b):
        if a == 0 or b == 0:
            return 0
        return -(a*math.log(a) + b*math.log(b))


a = Node("1,0,3,Braund, Mr. Owen Harris,male,22,1,0,A/5 21171,7.25,,S", 0)
# b = a.split('fissal,11')
b = a.getBestFeature()
print b



