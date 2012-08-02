'''
Created on 23/07/2012

@author: nomea
'''
import os


SUBJECTSFILE = 'SUBJECTS'
CLASSESFILE = 'CLASSES'
VENUESFILE = 'VENUES'


def read_lines(filename):
    try:
        f = open(filename, 'r')
        my_list = []
        for line in f:
            if line[0] != '#':
                my_list.append(line.rstrip())      
        return my_list
    except IOError:
        raise IOError('file not found!')


def read_table(filename):
    try:
        f = open(filename, 'r')
        my_table = []
        for line in f:
            if line[0] != '#':
                my_table.append(line.rstrip().split(':'))
        return my_table        
    except IOError:
        raise IOError('file not found!')


def write_lines(filename, lines):
    try:
        if os.path.basename(filename) == SUBJECTSFILE:
            _write_to_file(filename, lines, 1)
            return 1
        elif os.path.basename(filename) == CLASSESFILE:
            _write_to_file(filename, lines, 4)
            return 1
        elif os.path.basename(filename) == VENUESFILE:
            _write_to_file(filename, lines, 1)
            return 1
        else:
            _write_to_file(filename, lines, 0)
            
    except IOError:
        return 0


def _write_to_file(filename, lines, fields):
    try:
        f = open(filename, 'w')
        for i in range(len(lines)):
            if lines[i].count(':') == fields:
                f.write(lines[i])
                if i < len(lines) - 1:
                    f.write('\n')
    except IOError:
        raise                       
    finally:
        f.close


class Enrol(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.classes_raw = None
        self.all_subjects = []
        self.all_classes = []
        self.sb_subject_name_lookup = {}
        self.cl_subject_lookup = {}
        self.cl_time_lookup = {}
        self.cl_venue_lookup = {}
        self.cl_tutor_lookup = {}
        self.cl_class_lookup = {}
        self.vn_capacity_lookup = {}
        self.rl_enrollments = {}
        self.enrollment_files = []
        
        for f in (os.listdir(data_dir)):
            if f == SUBJECTSFILE:
                for s in read_table(data_dir + '//' + f):
                    self.sb_subject_name_lookup[s[0]] = s[1]
                    self.all_subjects.append(s[0])
            elif f == CLASSESFILE:
                self.classes_raw = read_table(data_dir + '//' + f)
                for c in read_table(data_dir + '//' + f):
                    self.cl_subject_lookup[c[0]] = c[1]
                    self.cl_time_lookup[c[0]] = c[2]
                    self.cl_venue_lookup[c[0]] = c[3]
                    self.cl_tutor_lookup[c[0]] = c[4]
                    self.all_classes.append(c[0])
            elif f == VENUESFILE:
                for v in read_table(data_dir + '//' + f):
                    self.vn_capacity_lookup[v[0]] = v[1]
            if f.endswith('.roll'):
                self.enrollment_files.append(f)
        for r in self.enrollment_files:
            self.rl_enrollments[r.rstrip('.roll')] = read_lines(self.data_dir + '//' + r)
            print self.rl_enrollments
        for s in self.all_subjects:
            my_classes = []
            for c in self.classes_raw:
                if c[1] == s:
                    my_classes.append(c[0])
                    self.cl_class_lookup[c[1]] = my_classes  
                     
    def subjects(self):
        return self.all_subjects
    
    def subject_name(self, subject_code):
        return self.sb_subject_name_lookup[subject_code]
            
    def classes(self, subject_code):
        return self.cl_class_lookup[subject_code]

    def class_info(self, class_code):
        for c in self.all_classes:
            if class_code == c:
                return [self.cl_subject_lookup[class_code], 
                        self.cl_time_lookup[class_code], 
                        self.cl_venue_lookup[class_code], 
                        self.cl_tutor_lookup[class_code], 
                        self._get_students(class_code)]
            else:
                return None

    def check_student(self, student_id, subject_code=None):
        if subject_code:
            return self._get_students_classes(self.cl_class_lookup[subject_code], student_id)
        else:
            return self._get_students_classes(self.all_classes, student_id)
    
    def enrol(self, student_id, class_code): 
        try:
            self._check_class_code(class_code),
            if os.path.exists(self.data_dir +'/' + class_code + '.roll'):
                no_of_students = len(self._get_students(class_code))
                capacity = self._get_venue_capacity(self._get_venue_name(class_code))
                if  no_of_students < capacity:
                    for c in self.all_classes:
                        for s in self._get_students(c):
                            if s == student_id:
                                self.rl_enrollments[c].remove(student_id)
                        if c == class_code:
                            self.rl_enrollments[c].append(student_id)
                        self._confirm_enrollment(c)
        except KeyError:
            pass  
                 
    def _get_venue_name(self, class_code):
        return self.cl_venue_lookup[class_code]
    
    def _get_venue_capacity(self, venue_name):
        return self.vn_capacity_lookup[venue_name]
        
    def _get_students(self, class_code):
        return self.rl_enrollments[class_code] 
    
    def _check_class_code(self, class_code):
        found = None
        for c in self.all_classes:
            if c == class_code:
                found = True
        if found:
            return found
        else:
            raise KeyError
    
    def _get_students_classes(self, classes, student_id):
        my_classes = []
        for c in classes:
            try:
                for s in self.rl_enrollments[c]:
                    if s == student_id:
                        my_classes.append(c)
            except KeyError:
                #fix
                pass
        return my_classes

    def _confirm_enrollment(self, class_code):
        write_lines(self.data_dir + '//' + class_code + '.roll', self.rl_enrollments[class_code])

#class En_Class(object):
#self.class_code
#self.time
#self.venue
#self.tutor
#self.students

#class En_Subject(object):
#self.subject_code
#self.subject_name
#self.classes

#class En_Venue(object):
#self.name
#self.capacity

#class En_Student(object):
#self.student_id
