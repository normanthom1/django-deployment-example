from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
# if you ever need a view to need a login to be displayed you can use 'login_required'
# decorator.
from django.contrib.auth.decorators import login_required
# Create your views here.
# command to get to the home page
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')
# this needs to go directly above logout request,
# it means that if not logged in log out can not be seen.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# command to go to the registration page
def register(request):
    # assume no registered
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # grab the user form and save it to the database
            user = user_form.save()
            # hashes password
            user.set_password(user.password)
            # save hased password to the database
            user.save()
            # don not commit to data base duplicate users
            profile = profile_form.save(commit=False)
            # sets up a one to one relationship
            profile.user = user

            # check if profile p[ic was supplied/]
            # if it is there set it to user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            register = True
        # error message if user login does not work (puts a post but request is not valid)
        else:
            print(user_form.errors, profile_form.errors)
    # if request wasnt an http request (user didnt post anything)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form': profile_form,
                            'registered': registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user checks if authenticated
        user = authenticate(username=username, password=password)
        # check if user is activated
        if user:
            if user.is_active:
                # command logs in user
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            console.log('someone tried to login and failed')
            console.log('Username {}, and Password {}'.format(username, password))
            HttpResponse('Invalid username details supplied')

    else:
        return render(request, 'basic_app/login.html',{})
