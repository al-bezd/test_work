from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django_registration import views

from mkblog_app.forms import PostAdminForm
from mkblog_app.models import Post
from mkblog_app.views import PostView
from .views import RegistrationForm
from django.contrib.auth.views import LoginView
urlpatterns=[
    path('registeraccount/',RegistrationForm.as_view(),name='registration_register'),
    path('mkblog/',login_required(PostView.as_view(template_name='mkblog/index.html')),name='mkblog'),
    path('login/',LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('auth_password_reset/', TemplateView.as_view(template_name='registration/password_reset_form.html'),
         name='auth_password_reset'),
    path('post/<str:pk>', DetailView.as_view(template_name="mkblog\detail.html", model=Post), name='detail_post'),

    path('activate/complete/',
         TemplateView.as_view(
             template_name='registration/activation_complete.html'
         ),
         name='django_registration_activation_complete'),
    # The activation key can make use of any character from the
    # URL-safe base64 alphabet, plus the colon as a separator.
    path('activate/<str:activation_key>/',
         views.ActivationView.as_view(),
         name='django_registration_activate'),
    path('register/$',
         views.RegistrationView.as_view(),
         name='django_registration_register'),
    path('register/complete/',
         TemplateView.as_view(
             template_name='registration/registration_complete.html'
         ),
         name='django_registration_complete'),
    path('register/closed/',
         TemplateView.as_view(
             template_name='registration/registration_closed.html'
         ),
         name='django_registration_disallowed'),



]







