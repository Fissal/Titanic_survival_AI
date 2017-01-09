from DataReader import *
from Passenger import *
from Node import *
from Feature import *

passengers = DataReader.read('data2.csv')
print passengers

node = Node(passengers)
print node.bestFeature
print node.survivalProbability()
print node.isLeaf()
print node.branches[0].bestFeature
print node.branches[0].survivalProbability()
print node.branches[1].bestFeature
print node.branches[1].survivalProbability()



