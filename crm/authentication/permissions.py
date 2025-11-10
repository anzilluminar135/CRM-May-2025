# permitted_users(['Admin','Sales'])

from django.shortcuts import redirect

from django.contrib import messages


def permitted_users(roles):

    def decorator(fn):

        def wrapper(request,*args,**kwargs):

            if request.user.is_authenticated:

                if request.user.role in roles :

                    return fn(request,*args,**kwargs)
                
                else :

                    messages.error(request,'You have no Permission')

                    return redirect('dashboard')

            else :

                return redirect('login')
            
        return wrapper   

    return decorator 

