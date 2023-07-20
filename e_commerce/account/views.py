from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
from django.views import View
from random import randint
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
	form_class = UserRegistrationForm
	template_name = 'account/register.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			random_code = randint(1000, 9999)
			send_otp_code(phone=form.cleaned_data['phone'], code=random_code)
			OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
			request.session['user_registration_info'] = {
				'phone_number': form.cleaned_data['phone'],
				'email': form.cleaned_data['email'],
				'full_name': form.cleaned_data['full_name'],
				'password': form.cleaned_data['password'],
			}
			messages.success(request, 'we sent you a code', 'success')
			return redirect('account:verify_code')
		return render(request, self.template_name, {'form':form})

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm 	
    
    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form':form})
    
    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)	
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create(
					phone_number=user_session['phone_number'],
					email=user_session['email'],
					full_name=user_session['full_name'],
					password=user_session['password']
				)
                code_instance.delete()
                messages.success(request, 'You Are Register.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'This Code is Not Right!', 'danger')
                return redirect('account:verify_code')
        return redirect('home:home')
    
class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'you logged out successfully', 'success')
		return redirect('home:home')


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'account/login.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'info')
				return redirect('home:home')
			messages.error(request, 'phone or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})
        
    