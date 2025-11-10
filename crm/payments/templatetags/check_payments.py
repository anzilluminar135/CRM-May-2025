from django.template import Library

from payments.models import Payment

from django.utils import timezone


register = Library()

@register.simple_tag

def check_payment_obj_exists(request):

    student = request.user.students

    course = request.user.students.course

    exists = False

    if Payment.objects.filter(student=student,course=course).exists():

        exists = True

    return exists    


@register.simple_tag
def check_due_date(due_date):

    current_date = timezone.now().date()

    late = False

    if current_date > due_date :

        late = True

    return late    




    

