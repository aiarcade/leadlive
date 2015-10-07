from django.db import models
import datetime

GENDER_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
    
)

class Batch(models.Model):
    name=models.CharField(max_length=200)
    start_date=models.DateField(verbose_name='Started Date (dd/mm/yy)')
    end_date=models.DateField(verbose_name='Finishing Date (dd/mm/yy)')
    status=models.CharField(max_length=10,default='Live')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Batches"
        verbose_name="Batch"
    def getName(self):
        return self.name
        

class Staff(models.Model):
    emp_no=models.CharField(max_length=20)
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=1)
    address=models.CharField(max_length=200)
    emergency_phone_no=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    education_history=models.CharField(max_length=200)
    joined_date=models.DateField('joined_date')
    emp_type=models.CharField(max_length=20)
    teaching_experience=models.CharField(max_length=5,null=True)
    industrial_experience=models.CharField(max_length=5,null=True)
    status=models.CharField(max_length=10,default='Live')
    def __unicode__(self):
        return self.name
    def shotName(self):
        _names=self.name.split(" ")
        if len(_names)>=2:
            _shot=_names[0][0]+_names[1][0]
        else:
            _shot=self.name[0:2]
        return _shot
    class Meta:
        verbose_name_plural = "Staffs"
        verbose_name="Staff"


class Student(models.Model):
    admission_no=models.CharField(max_length=20,verbose_name='Admission No')
    reg_no=models.CharField(max_length=20,null=True,verbose_name='University Reg No')
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=1)
    address=models.CharField(max_length=200)
    emergency_phone_no=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    parents=models.CharField(max_length=200)
    education_history=models.CharField(max_length=200)
    admitted_date=models.DateField(verbose_name='Admitted Date')
    status=models.CharField(max_length=10,default='Live')
    def __unicode__(self):
        return self.admission_no+'/'+self.name
    class Meta:
        verbose_name_plural = "Students"
        verbose_name="Student"

class BatchDivision(models.Model):
    name=models.CharField(max_length=200)
    batch=models.ForeignKey(Batch)
    students=models.ManyToManyField(Student)
    def __unicode__(self):
        return self.batch.name+'/'+self.name
    def getName(self):
        return self.batch.name+'/'+self.name



class Subject(models.Model):
    name=models.CharField(max_length=30)
    short_name=models.CharField(max_length=10)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Subjects"
        verbose_name="Subject"

class SubjectMap(models.Model):
    subject = models.ForeignKey(Subject)
    batch_div = models.ForeignKey(BatchDivision)
    staff=models.ForeignKey(Staff)
    status=models.CharField(max_length=10,default='Live')
    def mapName(self):
        return self.batch_div.batch.name+'-'+self.batch_div.name+'/'+self.subject.name
    def __unicode__(self):
        return  self.batch_div.batch.name+'-'+self.batch_div.name+'/'+self.subject.name
    def tmapName(self):
        return str(self.id)+'/'+self.staff.name+'/'+self.subject.short_name


class Attendance(models.Model):
    sub_map=models.ForeignKey(SubjectMap)
    student=models.ForeignKey(Student)
    date=models.DateField()
    slot_no=models.CharField(max_length=2)
    status_of_student = models.CharField(max_length=10)
    def __unicode__(self):
        return self.sub_map.mapName()
    class Meta:
        verbose_name_plural = "Attendance"
        verbose_name="Attendance"

class TimeTableSlots(models.Model):
    name=models.CharField(max_length=10)
    start_time=models.TimeField()
    end_time=models.TimeField()
    batch_div=models.ManyToManyField(BatchDivision)
    slot_no=models.CharField(max_length=2)
 
class TimeTable(models.Model):
    sid=models.CharField(max_length=100,null=True)
    sub_map=models.ForeignKey(SubjectMap)
    start_date_time=models.DateTimeField(null=True)
    end_date_time=models.DateTimeField(null=True)

