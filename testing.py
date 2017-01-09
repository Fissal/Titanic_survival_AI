__author__ = 'fissalalsharef'


import pandas as pd
import numpy as np

"""data = [101, 4, 23, 8, 27, -3]
s1 = pd.Series(data)
# print s1

data1 = [101, 4.3, 5]
s1b = pd.Series(data1)
# print s1b

# print s1.values
# print s1b.values
# for i in range(4):
#     print s1.index[i]

# print np.log(10)

d = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
s4 = pd.Series(d)

for i, v in enumerate(s4):
    print i, v
"""



"""
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
"""



L = ['this',',', 'is\n', 'a\n',',', 'list\n', 'of\n', 'words\n']
X = [w.strip(',') for w in  L]

for x in X:
    if x == '':
        X.remove(x)

print X

