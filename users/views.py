from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, SponsorRegistrationForm, DriverUpdateFrom, SponsorUpdateForm, PasswordResetForm, PasswordChangeForm, PasswordUpdateForm, EditPointsForm, AcceptApplicationForm, EditPointsRateForm
from .models import GenericUser, Driver, Sponsor, Application, PointHist, Sponsorship
from django.contrib.auth.models import User
#from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login
from portal.models import UserEditInfo
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
import datetime
from portal.views import driverGet

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

def register_sponsor_P2P(request):
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
			#form['sponsor_company']=(Sponsor.objects.get(username=request.user.username).sponsor_company)
			form.save()
			new_sponsor = Sponsor.objects.get(username=form.cleaned_data.get('username'))
			new_sponsor.sponsor_company = Sponsor.objects.get(username=request.user.username).sponsor_company
			new_sponsor.save()
			# register info with user table and log them in
			user = User.objects.create_user(form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('password'))
			#login(request, user)
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


def update_driver_points(request):
	driver = Driver.objects.get(username=request.POST.get("driver_username"))
	if request.method == 'POST':
		driver_points_form = EditPointsForm(request.POST, instance=driver)
		if driver_points_form.is_valid():
			# update point hist
			points = driver_points_form.cleaned_data.get('points')
			reason = driver_points_form.cleaned_data.get('reason')
			pointhist = PointHist.objects.create()
			pointhist.username = driver.username
			pointhist.sponsor_username = Sponsor.objects.get(username = request.user.username).username
			pointhist.sponsor_company = Sponsor.objects.get(username = request.user.username).sponsor_company
			pointhist.date = date.today().strftime("%m/%d/%Y")
			pointhist.points = points
			pointhist.reason = reason
			pointhist.save()
			# update drive points in sponsorships
			sponsorship = Sponsorship.objects.get(driver = request.POST.get("driver_username"), sponsor_company=pointhist.sponsor_company)
			sponsorship.driver_points += points
			sponsorship.save()
			messages.success(request, f"Your Driver's account has been updated")
			return redirect('sponsor-home')

	context = {
		'driver_points_form' : driver_points_form,
		'driver' : driver
	}
	return render(request, 'users/edit_points.html' , context)

def update_driver_points_rate(request):
	driver = Driver.objects.get(username=request.POST.get("driver_username"))
	if request.method == 'POST':
		driver_points_form = EditPointsRateForm(request.POST, instance=driver)
		if driver_points_form.is_valid():
			## update driver points rate in sponsorships
			sponsorship = Sponsorship.objects.get(driver = request.POST.get("driver_username"), sponsor_company=Sponsor.objects.get(username=request.user.username).sponsor_company)
			#sponsorship.driver_points += points
			sponsorship.price_scalar = driver_points_form.cleaned_data.get('price_scalar')
			sponsorship.save()
			messages.success(request, f"Your Driver's account has been updated")
			return redirect('sponsor-home')

	context = {
		'driver_points_form' : driver_points_form,
		'driver' : driver
	}
	return render(request, 'users/edit_points.html' , context)

# view for editing sponsor profile information
def update_sponsor_info(request):
	if request.method == 'POST':
		sponsor = Sponsor.objects.get(username=request.user.username)
		sponsor_form = SponsorUpdateForm(request.POST, request.FILES, instance=sponsor)
		if sponsor_form.is_valid():
			sponsor_form.save()
			UserEditInfo.objects.create(username=sponsor.username, date = "Today", time = "")
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
	driver = driverGet(request.user)
	application = ''
	application = request.POST.get('application')

	if application != '' and application != None:
		if Application.objects.filter(driver=driver.username,sponsor_company=application).exists() == False:
			Application.objects.create(driver=driver.username,sponsor_company=application, status = "Pending")
			messages.success(request, f"Application submitted!")

	companies = []
	for sponsor in Sponsor.objects.all():
		if companies.count(sponsor.sponsor_company) < 1:
			companies.append(sponsor.sponsor_company)

	context = {
		'companies': companies
	}
	return render(request, 'users/application.html', context)

def accept_application(request):
	driver = Driver.objects.get(username=request.POST.get("driver_username"))
	if request.method == 'POST':
		accept_application_form = AcceptApplicationForm(request.POST)
		if accept_application_form.is_valid():
			# update application
			sponsor_company = Sponsor.objects.get(username=request.user.username).sponsor_company
			application = Application.objects.get(driver=driver.username, sponsor_company=sponsor_company)
			application.status = accept_application_form.cleaned_data.get('status')
			application.reason = accept_application_form.cleaned_data.get('reason')
			application.save()
			# save Sponsorship
			if accept_application_form.cleaned_data.get('status') == 'Accepted':
				sponsor = Sponsor.objects.get(username=request.user.username)
				sponsorship = Sponsorship.objects.create(sponsor_company=sponsor.sponsor_company, driver=driver.username)
				sponsorship.save()
			return redirect('sponsor-home')
	else:
		accept_application_form = AcceptApplicationForm()
	context = {
		'accept_application_form' : accept_application_form,
		'driver' : driver,
	}
	return render(request, 'users/accept_application.html', context)

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

def generate_driver_points_report(request):
	if request.method == 'POST':
		driver_username = request.POST.get("driver_username")
		sponsor_company = Sponsor.objects.get(username=request.user.username).sponsor_company
		if driver_username == "all":
			drivers = drivers = PointHist.objects.filter(sponsor_company=sponsor_company)
		else:
			drivers = drivers = PointHist.objects.filter(sponsor_company=sponsor_company, username=driver_username)
		driver_names = []
		driver_points = []
		for driver in drivers:
			if driver_names.count(driver.username) == 0:
				driver_names.append(driver.username)
		for driver in driver_names:
			points = Sponsorship.objects.get(sponsor_company=sponsor_company, driver=driver)
			driver_points.append(points)
		context = {
				'drivers' : drivers,
				'driver_points' : driver_points,
			}
		return render(request, 'portal/driver_points_report.html', context)
	sponsor_company = Sponsor.objects.get(username=request.user.username).sponsor_company
	context = {
		'sponsor_company' : sponsor_company,
	}
	return render(request, 'portal/generate_driver_points.html', context)
