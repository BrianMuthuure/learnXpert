from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from ..users.models import User


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = TokenGenerator()


class UserService:
    @staticmethod
    def create_user(request, form):
        try:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # send email to user
            sent = UserService.send_email(request, user)
            return sent
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def send_email(request, user):
        # send email to user
        try:
            current_site = get_current_site(request)
            subject = "Activate Your LearnXpert Account"
            message = render_to_string(
                "users/activate_account.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                }
            )
            EmailMessage(subject, message, to=[user.email]).send(fail_silently=False)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_token_owner(uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    @staticmethod
    def activate_user_account(request, user):
        try:
            user.is_active = True
            user.email_verified = True
            user.save()
            login(request, user)
            return True
        except Exception as e:
            print(e)
            return False
