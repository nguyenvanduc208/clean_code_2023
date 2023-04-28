from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import User


class SendEmail:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.content_subtype = "html"
        email.send()


class RequestEmail:
    def get_user(self, request, email=None):
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        current_site = get_current_site(request=request).domain
        relativeLink = reverse(
            "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        # Link to reset password
        absurl = "http://" + current_site + relativeLink
        context_data = {"user": user, "absurl": absurl}
        message = get_template("reset_password.html").render(context_data)
        data = {
            "email_body": message,
            "to_email": user.email,
            "email_subject": "Reset your password",
        }

        SendEmail.send_email(data)
