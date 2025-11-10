from django.db import models

import uuid

# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class EducationChoices(models.TextChoices):

    SSLC = 'SSLC','SSLC'

    PLUS_TWO = 'Plus Two','Plus Two'

    DIPLOMA = 'Diploma','Diploma'

    DEGREE = 'Degree','Degree'

    POST_GRADUATION = 'Post Graduation','Post Graduation'

    DOCTORATE = 'Doctorate','Doctorate'

class DistrictChoices(models.TextChoices):

    THIRUVANANTHAPURAM = 'Thiruvananthapuram', 'Thiruvananthapuram'

    KOLLAM = 'Kollam', 'Kollam'

    PATHANAMTHITTA = 'Pathanamthitta', 'Pathanamthitta'

    ALAPPUZHA = 'Alappuzha', 'Alappuzha'

    KOTTAYAM = 'Kottayam', 'Kottayam'

    IDUKKI = 'Idukki', 'Idukki'

    ERNAKULAM = 'Ernakulam', 'Ernakulam'

    THRISSUR = 'Thrissur', 'Thrissur'

    PALAKKAD = 'Palakkad', 'Palakkad'

    MALAPPURAM = 'Malappuram', 'Malappuram'

    KOZHIKODE = 'Kozhikode', 'Kozhikode'

    WAYANAD = 'Wayanad', 'Wayanad'

    KANNUR = 'Kannur', 'Kannur'

    KASARAGOD = 'Kasaragod', 'Kasaragod'   

class CourseChoices(models.TextChoices):

    PYDJANGO = 'Py Django','Py Django' 

    MEARN = 'MEARN','MEARN'

    DS = 'Data Science','Data Science'

class BatchChoices(models.TextChoices):

    BATCH_1 = 'Batch 1','Batch 1'

    BATCH_2 = 'Batch 2','Batch 2'

    BATCH_3 = 'Batch 3','Batch 3'

    BATCH_4 = 'Batch 4','Batch 4'

class TrainerChoices(models.TextChoices):

    JOHN = 'John','John'  

    JAMES = 'James','James' 

    ALEX = 'Alex','Alex'    

class Students(BaseClass):

    '''

    first_name
    last_name
    adm_num
    email
    contact_num
    photo
    dob
    education
    address
    place
    district
    pincode
    course
    batch
    trainer
    join_date

    '''
    profile = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    first_name = models.CharField(max_length=25)

    last_name = models.CharField(max_length=25)

    adm_num = models.CharField(max_length=8)

    email = models.EmailField(unique=True)

    contact_num = models.CharField(max_length=13,unique=True)

    photo = models.ImageField(upload_to='students-photos')

    dob = models.DateField()

    education = models.CharField(max_length=15,choices=EducationChoices.choices)

    address = models.CharField(max_length=50)

    place = models.CharField(max_length=15)

    district = models.CharField(max_length=20,choices=DistrictChoices.choices)

    pincode = models.CharField(max_length=6)

    course = models.ForeignKey('course.Course',on_delete=models.CASCADE)

    batch = models.ForeignKey('batch.Batch',on_delete=models.CASCADE)

    trainer = models.ForeignKey('trainer.Trainer',on_delete=models.CASCADE)

    join_date = models.DateField(auto_now_add=True)  

   
    def __str__(self):

        return f'{self.first_name}-{self.last_name}-{self.adm_num}'
    
    class Meta :

        verbose_name = 'Students'

        verbose_name_plural = 'Students'
        