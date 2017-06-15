from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

from datetime import datetime

# использует cookie на стороне клиента
# def index(request, *args, **kwargs):
#     # тест работы cookie
#     # https://docs.djangoproject.com/en/1.8/topics/http/sessions/#using-sessions-in-views
#     # request.session.set_test_cookie()
#     category_list=Category.objects.all()
#     page_list=Page.objects.order_by("-views")[:5]
#     context_dict={"categories":category_list, "pages":page_list}
#     # Получаем кол-во посещений сайта.
#     # Используем функцию COOKIES.get(), чтобы получить cookie с кол-ом посещений.
#     # Если cookie существует, возвращаемое значение преобразуется в целое число.
#     visits=int(request.COOKIES.get("visits", "1"))
#     reset_last_visit_time=False
#     context_dict["visits"]=visits
#     responce = render(request, "rango/index.html", context_dict)
#     if "last_visit" in request.COOKIES:
#         last_visit=request.COOKIES["last_visit"]
#         last_visit_time=datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
#         # тест работы cookie
#         # if (datetime.now()-last_visit_time).seconds>5:
#         if (datetime.now()-last_visit_time).days>0:
#             visits=visits+1
#             reset_last_visit_time=True
#     else:
#         reset_last_visit_time=True
#         context_dict["visits"]=visits
#         responce=render(request, "rango/index.html", context_dict)
#     if reset_last_visit_time:
#         responce.set_cookie("last_visit", datetime.now())
#         responce.set_cookie("visits", visits)
#     return responce

# использует данные сессии
# использует cookie на стороне сервера
def index(request):
    category_list=Category.objects.order_by("-likes")[:5]
    page_list=Page.objects.order_by("-views")[:5]
    context_dict={"categories":category_list, "pages":page_list}
    visits=request.session.get("visits")
    if not visits:
        visits=1
    reset_last_visit_time=False
    last_visit=request.session.get("last_visit")
    if last_visit:
        last_visit_time=datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # if (datetime.now() - last_visit_time).days>1:
        if (datetime.now() - last_visit_time).seconds>5:
            visits=visits+1
            reset_last_visit_time=True
    else:
        reset_last_visit_time=True
    if reset_last_visit_time:
        request.session["last_visit"]=str(datetime.now())
        request.session["visits"]=visits
    context_dict["visits"]=visits
    responce=render(request, "rango/index.html", context_dict)
    return responce


def about(request, *args, **kwargs):
    context_dict={}
    visits=request.session.get('visits')
    if visits:
        context_dict["visits"]=int(visits)
    else:
        visits=0
        context_dict["visits"]=visits
    return render(request, "rango/about.html", context_dict)

def category(request, category_name_slug):
    context_dict={}
    try:
        category=Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category.name
        pages=Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
        context_dict["category_name_slug"]=category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, "rango/category.html", context_dict)

def add_category(request):
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form=CategoryForm()
    return render(request, "rango/add_category.html", {"form":form})

def add_page(request, category_name_slug):
    try:
        cat=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat=None
    if request.method=="POST":
        form=PageForm(request.POST)
        if form.is_valid():
            if cat:
                page=form.save(commit=False)
                page.category=cat
                page.views=0
                page.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form=PageForm()
    context_dict={"form":form, "category":cat}
    return render(request, "rango/add_page.html", context_dict)

def register(request):
    # тест работы cookie
    # if request.session.test_cookie_worked():
    #     print(">>>> TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if "picture" in request.FILES:
                profile.picture=request.FILES["picture"]
            profile.save()
            registered=True
        else:
            print(profile_form.errors, user_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render(request, "rango/register.html", {"user_form": user_form, "profile_form":profile_form, "registered": registered})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/rango/")
            else:
                HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponseRedirect("/rango/")
    else:
        return render(request, "rango/login.html", {})

@login_required
def like_category(request):
    cat_id=None
    if request.method=="GET":
        cat_id=request.GET["category_id"]
    likes=0
    if cat_id:
        cat=Category.objects.get(id=int(cat_id))
        if cat:
            likes=cat.likes+1
            cat.likes=likes
            cat.save()
    return HttpResponse(likes)

@login_required
def restricted(request):
    return render(request, "rango/restricted.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango/")
