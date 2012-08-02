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
    finally:
        f.close

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
    finally:
        f.close


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
    data_dir = None
    subjects = []
    classes = []
    venues = []
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        for f in (os.listdir(data_dir)):
            if f == VENUESFILE:
                for v in read_table(os.path.join(data_dir + '/' + f)):
                    en_venue = En_Venue(v[0], v[1])
                    self.venues.append(en_venue)
                    
        for f in (os.listdir(data_dir)):
            if f == CLASSESFILE:
                for c in read_table(os.path.join(data_dir + '/' + f)):
                    en_class = En_Class(c[0], c[1], c[2], c[4])
                    for v in self.venues:
                        if v.get_name() == c[3]:
                            en_class.add_venue(v)         
                    self.classes.append(en_class)  
                            
        for f in (os.listdir(data_dir)):
            if f == SUBJECTSFILE:
                for s in read_table(os.path.join(data_dir + '/' + f)):
                    en_subject = En_Subject(s[0], s[1])
                    self.subjects.append(en_subject) 
                    
        for s in self.subjects:
            class_list = []
            for c in self.classes:
                if c.get_subject_code() == s.get_code():
                    class_list.append(c)
            s.add_classes(class_list)  
           
                                 
        for f in (os.listdir(data_dir)):
            if f.endswith('.roll'):
                for c in self.classes:
                    if f.startswith(c.get_code()):
                        c.add_students(read_lines(os.path.join(data_dir + '/' + f)))
        for c in self.classes:
            print c.get_code() 
                        
    def class_info(self, class_code):
        for c in self.classes:
            try:
                if c.get_code() == class_code:
                    return [c.get_subject_code(), 
                            c.get_time(),
                            c.get_venue_name(),
                            c.get_tutor(),
                            c.get_students()]
            except KeyError:
                raise           

    def check_student(self, student_id, subject_code=None):
        class_list = []
        for c in self.classes:
            for s in c.get_students():
                if subject_code:
                    if c.get_subject_code() == subject_code and s == student_id:
                        class_list.append(c.get_code())
                else:
                    if s == student_id:
                        class_list.append(c.get_code())
        if class_list:
            return class_list
        else:
            return None
 
    def enrol(self, student_id, class_code): 
        for s in self.subjects:
            for c in s.get_classes():
                if c.get_student_count() < c.get_venue_capacity():
                    for s in c.get_students():
                        if s == student_id:
                            c.remove_student(student_id)
                    if c.get_code() == class_code:
                        c.add_student(student_id)
            self._confirm_enrolment()
            
    def _confirm_enrolment(self):
        for c in self.classes:
            write_lines(os.path.join(self.data_dir, c.get_code() + '.roll'), c.get_students())


class En_Class(object):
    _code = None
    _subject_code = None
    _time = None
    _venue = None
    _tutor = None
    _students = []
    
    def __init__(self, code, subject_code, time, tutor):
        self._code = code
        self._subject_code = subject_code
        self._time = time
        self._tutor = tutor
        
    def add_venue(self, venue):
        self._venue = venue

    def add_students(self, students):
        self._students = students
        
    def add_student(self, student_id):
        self._students.append(student_id)    
        
    def remove_student(self, student_id):
        self._students.remove(student_id)
        
    def get_code(self):
        return self._code
    
    def get_subject_code(self):
        return self._subject_code
    
    def get_time(self):
        return self._time
    
    def get_venue(self):
        return self._venue
    
    def get_tutor(self):
        return self._tutor
    
    def get_students(self):
        return self._students
    
    def get_venue_name(self):
        return self._venue.get_name()
    
    def get_venue_capacity(self):
        return self._venue.get_capacity()
    
    def get_student_count(self):
        return len(self._students)


class En_Subject(object):
    _code = None
    _name = None
    _classes = []
    
    def __init__(self, code, name):
        self._code = code
        self._name = name 
    
    def get_code(self):
        return self._code

    def get_name(self):
        return self._name
    
    def add_classes(self, classes):
        self._classes = classes
        
    def get_classes(self):
        return self._classes
        

class En_Venue(object):
    _name = None
    _capacity = None

    def __init__(self, name, capacity):
        self._name = name
        self._capacity = capacity 
    
    def get_name(self):
        return self._name

    def get_capacity(self):
        return self._capacity
