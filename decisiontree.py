#!/usr/bin/python
# -*- coding: utf-8 -*-
          
import csv as csv 
import numpy as np
#from sklearn import tree

def create_numpy_array_from_csv(csv_file_path):
    csv_file_object = csv.reader(open('../../train.csv')) 
    header = next(csv_file_object) #Skip header.
    raw_data=[]
    for row in csv_file_object:
        raw_data.append(row)
        
    return (header, np.array(raw_data))

header, data = create_numpy_array_from_csv(csv_file_path='../../train.csv')

S = data[0::, 1:] #Cut out survived

# female=0, male=1
S[ (S[0::,2] == "female"), 2] = 0
S[ (S[0::,2] == "male"), 2] = 1

#Extract and encode title (from name)
title_dictionary = {}
title_id = 0
for row in S[:]:
    title = row[1].split(sep=',')[1].split(' ')[1].upper()
    if (title in title_dictionary):
        row[1] = title_dictionary[title]
    else:
        title_dictionary[title] = title_id
        row[1] = title_dictionary[title]
        title_id+=1

#Group age into child < 12, teen < 20, adult, senior >60
#Average marriage age for females: 22
mean_age = np.mean(S[ (S[0::,3] != ''), 3].astype(float))

mrs_code = title_dictionary['MRS.']
S[(S[0::,3] == '') & (S[0::,1] == str(mrs_code)), 3] = 22
S[ (S[0::,3] == ''), 3] = mean_age 
S[ (S[0::,3].astype(float) > 60), 3] = 0
S[ (S[0::,3].astype(float) <= 60), 3] = 1
S[ (S[0::,3].astype(float) < 20), 3] = 2
S[ (S[0::,3].astype(float) <= 12), 3] = 3

#Encode ticket
ticket_dictionary = {}
ticket_id = 0
for row in S[:]:
    ticket = row[6].split(' ')[0].upper()
    if ticket.isdigit():
        ticket = "N"
        
    if (ticket in ticket_dictionary):
        row[6] = ticket_dictionary[ticket]
    else:
        ticket_dictionary[ticket] = ticket_id
        row[6] = ticket_dictionary[ticket]
        ticket_id+=1

#Discreatize fare
mean_first_class = np.mean(S[ S[0::,0] == '1', 7].astype(float))
mean_second_class = np.mean(S[ S[0::,0] == '2', 7].astype(float))
mean_third_class = np.mean(S[ S[0::,0] == '3', 7].astype(float))

S[ (S[0::,7] == '0') & (S[0::,0] == '1'), 7] = mean_first_class
S[ (S[0::,7] == '0') & (S[0::,0] == '2'), 7] = mean_second_class
S[ (S[0::,7] == '0') & (S[0::,0] == '3'), 7] = mean_third_class

for row in S[:]:
    if (row[7].astype(float) <= 20):
        row[7] = 4
    elif (row[7].astype(float) <= 40):
        row[7] = 3
    elif (row[7].astype(float) <= 60):
        row[7] = 2
    elif (row[7].astype(float) <= 80):
        row[7] = 1
    elif (row[7].astype(float) > 80):
        row[7] = 0

#Encode cabin
cabin_dictionary = {}
cabin_id = 0
for row in S[:]:
    cabin = row[8]
    
    if (len(cabin)==0):
        cabin = 'U'
        
    cabin = cabin[0] #Just use the first character
    
    if (cabin in cabin_dictionary):
        row[8] = cabin_dictionary[cabin]
    else:
        cabin_dictionary[cabin] = cabin_id
        row[8] = cabin_dictionary[cabin]
        cabin_id += 1

# Q=0, C=1, S=2 for embarked.
S[ (S[0::,-1] == "Q"), -1] = 0
S[ (S[0::,-1] == "C"), -1] = 1
S[ (S[0::,-1] == "S"), -1] = 2

S[S=='']='0'

Y = data[0::, 0]

