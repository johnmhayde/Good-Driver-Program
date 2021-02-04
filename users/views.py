from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

# register new user with form input if form is valid
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}')
			return redirect('portal-home')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})
