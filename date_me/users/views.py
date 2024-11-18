from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from .forms import ProfileUserForm, RegistrationUserForm
from django.contrib import auth


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class=RegistrationUserForm
    success_url=reverse_lazy('users:profile')

    def form_valid(self, form):
        user=form.instance

        if user:
            form.save()
            auth.login(self.request,user)
        
        return HttpResponseRedirect(self.success_url)
    
    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context




class UserProfileView(UpdateView):  #добавить LoginRequiredMixin
    template_name = 'users/profile.html'
    form_class=ProfileUserForm
    success_url=reverse_lazy("users:profile")


    


