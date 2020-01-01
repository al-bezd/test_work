from django.contrib.messages import get_messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView

from mkblog_app.models import Post
from .forms import PostAdminForm
from django.views.generic.edit import FormView

class PostView(SuccessMessageMixin,FormView):
    form_class = PostAdminForm
    success_url = reverse_lazy("accounts:mkblog")
    success_message = "Post was created successfully"

    def get(self, request, *args, **kwargs):
        post_list = Post.objects.filter(enable=True)
        paginator = Paginator(post_list, 2)  # Show 25 contacts per page

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context=self.get_context_data()
        context['posts']=posts
        context['messages']=get_messages(request)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            author = form.save(commit=False)
            author.author = request.user
            author.enable = True
            author.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        #form.author=requests.user
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        #form.save({"author":})
        return super().form_valid(form)