class Mentorship(models.Model):
    name=models.CharField(max_length=200)
    batch=models.ForeignKey(Batch)
    staff=models.ForeignKey(Staff)	
    students=models.ManyToManyField(Student)
    def __unicode__(self):
        return self.batch.name+'/'+self.name
    def getName(self):
        return self.batch.name+'/'+self.name

class LeaveRequest(models.Model):
    student=models.ForeignKey(Student)
    start_date=models.DateTimeField(verbose_name='Started Date (dd/mm/yy)')
    end_date=models.DateTimeField(verbose_name='Finishing Date (dd/mm/yy)')
    session=models.CharField(max_length=10)	
    mentor=models.ForeignKey(Mentorship)
    reason=models.TextField()
    leave_status = models.CharField(max_length=10)	
    
class OdList(models.Model):
	staff=models.ForeignKey(Staff)
	date=models.DateField(verbose_name='Started Date (dd/mm/yyyy)')
	club=models.CharField(max_length=20)
	purpose=models.CharField(max_length=30)
	students=models.TextField()


# class Batch(models.Model):
#     name=models.CharField(max_length=200)
#     start_date=models.DateField('started_date')
#     end_date=models.DateField('end_date')
#     status=models.CharField(max_length=10)
#     currrent_semester=models.CharField(max_length=10)
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural = "Batches"
#         verbose_name="Batch"




# class Staff(models.Model):
#     emp_no=models.CharField(max_length=20)
#     name=models.CharField(max_length=200)
#     gender=models.CharField(max_length=1)
#     address=models.CharField(max_length=200)
#     emergency_phone_no=models.CharField(max_length=20)
#     mobile_no=models.CharField(max_length=20)
#     email=models.CharField(max_length=50)
#     education_history=models.CharField(max_length=200)
#     joined_date=models.DateField('joined_date')
#     emp_type=models.CharField(max_length=20)

#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural = "Staffs"
#         verbose_name="Staff"

# class Subject(models.Model):
#     name=models.CharField(max_length=30)
#     short_name=models.CharField(max_length=10)
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name_plural = "Subjects"
#         verbose_name="Subject"

# class SubjectMap(models.Model):
#     subject = models.ForeignKey(Subject)
#     batch = models.ForeignKey(Batch)
#     staff=models.ForeignKey(Staff)
#     def mapName(self):
#         return self.batch.name+'/'+self.staff.name+'/'+self.subject.name
#     def __unicode__(self):
#         return  self.batch.name+'/'+self.staff.name+'/'+self.subject.name

# class MentorShip(models.Model):
#     student= models.ForeignKey(Student)
#     staff=models.ForeignKey(Staff)
#     def __unicode__(self):
#         return self.staff.name+'->'+self.student.name
#     class Meta:
#         verbose_name_plural = "Mentor ship"
#         verbose_name="Mentor ship"

# #personal shedules - Person can add a schedule to their own calender
# class schedules(models.Model):
#     start_date_time=models.DateTimeField('start_date')
#     end_date_time=models.DateTimeField('end_date')
#     geo_location=models.CharField(max_length=50)
#     notify=models.CharField(max_length=5)
#     summary=models.CharField(max_length=200)
# #define an event type - ex: Lecture
# #popualted by admin
# class EventTypes(models.Model):
#     name=models.CharField(max_length=50)#Name of the event - lecture , vacation , celeberation ,etc

# #Timetable - based on calender , populated by admin
# #Each entry specify a  slot , that is a unique id to represent an event/schedule/lecture
# class TimeTable(models.Model):
#     sub_map=models.ForeignKey(SubjectMap)
#     start_date_time=models.DateTimeField()
#     end_date_time=models.DateTimeField()
#     def __unicode__(self):
#         return self.start_date_time.strftime("%d-%m-%Y")
#     class Meta:
#         verbose_name_plural = "Time Tables"
#         verbose_name="Time Table"



