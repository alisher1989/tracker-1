from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='Username')
    first_name = forms.CharField(max_length=100, required=False, label='First name')
    last_name = forms.CharField(max_length=100, required=False, label='Last name')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput,
                               label='Password')
    password_confirm = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput,
                               label='Password confirm')
    email = forms.EmailField(required=True, label='Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('Username is already taken.', code='username_taken')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('This email is already registered', code='registered_email')
        except User.DoesNotExist:
            return email

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match', code='password_do_not_match')
        if not (first_name or last_name):
            raise ValidationError('One of these First name or Last name fields should be filled')
        return self.cleaned_data


class UserChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    about_user = forms.CharField(required=False, label='About user', widget=forms.Textarea)
    git_profile = forms.URLField()

    def clean(self):
        super().clean()
        git_profile = self.cleaned_data.get('git_profile')
        git_link = 'https://github.com/'
        for i in git_profile:
            if i in git_link:
                raise ValidationError('no')
            return self.cleaned_data

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if not profile.avatar:
            profile.avatar = None
        if commit:
            profile.save()
        return profile

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        profile_fields = ['avatar', 'about_user', 'git_profile']


class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm']
