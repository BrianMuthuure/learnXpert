from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import UserSignUpForm
from .services import UserService
from .services import account_activation_token


class SignUp(View):
    form_class = UserSignUpForm
    template_name = "users/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = UserService.create_user(request, form)
            if user:
                return HttpResponse("Please confirm your email address to complete the registration")
        else:
            form = self.form_class()
        return render(request, self.template_name, {"form": form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        user = UserService.get_token_owner(uidb64)
        if user is not None and account_activation_token.check_token(user, token):
            account_activated = UserService.activate_user_account(request, user)
            if account_activated:
                messages.success(request, 'Your account have been confirmed.')
                return redirect('login')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('login')
