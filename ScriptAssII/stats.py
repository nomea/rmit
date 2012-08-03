'''
Created on Aug 3, 2012

@author: Aemon Murphy
'''
import enrol
 
e = enrol.Enrol('data')
for s in e.get_subjects():
    print s.get_code() + ' : ' + s.get_name() + ' : ' + str(len(s.get_classes())) 