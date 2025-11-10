import random

import string

from students.models import Students

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from decouple import config

from twilio.rest import Client

from django.utils import timezone

# import datetime





def generate_adm_num():

  while True :

    five_numbers = ''.join(random.choices(string.digits,k=5))

    adm_num = f'LM-{five_numbers}'

    if not Students.objects.filter(adm_num=adm_num).exists():

      return adm_num




def generate_password():

  password = ''.join(random.choices(string.ascii_lowercase+string.ascii_uppercase,k=5))

  return password


def sent_email(recepient,template,title,context):

  sender = config('EMAIL_HOST_USER')

  content = render_to_string(template,context)

  msg = EmailMultiAlternatives(from_email=sender,to=[recepient],subject=title)

  msg.attach_alternative(content,'text/html')

  msg.send()


def generate_otps():

  email_otp = ''.join(random.choices(string.digits,k=4))

  phone_otp = ''.join(random.choices(string.digits,k=4))

  return email_otp,phone_otp



def send_otp_sms(otp):

    account_sid = config('ACCOUNT_SID') 
    auth_token = config('AUTH_TOKEN')
    from_num = config('FROM_NUM')
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_=from_num,
                                     to='+919633769001',
                                     body=f'OTP for Verification : {otp}'
                                    )

  


def masking_email_and_phone(email,phone):

  username,domain = email.split('@')

  remaining_part_email = username[5:]

  remaining_part_phone = phone[-4:]

  masked_email = f'*****{remaining_part_email}@{domain}'

  masked_phone = f'******{remaining_part_phone}'

  return masked_email,masked_phone




def get_batch_code(course,start_date):

  month_codes = {1:'JAN',
                 2:'FEB',
                 3:'MAR',
                 4:'APR',
                 5:'MAY',
                 6:'JUN',
                 7:'JUL',
                 8:'AUG',
                 9:'SEP',
                 10:'OCT',
                 11:'NOV',
                 12:'DEC'}

  course_code = course.code 

  month = start_date.month

  year = start_date.year

  if month in month_codes :

    month_code = month_codes.get(month)

    return f'{course_code}-{month_code}-{year}'
  

def get_end_date(start_date):

  return start_date+timezone.timedelta(days=180)




  