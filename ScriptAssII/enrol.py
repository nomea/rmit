'''
Created on 23/07/2012
@author: aemon murphy s3311114
'''
import os

#Names of source data files
SUBJECTSFILE = 'SUBJECTS'
CLASSESFILE = 'CLASSES'
VENUESFILE = 'VENUES'


def read_lines(filename):
    """Read file and return a list of all lines in the specified file."""
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
    """Read a colon-delimited file and return a list of lists."""
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
    """Select file to write to base on inputed filename variable. 
    
    Return 0 if exception raised by from _write_to_file.
    
    """
    try:
        if os.path.basename(filename) == SUBJECTSFILE:
            #The integer is the no. of delimiting colons to expect on each line
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
        #If a exception occurs while writing to the file return 0 instead of
        #raising exception
        return 0


def _write_to_file(filename, lines, fields):
    """Write a list of strings to the specified file. 
    
    Validate lines based on no. of fields expected in file 
    Overwrite file if exists.
    Return 0 if exception occurs.
    
    """
    try:
        f = open(filename, 'w')
        for i in range(len(lines)):
            #If the field count does not match the no. of fields expected
            #an IOError is raised to prevent data inconsistencies
            if lines[i].count(':') == fields:
                f.write(lines[i])
                if i < len(lines) - 1:
                    f.write('\n')
            else:
                raise IOError
    except IOError:
        raise                       


class Enrol(object):
    """ Main Class """
    data_dir = None
    subject_list = []
    class_list = []
    venue_list = []
    
    def __init__(self, data_dir):
        """ Read files and build Subject, Class and Venue objects """
        #Set data folder to supplied location
        self.data_dir = data_dir
        #Build venue, class and subject objects then add Students to their
        #classes
        for f in (os.listdir(data_dir)):
            if f == VENUESFILE:
                for fields in read_table(os.path.join(data_dir + '/' + f)):
                    en_venue = En_Venue(fields[0], fields[1])
                    self.venue_list.append(en_venue)
                    
        for f in (os.listdir(data_dir)):
            if f == CLASSESFILE:
                for fields in read_table(os.path.join(data_dir + '/' + f)):
                    en_class = En_Class(
                                        fields[0], 
                                        fields[1], 
                                        fields[2], 
                                        fields[4])
                    for v in self.venue_list:
                        if v.get_name() == fields[3]:
                            en_class.add_venue(v)         
                    self.class_list.append(en_class)  
                            
        for f in (os.listdir(data_dir)):
            if f == SUBJECTSFILE:
                for fields in read_table(os.path.join(data_dir + '/' + f)):
                    en_subject = En_Subject(fields[0], fields[1])
                    self.subject_list.append(en_subject) 
        
        #Set subject codes for classes           
        for sb in self.subject_list:
            class_list = []
            for c in self.class_list:
                if c.get_subject_code() == sb.get_code():
                    class_list.append(c)
            sb.add_classes(class_list)   
        
        #Add students to classes                         
        for f in (os.listdir(data_dir)):
            if f.endswith('.roll'):
                for c in self.class_list:
                    if f.startswith(c.get_code()):
                        c.add_students(read_lines(
                                                  os.path.join(
                                                  data_dir + '/' + f)))
                        
    def class_info(self, class_code):
        """ Return class information 
        
        Raise KeyError if class does not exist 
        
        """
        found = None
        for c in self.class_list:
            if c.get_code() == class_code:
                found = True
                return [c.get_subject_code(), 
                        c.get_time(),
                        c.get_venue_name(),
                        c.get_tutor(),
                        c.get_students()]
        if not found: 
            raise KeyError          

    def check_student(self, student_id, subject_code=None):
        """ Return list of class codes student is enrolled in 
        
        If subject code is specified, Return the class code that the students
        is enrolled in that subject. Return None if the student is not
        enrolled in the specified subject
        
        """
        class_list = []
        for c in self.class_list:
            for s in c.get_students():
                if subject_code:
                    if c.get_subject_code() == subject_code \
                                      and s == student_id:
                        class_list.append(c.get_code())
                else:
                    if s == student_id:
                        class_list.append(c.get_code())
        if class_list:
            return class_list
        else:
            return None
 
    def enrol(self, student_id, class_code): 
        """ Enrols student in selected class. 
        
        Check current number of students in class is less than venue capacity.
          
        
        """
        for subject in self.subject_list:
            if subject.get_class(class_code):
                clss = subject.get_class(class_code)
                #Check venue not full
                if clss.check_venue_space:
                    #Add student to class
                    clss.add_student(student_id)
                    #Compare classes and remove student if enrolled in another
                    #class in the same subject    
                    for subject_class in subject.get_classes():
                        if clss.get_subject_code() == \
                                subject_class.get_subject_code() and \
                                clss.get_code() != subject_class.get_code():
                            subject_class.remove_student(student_id)
            self._confirm_enrolment()
     
    def _confirm_enrolment(self):
        """ Update class files. """
        for c in self.class_list:
            write_lines(os.path.join(self.data_dir, c.get_code() + '.roll'),
                        c.get_students())
    
    def subjects(self):
        """ Return all subject codes in system """
        subjects = []
        for s in self.subject_list:
            subjects.append(s)
        return subjects

    def subject_name(self, subject_code):
        """ Return subject name. 
        
        If subject code does not exist raise KeyError
        
        """
        found = None
        for s in self.subject_list:
            if s.get_code() == subject_code:
                found = True
                return s.get_name()
        if not found:
            raise KeyError

    def classes(self, subject_code):
        """ Return a list of class codes for the specified subject. 
        
        If subject code does not exist raise KeyError
        
        """
        found = None
        classes = []
        for c in self.class_list:
            if c.get_subject_code() == subject_code:
                found = True
                classes.append(c.get_code())
        if found:
            return classes
        else:
            raise KeyError
                
#Class, Subject and Venue classes have been used to imporve modularisation 

class En_Class(object):
    """ Class Class """
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
        if self._get_student_count() < self._get_venue_capacity(): 
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
        if self._venue:
            return self._venue.get_name()
    
    def _get_venue_capacity(self):
        if self._venue:
            return self._venue.get_capacity()
    
    def _get_student_count(self):
        return len(self._students)

    def check_venue_space(self):
        if self._get_student_count < self._get_venue_capacity:
            return 1
        else:
            return 0

class En_Subject(object):
    """ Subject Class """
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
        
    def get_class(self, class_code):
        for clss in self._classes:
            if clss.get_code() == class_code:
                return clss

class En_Venue(object):
    """ Venue Class """
    _name = None
    _capacity = None

    def __init__(self, name, capacity):
        self._name = name
        self._capacity = capacity 
    
    def get_name(self):
        return self._name

    def get_capacity(self):
        return self._capacity

#no student class was used as a student only has an id. It seemed like a lot 
#of overhead for 1 data variable