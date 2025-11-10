from django.shortcuts import render,redirect

# Create your views here.
from django.utils.decorators import method_decorator

from authentication.permissions import permitted_users

from django.views import View

from .forms import AddBatchForm

from crm.utils import get_batch_code,get_end_date



@method_decorator(permitted_users(['Admin','Sales']),name='dispatch')    
class AddBatchView(View):

    form_class = AddBatchForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        # print(request.user._meta.get_fields())

        data = {'form':form,'title':'Add Batch'}

        return render(request,'batch/add-batch.html',context=data)  

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            batch = form.save(commit=False)

            start_date = form.cleaned_data.get('start_date')

            batch_code = get_batch_code(batch.course,start_date)

            print(batch_code)

            end_date = get_end_date(start_date)

            print(end_date)

            batch.code = batch_code

            batch.end_date = end_date

            batch.save()

            form.save_m2m()

            return redirect('course-list')

        data = {'form':form}

        return render(request,'batch/add-batch.html',context=data)