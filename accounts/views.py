#from django.contrib.auth.models import User
from warnings import warn

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django_registration import signals
from django_registration.views import RegistrationView as BaseRegistrationView

from accounts.models import User

#from rest_framework import viewsets
#from .serializers import UserSerializer


REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')

class RegistrationForm(BaseRegistrationView):
    template_name='registration/registration_form.html'
    success_url=reverse_lazy('accounts:django_registration_activation_complete')

    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    def post(self, request, *args, **kwargs):
        context=dict()

        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            User.objects.get(email=email)
            context['error'] = '<strong>Ошибка</strong><br><span>%s</span>'%'Учетная запись с таким email уже существует'
        except User.DoesNotExist:
            if len(password)<8:
                context['error'] = '<strong>Ошибка</strong><br><span>%s</span>'%'Пароль не должен быть менее 8ми символов'
            else:
                new_user=User.objects.create_user(
                    email,email=email,password=password
                )
                new_user.is_active = False
                new_user.save()
                self.send_activation_email(new_user)
                #new_user = self.create_inactive_user(form)
                signals.user_registered.send(sender=self.__class__,
                                             user=new_user,
                                             request=self.request)
                #return new_user
                return HttpResponseRedirect(self.success_url)

        context['email']=email

        return render(request,self.template_name,context)
        #return new_user


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('accounts:mkblog'))
        else:
            context = self.get_context_data(**kwargs)

            return self.render_to_response(context)

    '''
    def register(self, form):
        new_user = self.create_inactive_user(form)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user
        '''

    def get_success_url(self, user):
        return ('registration_complete', (), {})

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=REGISTRATION_SALT
        )

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """
        scheme = 'https' if self.request.is_secure() else 'http'
        return {
            'scheme': scheme,
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request)
        }
    def attach_alternative(self, content, mimetype):
        """Attach an alternative content representation."""
        assert content is not None
        assert mimetype is not None
        self.alternatives.append((content, mimetype))

    def send_activation_email(self, user):
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user,
        })
        ctx_dict = {'activation_key': activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': context['site'],
                    'email': user.email}

        # Email subject *must not* contain newlines
        subject = ''.join( \
            render_to_string('registration/activation_email_subject.txt',
                             ctx_dict).splitlines())

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        text_content = render_to_string('registration/activation_email.txt',
                                        ctx_dict)
        try:
            html_content = render_to_string('registration/activation_email.html',
                                            ctx_dict)
        except:
            # If any error occurs during html preperation do not add html content
            # This is here to make sure when we switch from default backend to extended
            # we do not get any missing here
            html_content = None
            # XXX we should not catch all exception for this
            warn(
                'registration/activation_email.html template cannot be rendered. Make sure you have it to send HTML messages. Will send email as TXT'
            )

        msg = EmailMultiAlternatives(subject,
                                     text_content,
                                     from_email,
                                     [to_email])
        if html_content:
            msg.attach_alternative(html_content, "text/html")

        msg.send()

def homepage(request):
    return redirect(reverse_lazy("accounts:mkblog"))


