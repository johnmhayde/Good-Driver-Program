from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, SponsorRegistrationForm, DriverUpdateFrom, SponsorUpdateForm, ApplicationForm, PasswordResetForm, PasswordChangeForm, PasswordUpdateForm
from .models import GenericUser, Driver, Sponsor, Application
from django.contrib.auth.models import User
#from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login
from portal.models import UserEditInfo
from django.contrib.auth.hashers import make_password

# register new user with form input if form is valid
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			# save user info to GenericUser table
			new_user = GenericUser(
			username = form.cleaned_data.get('username'),
			password = form.cleaned_data.get('password'),
			type = "Driver"
			)
			new_user.save()
			# save user info to Driver table
			form.save()
			# register info with user table and log them in
			user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
			login(request, user)
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}')
			return redirect('driver-home')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})

def register_sponsor(request):
	if request.method == 'POST':
		form = SponsorRegistrationForm(request.POST)
		if form.is_valid():
			# save user info to GenericUser table
			new_user = GenericUser(
			username = form.cleaned_data.get('username'),
			password = form.cleaned_data.get('password'),
			type = "Sponsor"
			)
			new_user.save()
			# save user info to Driver table
			form.save()
			# register info with user table and log them in
			user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
			login(request, user)
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}')
			return redirect('sponsor-home')
	else:
		form = SponsorRegistrationForm()
	return render(request, 'users/register.html', {'form': form})

# view for editing driver profile information
def update_driver_info(request):
	if request.method == 'POST':
		driver = Driver.objects.get(username=request.user.username)
		driver_form = DriverUpdateFrom(request.POST, request.FILES, instance=driver)
		if driver_form.is_valid():
			driver_form.save()
			UserEditInfo.objects.create(username=driver.username, date = "Today", time = "")
			messages.success(request, f'Your account has been updated')
			return redirect('driver-home')
	else:
		driver = Driver.objects.get(username=request.user.username)
		driver_form = DriverUpdateFrom(instance=driver)
	context = {
		'driver_form' : driver_form
	}

	return render(request, 'users/edit_info.html', context)

# view for editing sponsor profile information
def update_sponsor_info(request):
	if request.method == 'POST':
		sponsor = Sponsor.objects.get(username=request.user.username)
		sponsor_form = SponsorUpdateForm(request.POST, request.FILES, instance=sponsor)
		if sponsor_form.is_valid():
			sponsor_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('sponsor-home')
	else:
		sponsor = Sponsor.objects.get(username=request.user.username)
		sponsor_form = SponsorUpdateForm(instance=sponsor)
	context = {
		'sponsor_form' : sponsor_form
	}

	return render(request, 'users/edit_sponsor_info.html', context)

def application(request):
	if request.method == 'POST':
		application_form = ApplicationForm(request.POST)
		if application_form.is_valid():
			sponsor = application_form.cleaned_data.get('sponsor')
			sponsor_company = Sponsor.objects.get(username=sponsor)
			application = Application.objects.create(driver=request.user.username, sponsor=sponsor, sponsor_company=sponsor_company.sponsor_company, status="Pending")
			application.save()
			return redirect('driver-home')
	else:
		application_form = ApplicationForm()
	context = {
		'application_form' : application_form,
	}
	return render(request, 'users/application.html', context)

def password_reset_request(request):
        if request.method == "POST":
                password_reset_form = PasswordResetForm(request.POST)
                if password_reset_form.is_valid():
                        try:
                                user = GenericUser.objects.get(username=password_reset_form.cleaned_data.get('username'))
                        except:
                                messages.error(request, f"Please input a valid username")
                                return redirect('password_reset')
                        userType = user.type
                        username = user.username
                        if(userType == 'Sponsor'):
                                user = Sponsor.objects.get(username=password_reset_form.cleaned_data.get('username'))
                        if(userType == 'Driver'):
                                user = Driver.objects.get(username=password_reset_form.cleaned_data.get('username'))
                        password_change_form = PasswordChangeForm()
                        context = {
                                'type' : userType,
                                'security_question' : user.security_question,
                                'security_answer' : user.security_answer,
                                'password_change_form' : password_change_form,
                        }
                        return redirect('password_reset_done', userType, username)
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="users/password_reset.html", context={"password_reset_form":password_reset_form})

def password_change_request(request, userType, username):
        if(userType == 'Sponsor'):
                user = Sponsor.objects.get(username=username)
        if(userType == 'Driver'):
                user = Driver.objects.get(username=username)
        if request.method == "POST":
                password_change_form = PasswordChangeForm(request.POST)
                if password_change_form.is_valid():
                        answer = password_change_form.cleaned_data.get('answer')
                        if(answer == user.security_answer): 
                                #uid = urlsafe_base64_encode(force_bytes(user.pk))
                                #token = default_token_generator.make_token(user)
                                return redirect('password_reset_confirm', user.username)
                                #return render(request, 'users/password_reset_confirm.html', contex
                        else:
                                messages.error(request, f"Incorrect Security Answer")
                                return redirect('password_reset_done', userType, username)
        password_change_form = PasswordChangeForm()
        context2 = {
                'security_question' : user.security_question,
                'password_change_form' : password_change_form,
        }
        return render(request, 'users/password_reset_done.html', context2)

def password_update_request(request, username):
    if request.method == "POST":
            user = User.objects.get(username=username)
            password_update_form = PasswordUpdateForm(request.POST)
            if password_update_form.is_valid():
                    answer = password_update_form.cleaned_data.get('password')
                    answer2 = password_update_form.cleaned_data.get('password2')
                    if (answer == answer2):
                            user.password = answer
                            user.password = make_password(answer)
                            user.save()
                            return render(request, 'users/password_reset_complete.html')
                    else:
                            messages.error(request, f"New passwords do not match. Please type in matching passwords")
                            return redirect('password_reset_confirm', username)
    password_update_form = PasswordUpdateForm()
    return render(request, 'users/password_reset_confirm.html', context={"password_update_form":password_update_form})
