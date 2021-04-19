from django import forms
from .models import Driver, Sponsor, GenericAdmin, Application
from PIL import Image

# create a custom form for the Driver Model
class UserRegistrationForm(forms.ModelForm):
	username = forms.CharField(label = 'Username')
	first_name = forms.CharField(label = 'First Name')
	last_name = forms.CharField(label = 'Last Name')
	email = forms.EmailField()
	phone_num = forms.CharField(label = 'Phone Number')
	address = forms.CharField(label = 'Address')
	password = forms.CharField(label = 'Password')
	password2 = forms.CharField(label = 'Password Verification')
	security_question = forms.CharField(label = 'Password Recovery Security Question')
	security_answer = forms.CharField(label = 'Password Recovery Security Answer')

	# overwrite the clean for username and password validation
	def clean(self):
		cleaned_data = self.cleaned_data
		try:
			result = Driver.objects.get(username = cleaned_data.get('username'))
			if result != None:
				raise forms.ValidationError('A user already exists with that username')
		except Driver.DoesNotExist:
			pass
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Passwords Must Match')

		return cleaned_data
		# deliver the proper model to the database
	class Meta:
		model = Driver
		fields = ['username', 'first_name', 'last_name', 'phone_num', 'email', 'address', 'password', 'security_question', 'security_answer']

# Driver Registration Form
class SponsorRegistrationForm(forms.ModelForm):
		username = forms.CharField(label = 'Username')
		first_name = forms.CharField(label = 'First Name')
		last_name = forms.CharField(label = 'Last Name')
		email = forms.EmailField()
		sponsor_company = forms.CharField(label = 'Company Name')
		password = forms.CharField(label = 'Password')
		password2 = forms.CharField(label = 'Password Verification')
		security_question = forms.CharField(label = 'Password Recovery Security Question')
		security_answer = forms.CharField(label = 'Password Recovery Security Answer')

		# overwrite the clean for username and password validation
		def clean(self):
			cleaned_data = self.cleaned_data
			try:
				result = Sponsor.objects.get(username = cleaned_data.get('username'))
				if result != None:
					raise forms.ValidationError('A user already exists with that username')
			except Sponsor.DoesNotExist:
				pass
			password1 = cleaned_data.get('password')
			password2 = cleaned_data.get('password2')
			if password1 != password2:
				raise forms.ValidationError('Passwords Must Match')
			return cleaned_data

			# deliver the proper model to the database
		class Meta:
			model = Sponsor
			fields = ['username', 'first_name', 'last_name', 'email', 'sponsor_company', 'password', 'security_question', 'security_answer']
class AdminRegistrationForm(forms.ModelForm):
	username = forms.CharField(label = 'Username')
	first_name = forms.CharField(label = 'First Name')
	last_name = forms.CharField(label = 'Last Name')
	email = forms.EmailField()
	password = forms.CharField(label = 'Password')
	password2 = forms.CharField(label = 'Password Verification')

	# overwrite the clean for username and password validation
	def clean(self):
		cleaned_data = self.cleaned_data
		try:
			result = GenericAdmin.objects.get(username = cleaned_data.get('username'))
			if result != None:
				raise forms.ValidationError('A user already exists with that username')
		except GenericAdmin.DoesNotExist:
			pass
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError('Passwords Must Match')
		return cleaned_data

		# deliver the proper model to the database
	class Meta:
		model = GenericAdmin
		fields = ['username', 'first_name', 'last_name',  'email', 'password']

# form for Driver Editing profile
class DriverUpdateFrom(forms.ModelForm):
	model = Driver
	# deliver only editable content to the page
	class Meta:
		model = Driver
		fields = ['first_name', 'last_name', 'phone_num', 'email', 'address', 'profile_photo', 'security_question', 'security_answer']

# form for Sponsor Editing profile
class SponsorUpdateForm(forms.ModelForm):
	model = Sponsor
	# deliver only editable content to the page
	class Meta:
		model = Sponsor
		fields = ['first_name', 'last_name', 'email', 'sponsor_company', 'password', 'security_question', 'security_answer']

class ApplicationForm(forms.Form):
	sponsor = forms.ChoiceField(label="Select a sponsor from the list:", choices=[tuple([sponsor.username,sponsor.sponsor_company]) for sponsor in Sponsor.objects.all()])

class PasswordResetForm(forms.Form):
    username = forms.CharField(label = 'Username')

class PasswordChangeForm(forms.Form):
    #question = forms.CharField(label = 'Security Question')
    answer = forms.CharField(label = 'Security Answer')

class PasswordUpdateForm(forms.Form):
    password = forms.CharField(label = 'New Password')
    password2 = forms.CharField(label = 'Confirm Password')
