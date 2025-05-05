from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Құпия сөзді енгізіңіз',
        #   'class': 'form-control'  To add the css class to the field
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Құпия сөзді растау'
    }))

    class Meta:
        model = Account
        fields = ['аты_жөні', 'тегі', 'телефон_нөмірі', 'электрондық_пошта', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['аты_жөні'].widget.attrs['placeholder'] = 'Өз атыңызды енгізіңіз'
        self.fields['тегі'].widget.attrs['placeholder'] = 'Тегіңізді енгізіңіз'
        self.fields['телефон_нөмірі'].widget.attrs['placeholder'] = 'Телефон нөміріңізді енгізіңіз'
        self.fields['электрондық_пошта'].widget.attrs['placeholder'] = 'Электрондық пошта мекенжайыңызды енгізіңіз'
        for field in self.fields: 
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['аты_жөні', 'тегі', 'телефон_нөмірі']


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']
