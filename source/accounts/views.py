from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from main.settings import HOST_NAME
from django.views.generic import UpdateView, DetailView, ListView

from accounts.forms import SignUpForm, UserChangeForm, UserChangePasswordForm, UserPasswordResetForm
from accounts.models import Token, Profile

def send_token(user, subject, message, redirect_url):
    token = Token.objects.create(user=user)
    url = HOST_NAME + reverse(redirect_url, kwargs={'token': token})
    print(url)
    try:
        user.email_user(subject, message.format(url=url))
    except ConnectionRefusedError:
        print('Could not send email. Server error.')


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'registration/login.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('webapp:index')


def register_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', context={'form': form})
    elif request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = User(
                 username=form.cleaned_data.get('username'),
                 first_name=form.cleaned_data.get('first_name'),
                 last_name=form.cleaned_data.get('last_name'),
                 email=form.cleaned_data.get('email'),
                 is_active=False
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            Profile.objects.create(user=user)
            token = Token.objects.create(user=user)

            activation_url = HOST_NAME + reverse('accounts:user_activate', kwargs={'token': token})
            print(activation_url)
            try:
                user.email_user(
                    'Вы зарегистрировались на сайте localhost:8000.',
                    'Для активации перейдите по ссылке: ' + activation_url
                )
            except ConnectionRefusedError:
                print('Could not send email. Server error.')

            return redirect('webapp:index')
        else:
            return render(request, 'register.html', context={'form': form})


def user_activate_view(request, token):
    token = get_object_or_404(Token, token=token)
    user = token.user
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('webapp:index')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_obj'
    form_class = UserChangeForm

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_change_password.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:login')


class UsersListView(ListView):
    template_name = 'registration/users.html'
    context_object_name = 'users'
    model = User
    paginate_by = 4
    paginate_orphans = 1


def password_reset_email_view(request):
    if request.method == 'GET':
        return render(request, 'password_reset_email.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            user = users[0]
            send_token(user,
                       'Вы запросили восстановление пароля на сайте localhost:8000.',
                       'Для ввода нового пароля перейдите по ссылке: {url}',
                       redirect_url='accounts:password_reset_form')
        return render(request, 'password_reset_confirm.html')


class PasswordResetFormView(UpdateView):
    model = User
    template_name = 'password_reset_form.html'
    form_class = UserPasswordResetForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        token = self.get_token()
        return token.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = self.kwargs.get('token')
        return context

    def form_valid(self, form):
        token = self.get_token()
        token.delete()
        return super().form_valid(form)

    def get_token(self):
        token_value = self.kwargs.get('token')
        return get_object_or_404(Token, token=token_value)

    def get_success_url(self):
        return reverse('accounts:login')


