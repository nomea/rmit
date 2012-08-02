import enrol2

#Setup Data Files
fileSubjects = open("data/SUBJECTS", 'w')
fileSubjects.write('#subject_code:subject_name\n')
fileSubjects.write('bw101:Introductory Basketweaving 1\nbw110:Introductory Basketweaving 2\nbw330:Underwater Basketweaving')
fileSubjects.close()

fileClasses = open("data/CLASSES", 'w')
fileClasses.write('#class_code:subject_code:time:venue_name:tutor_name\n')
fileClasses.write("bw101.1:bw101:Mon 9.30:2.5.10:Alice Chiswick\nbw101.2:bw101:Wed 14.30:2.6.1:Bob Turnham\nbw330A:bw330:Tue 15.30:23.5.32:Carlos Stamford\nbw110.1:bw110:Thu 8.30:2.6.1:Authur Bags\n")
fileClasses.close()

fileVenues = open("data/VENUES", 'w')
fileVenues.write('#venue_name:venue_capacity\n')
fileVenues.write("2.5.10:18\n2.5.11:18\n2.6.1:22\n23.5.32:50")
fileVenues.close()

fileVenues = open("data/bw101.1.roll", 'w')
fileVenues.write('#student_id\n')
fileVenues.write("s3300001\ns3300002\ns3300003\ns3300004")
fileVenues.close()

fileVenues = open("data/bw101.2.roll", 'w')
fileVenues.write('#student_id\n')
fileVenues.write("s3300005\ns3300006\ns3300007\ns3300008")
fileVenues.close()

fileVenues = open("data/bw330A.roll", 'w')
fileVenues.write('#student_id\n')
fileVenues.write("s3300009\ns3300010\ns3300011\ns3300012")
fileVenues.close()

fileVenues = open("data/bw110.1.roll", 'w')
fileVenues.write('#student_id\n')
fileVenues.write("s3300013\ns3300014\ns3300015\ns3300016")
fileVenues.close()

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

e = enrol2.Enrol('data')
#print e.subjects()
#print e.subject_name('bw101')
#print e.classes('bw101')

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