#decision_tree_classifer = tree.DecisionTreeClassifier()
#decision_tree_classifer = tree.DecisionTreeClassifier(max_depth = 4)
#decision_tree_classifer = tree.DecisionTreeClassifier(max_depth = 3, min_samples_leaf=50)
decision_tree_classifer = tree.DecisionTreeClassifier(max_depth = 3)
#decision_tree_classifer = tree.DecisionTreeClassifier(max_depth = 2)
decision_tree_classifer = decision_tree_classifer.fit(S, Y)

#Write the data out
test_file_obect = csv.reader(open('../../test.csv'))
header = next(test_file_obect)
open_file_object = csv.writer(open("../../Models/decisiontreemodel.csv", "w", newline=''))

for row in test_file_obect:
    row_formatted = np.array(row)
    # female=0, male=1
    if (row_formatted[2] == "female"):
        row_formatted[2] = 0
    else:
        row_formatted[2] = 1
    
    #Extract and encode title (from name)
    title = row_formatted[1].split(sep=',')[1].split(' ')[1].upper()
    if (title in title_dictionary):
        row_formatted[1] = title_dictionary[title]
    else:
        row_formatted[1] = -1
     
    #Group age into categories   
    if(row_formatted[3] == ''):
        if (row_formatted[1] == str(mrs_code)):
            row_formatted[3] = 22
        else:
            row_formatted[3] = mean_age 
        
    if(float(row_formatted[3]) <= 12):
        row_formatted[3] = 3
    elif(float(row_formatted[3]) < 20):
        row_formatted[3] = 2
    elif(float(row_formatted[3]) <= 60):
        row_formatted[3] = 1
    elif(float(row_formatted[3]) > 60):
        row_formatted[3] = 0

    #Encode ticket
    ticket = row_formatted[6].split(' ')[0].upper()
    if ticket.isdigit():
        ticket = "N"
        
    if (ticket in ticket_dictionary):
        row_formatted[6] = ticket_dictionary[ticket]
    else:
        row_formatted[6] = "-1"
    
    #Discreatize fare
    if ((row_formatted[7] == '0') or (row_formatted[7] == '')):
        if (row_formatted[0] == '1'):
            row_formatted[7] = mean_first_class
        elif (row_formatted[0] == '2'):
            row_formatted[7] = mean_second_class
        elif(row_formatted[0] == '3'):
            row_formatted[7] = mean_third_class
        
    if (row_formatted[7].astype(float) <= 20):
        row_formatted[7] = 4
    elif (row_formatted[7].astype(float) <= 40):
        row_formatted[7] = 3
    elif (row_formatted[7].astype(float) <= 60):
        row_formatted[7] = 2
    elif (row_formatted[7].astype(float) <= 80):
        row_formatted[7] = 1
    elif (row_formatted[7].astype(float) > 80):
        row_formatted[7] = 0
    
    #Encode cabin
    cabin = row_formatted[8]
    if (len(cabin)==0):
        cabin = 'U'
    cabin = cabin[0] #Just use the first character
    
    if (cabin in cabin_dictionary):
        row_formatted[8] = cabin_dictionary[cabin]
    else:
        row_formatted[8] = "-1"
    
    # Q=0, C=1, S=2 for embarked.
    if (row_formatted[-1] == "Q"):
        row_formatted[-1] = 0
    elif (row_formatted[-1] == "C"):
        row_formatted[-1] = 1
    else:
        row_formatted[-1] = 2
        
    row_formatted[ row_formatted == ''] = 0
    print(row_formatted)
    prediction = decision_tree_classifer.predict(row_formatted)
    #print(str(prediction[0]) + " % " + str(decision_tree_classifer.predict_proba(row_formatted)[0][0]))
    if prediction[0] == '1':
        row.insert(0,'1')
        open_file_object.writerow(row)
    else:
        row.insert(0,'0')
        open_file_object.writerow(row) 

for i,f in enumerate(header):
    print("%d => %s"%(i,f))
        
#output model as .dot        
with open("../../Models/decisiontree.dot", 'w') as f:
    f = tree.export_graphviz(decision_tree_classifer, out_file=f)
