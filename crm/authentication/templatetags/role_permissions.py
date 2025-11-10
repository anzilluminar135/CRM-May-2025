from django.template import Library


register = Library()


@register.simple_tag
def display_name(name):

    return name.upper()


# {% display_name 'Anzil Nazer' as name %}  used in html

# {% check_roles request 'Student,Admin' as allow%}

@register.simple_tag
def check_roles(request,roles):

    roles = roles.split(',')

    if request.user.is_authenticated and request.user.role in roles :

        return True
    
    return False

    