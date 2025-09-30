from django.shortcuts import render,redirect

from django.views import View

from .models import Students,CourseChoices,BatchChoices,TrainerChoices

from .forms import AddStudentForm

from crm.utils import generate_adm_num

from django.db.models import Q

# Create your views here.

class DashboardView(View):

    def get(self,request,*args,**kwargs):

        data = {'title':'Dashboard'}

        return render(request,'students/dashboard.html',context=data)


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

            students = students.filter(course=course)  

        elif batch:

            students = students.filter(batch=batch)  

        elif trainer:

            students = students.filter(trainer=trainer)    
        

        data = {'title':'Students','students':students,
                'course_choices':CourseChoices,'query':query,
                'batch_choices':BatchChoices,'trainer_choices':TrainerChoices,
                'course':course,
                'batch':batch,
                'trainer':trainer}

        return render(request,'students/students-list.html',context=data)
    
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
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        student.active_status = False

        student.save()

        return redirect('students-list')
    
class AddStudent(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form,'title':'Add Student'}

        return render(request,'students/add-student.html',context=data)  

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():

            student=form.save(commit=False)

            adm_num = generate_adm_num()

            student.adm_num = adm_num

            student.save()

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


