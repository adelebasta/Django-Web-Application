from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import MySignUpForm
from .models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin


class MySignUpView(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        #form.get_user().execute_after_login()  # Custom code
        return HttpResponseRedirect(self.get_success_url())



class MyUserListView(LoginRequiredMixin, generic.ListView):
    login_url = '/useradmin/login/'
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser-list.html'


class HomeBirthdayView(TemplateView):
    def get_context_data(self, **kwargs):
        myuser = self.request.user  # Class is User, not MyUser
        myuser_has_birthday_today = False
        if myuser.is_authenticated:  # Anonymous user cannot call has_birthday_today()
            myuser_has_birthday_today = myuser.has_birthday_today()

        context = super(HomeBirthdayView, self).get_context_data(**kwargs)
        context['myuser_has_birthday_today'] = myuser_has_birthday_today
        return context
