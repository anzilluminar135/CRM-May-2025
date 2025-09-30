import random

import string

from students.models import Students



def generate_adm_num():

  while True :

    five_numbers = ''.join(random.choices(string.digits,k=5))

    adm_num = f'LM-{five_numbers}'

    if not Students.objects.filter(adm_num=adm_num).exists():

      return adm_num



