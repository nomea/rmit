import enrol

#Setup Data Files
fileSubjects = open("data/SUBJECTS", 'w')
fileSubjects.write('\
#subject_code:subject_name\n\
bw101:Introductory Basketweaving 1\n\
bw110:Introductory Basketweaving 2\n\
bw330:Underwater Basketweaving\n\
bw201:Baskets Throughout History\n\
bw340:Quantum Basketweaving\n\
bw232:Poststructuralist Basketweaving\n\
bw290:Non-Euclidean Basketweaving')
fileSubjects.close()

fileClasses = open("data/CLASSES", 'w')
fileClasses.write("\
#class_code:subject_code:time:venue_name:tutor_name\n\
bw101.1:bw101:Mon 9.30:2.5.10:Alice Chiswick\n\
bw101.2:bw101:Wed 14.30:2.6.1:Bob Turnham\n\
bw330A:bw330:Tue 15.30:23.5.32:Carlos Stamford\n\
bw110.1:bw110:Thu 8.30:2.6.1:Authur Bags")
fileClasses.close()

fileVenues = open("data/VENUES", 'w')
fileVenues.write("\
#venue_name:venue_capacity\n\
2.5.10:18\n\
2.5.11:18\n\
2.6.1:22\n\
23.5.32:50")
fileVenues.close()

f = open("data/bw101.1.roll", 'w')
f.write("\
#student_id\n\
s3300001\n\
s3300002\n\
s3300003\n\
s3300004")
f.close()

f = open("data/bw101.2.roll", 'w')
f.write("\
#student_id\n\
s3300005\n\
s3300006\n\
s3300007\n\
s3300008")
f.close()

f = open("data/bw330A.roll", 'w')
f.write("\
#student_id\n\
s3300009\n\
s3300010\n\
s3300011\n\
s3300012")
f.close()

f = open("data/bw110.1.roll", 'w')
f.write("\
#student_id\n\
s3300013\n\
s3300014\n\
s3300015\n\
s3300016")
f.close()

#try:
#    print enrol.read_lines("data/SUBJECTS")
#except IOError:
#    raise
    
#print enrol.read_lines("data/CLASSES")
#print enrol.read_lines("data/VENUES")
#
#print enrol.read_table("data/SUBJECTS")
#print enrol.read_table("data/CLASSES")
#print enrol.read_table("data/VENUES")

#print enrol.write_lines("data/SUBJECTS", ["bwm108:Intro to BoxMaking", "bw101:Introductory Basketweaving 1", "bw110:Introductory Basketweaving 2", "bw330:Underwater Basketweaving"])
#print enrol.write_lines("data/CLASSES", ["bw101.1:bw101:Mon 9.30:2.5.10:Aemon Murphy", "bw101.2:bw101:Wed 14.30:2.6.1:Bob Turnham", "bw330A:bw330:Tue 15.30:23.5.32:Carlos Stamford"])
#print enrol.write_lines("data/VENUES", ["2.5.10:18", "23.5.32:50"])
#
#print enrol.read_lines("data/SUBJECTS")
#print enrol.read_lines("data/CLASSES")
#print enrol.read_lines("data/VENUES")
#
#print enrol.read_table("data/SUBJECTS")
#print enrol.read_table("data/CLASSES")
#print enrol.read_table("data/VENUES")

e = enrol.Enrol('data')
print e.subject_name('bw101')
print e.classes('bw101')

e.enrol('s3300001', 'bw101.1')
e.enrol('s3300002', 'bw101.2')
e.enrol('s3300003', 'bw101.1')
e.enrol('s3300004', 'bw101.2')
e.enrol('s3300005', 'bw101.1')
e.enrol('s3300006', 'bw101.2')
e.enrol('s3300007', 'bw101.1')
e.enrol('s3300008', 'bw101.2')

print e.class_info('bw101.1')
print e.class_info('bw101.2')
print e.class_info('bw110.1')
print e.class_info('bw330A')
print e.check_student('s3300011')
print e.check_student('s3300001', 'bw101')

