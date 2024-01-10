from django import forms
from . import models
from crispy_forms.helper import FormHelper

class FormSearch(forms.ModelForm):
    title = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True

    class Meta:
        model = models.Course
        fields = ('title',)

class FormCustomer(forms.ModelForm):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput())
    password = forms.CharField(
        max_length=150, label='password', widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='confirm', widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.TextInput())
    fullname = forms.CharField(
        max_length=200, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
                            'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))', 'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    address = forms.CharField(
        max_length=500, widget=forms.TextInput())

    class Meta:
        model = models.Customer
        exclude = ('reg_class',)

class FormCancel(forms.ModelForm):
    reason = forms.CharField(
        max_length=500, widget=forms.TextInput())

    class Meta:
        model = models.Cancel
        exclude = ('customer', 'reg_class',)

class FormNewsletter(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
            'type': 'text',
            'placeholder': 'Nhập email của bạn.',
            'name': 'news_email',
        }))

    class Meta:
        model = models.Newsletter
        fields = ('email', )

class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=150, label='Password', widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='Confirm', widget=forms.PasswordInput())

    class Meta():
        model = models.User
        fields = ('username', 'email', 'password')
       