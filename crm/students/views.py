from django.shortcuts import render,redirect

from django.views import View

from .models import Students,CourseChoices,BatchChoices,TrainerChoices

from .forms import AddStudentForm

from crm.utils import generate_adm_num,generate_password,sent_email

from django.db.models import Q

from course.models import Course

from trainer.models import Trainer

from batch.models import Batch

from authentication.models import Profile,OTP

from django.db import transaction

from decouple import config

import threading

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_users

# Create your views here.


# @method_decorator(login_required(login_url='login'),name='dispatch')
class DashboardView(View):

   
    def get(self,request,*args,**kwargs):

        data = {'title':'Dashboard'}

        return render(request,'students/dashboard.html',context=data)


@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')
class StudentListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        course = request.GET.get('course')

        batch = request.GET.get('batch')

        trainer = request.GET.get('trainer')

        students = Students.objects.filter(active_status=True)

        if query :

            students = students.filter(
                                        Q(first_name__icontains=query)|

                                        Q(last_name__icontains=query) |

                                        Q(email__icontains=query) |

                                        Q(contact_num__icontains=query) |

                                        Q(education__icontains=query) |

                                        Q(address__icontains=query) |

                                        Q(place__icontains=query) |

                                        Q(district__icontains=query) |

                                        Q(pincode__icontains=query) |

                                        Q(course__icontains=query) |

                                        Q(batch__icontains=query) |

                                        Q(trainer__icontains=query) 

                                        )
        elif course:

            students = students.filter(course__name=course)  

        elif batch:

            students = students.filter(batch__name=batch)  

        elif trainer:

            students = students.filter(trainer__name=trainer)    
        

        data = {'title':'Students','students':students,
                'course_choices':Course.objects.all(),'query':query,
                'batch_choices':Batch.objects.all(),'trainer_choices':Trainer.objects.all(),
                'course':course,
                'batch':batch,
                'trainer':trainer}

        return render(request,'students/students-list.html',context=data)

@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')    
class StudentDetailsView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        data = {'title':'Student Details','student':student}

        return render(request,'students/student-details.html',context=data) 



# way to perform hard delete
# class StudentDeleteView(View):

#     def get(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         student = Students.objects.get(uuid=uuid)

#         student.delete()

#         return redirect('students-list')


# perform soft delete
@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        student.active_status = False

        student.save()

        return redirect('students-list')
    
@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')    
class AddStudent(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        # print(request.user._meta.get_fields())

        data = {'form':form,'title':'Add Student'}

        return render(request,'students/add-student.html',context=data)  

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                student=form.save(commit=False)

                adm_num = generate_adm_num()

                student.adm_num = adm_num

                email = form.cleaned_data.get('email')

                password = generate_password()

                print(password)

                profile = Profile.objects.create_user(username=email,password=password,role='Student')

                OTP.objects.create(profile=profile)

                student.profile = profile

                student.save()

                recepient = student.email

                template = 'email/credentials.html'

                site_link = config('SITE_LINK')

                context = {'username':student.email,'password':password,'name':f'{student.first_name} {student.last_name}','site_link':site_link}

                title = 'Login Credentials'

                thread = threading.Thread(target=sent_email,args=(recepient,template,title,context))

                thread.start()

                # sent_email(recepient,template,title,context)

                return redirect('students-list')
        
        data = {'form':form}

        return render(request,'students/add-student.html',context=data)

        # post_data = request.POST

        # first_name = post_data.get('first_name')

        # last_name = post_data.get('last_name')

        # adm_num = post_data.get('adm_num')

        # email = post_data.get('email')

        # contact_num = post_data.get('contact_num')

        # photo = request.FILES.get('photo')

        # dob = post_data.get('dob')

        # education = post_data.get('education')

        # address = post_data.get('address')

        # place = post_data.get('place')

        # district = post_data.get('district')

        # pincode = post_data.get('pincode')

        # course = post_data.get('course')

        # batch = post_data.get('batch')

        # trainer = post_data.get('trainer')

        # student = Students.objects.create(first_name=first_name,
        #                                   last_name=last_name,
        #                                   adm_num = adm_num,
        #                                   email=email,
        #                                   contact_num=contact_num,
        #                                   photo=photo,
        #                                   dob=dob,
        #                                   education=education,
        #                                   address=address,
        #                                   place=place,
        #                                   district=district,
        #                                   pincode=pincode,
        #                                   course=course,
        #                                   batch=batch,
        #                                   trainer=trainer)

@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')
class EditStudent(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        form = self.form_class(instance=student)

        data = {'form':form,'title':'Edit Student'}

        return render(request,'students/edit-student.html',context=data)   

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        form = self.form_class(request.POST,request.FILES,instance=student)

        if form.is_valid():

            form.save()

            return redirect('students-list')

        data = {'form':form}

        return render(request,'students/edit-student.html',context=data)    


