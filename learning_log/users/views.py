from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout

def logout_view(resquest):
    logout(resquest)
    return HttpResponseRedirect(reverse('index'))
