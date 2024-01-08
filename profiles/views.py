from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.generic import FormView,CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from .forms import UserForm,DepositForm
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email_from_backend(user, sub, amount, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount
    })
    send_email = EmailMultiAlternatives(sub, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

class RegisterView(FormView):
    template_name = 'profiles/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            messages.success(self.request, 'User created successfully !!')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'profiles/login.html'

    def get_success_url(self):
        messages.success(self.request, 'User login successfully !!')
        return reverse_lazy('homepage')

class UserLogOutView(LogoutView):
    template_name = 'index.html'
    def get_success_url(self):
         if self.request.user.is_authenticated:
             logout(self.request)
         return  reverse_lazy('homepage')
    
class DepositView(LoginRequiredMixin,CreateView):
      template_name='profiles/deposit.html'
      login_url=reverse_lazy('user_login')
      def get(self, request, *args, **kwargs):

            form=DepositForm()
            return render(request, self.template_name,{'forms':form})

      def post(self, request, *args, **kwargs):
            form=DepositForm(request.POST)
            if form.is_valid():
                  amount=form.cleaned_data['deposit_amount']
                  user_profile=UserProfile.objects.get(user=request.user)
                  user_profile.balance+=amount
                  user_profile.save()
                  messages.success(request,f'Deposit money {amount} add successfully your current balance {user_profile.balance}')
                  send_email_from_backend(request.user, 'Deposit', amount, 'profiles/email_deposit.html')

                  return redirect('deposit')
            return render(request,self.template_name,{'form':form})