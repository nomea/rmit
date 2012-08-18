'''
Created on Aug 3, 2012

@author: Aemon Murphy
'''
import enrol
import sys
import getopt
import os

def main(argv):
    data_dir = 'data'
    try:
        env_dir = os.environ['ENROLDIR']
        if os.path.exists(env_dir):
            data_dir = env_dir
    except KeyError:
        pass
    if os.path.exists(data_dir):
        e = enrol.Enrol(data_dir) 
        if argv:
            opts, args = getopt.getopt(argv, '', ['student='])
            for o, a in opts:
                if o == '--student':
                    report_student(e, a)
        else:
            report_subjects(e)
    else:
        print 'supplied data directory does not exist'
 
def report_student(e, student_id): 
    classes = e.check_student(student_id)
    for c in classes:
        print '{0:s} {1:35s} {2:s}'.format(get_subject_code(e, c),
                                get_subject_name(e, get_subject_code(e, c)),
                                get_class_time_venue(e, c))
        
def report_subjects(e):    
    for sb in e.subjects():
        print '{0:s} {1:35s} {2:4s} {3:4s}'.format(sb.get_code(), get_subject_name(e, sb.get_code()), get_no_classes(sb), get_no_students(sb))

def get_no_classes(subject):
    return str(len(subject.get_classes()))
    
def get_no_students(subject):
    students = 0
    for s in subject.get_classes():
        students += len(s.get_students())
    return str(students)
    
def get_subject_name(e, subject):
    for sb in e.subjects():
        if sb.get_code() == subject:
            return sb.get_name()

def get_subject_code(e, clss):
    return e.class_info(clss)[0]
        
def get_class_time_venue(e, clss):
    info = e.class_info(clss)
    return  info[1] + ' @ ' + info[2]
        
main(sys.argv[1:])
        