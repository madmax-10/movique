from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from nApp.models import Video, Genre
from django.urls import reverse

# Create your views here.
class index(TemplateView):
    template_name="index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"]=Genre.objects.all()
        context["videos"]=Video.objects.all()
        return context

def signin(request):
    if request.method=="POST":
        usrname=request.POST.get("your_name")
        paswrd=request.POST.get("your_pass")
        user=auth.authenticate(username=usrname,password=paswrd)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            return redirect("/signin/")
    else:
        return render(request,"signin.html")

def signup(request):
        if request.method=="POST":
            usrname=request.POST.get("name")
            uemail=request.POST.get("email")
            pswrd=request.POST.get("pass")
            repswrd=request.POST.get("re_pass")
            if pswrd==repswrd:
                if User.objects.filter(email=uemail).exists():
                    messages.info(request,"Email Already in Use")
                    return redirect("/signup/")
                elif User.objects.filter(username=usrname).exists():
                    messages.info(request,"Username Already in Use")
                    return redirect("/signup/")
                else:
                    user=User.objects.create_user(username=usrname,email=uemail,password=pswrd)
                    user.save()
                    messages.info(request,"Account Created")
                    return redirect("/signin/")
            else:
                messages.info(request,"Password Mismatch")
                return redirect("/signup/")
        else:
            return render(request,"signup.html")
        
def logout(request):
    auth.logout(request)
    return redirect("/")
    
class create(CreateView):
    model=Video
    fields=['title','desc','thumbnail','vidFile']
    template_name='create.html'

    def get_success_url(self):
        return reverse('video-detail',kwargs={'pk' : self.object.pk})
    
class detail(DetailView):
    model=Video
    template_name='detail.html'

class vidList(ListView):
    model=Video
    template_name="movieList.html"
    context_object_name="videos"
    paginate_by=3
    def get_queryset(self, *args, **kwargs):
        if (self.kwargs['filter']=="genre"):
            return Video.objects.filter(genres__name__icontains=(self.kwargs['text']))
        elif (self.kwargs['filter']=="search"):
            return Video.objects.filter(title__icontains=(self.kwargs['text']))
