"""

Admin account currently doesn't work on the site as it is hashing the username
Easiest solution is to figure out what the hash of "Admin" is and then store that
in the database!


Need to test how we respond to the same user being registered twice!
"""

from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from grapevine import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from cryptonic import hash_string

"""
View for: Logging in
"""
def login(request):
    next = request.GET.get('next', '/')
    if request.method == "POST":
        username = request.POST['username']
        string_hasher = hash_string.StringEncryption(username)
        hashed_username = string_hasher.hashStringMd5()[0:-2]
        print "[+] Username: " + username + "\nHashed Username: " + hashed_username

        password = request.POST['password']
        user = authenticate(username=hashed_username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('Inactive User')

        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, 'account/login.html', {'redirect_to': next})


"""
View for: logging out
Requires login
"""
@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


"""
View for: The Dashboard
Requires login
"""
@login_required
def dash(request):
    permission_list = request.user.get_all_permissions()
    return render(request, 'account/dash.html', {'permission_list': permission_list})


"""
View for registration
Appears to be working
"""
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        # If the passwords match, hash the password and create the database user
        if password == repeat_password:
            print "[+] Passwowds match"
            string_hasher = hash_string.StringEncryption(username)
            hashed_username = string_hasher.hashStringMd5()[0:-2]

            # TODO just for testing
            print "[+] Username: " + username + "\nHashed Username: " + hashed_username

            # Check if the user already exists in the database
            if User.objects.filter(username=hashed_username).exists():
                error_message = "That username already exists"
                print "[+] Error: Username already exists!"
                return render(request, 'account/register.html', {'error_message': error_message})

            # Create the django user as normal but use the encrypted username
            user = User.objects.create_user(username=hashed_username,
                                            password=password)

            # Add the user to the user group
            group = Group.objects.get(name='users')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('home:index'))


        else:
            print "[-] Passwords don't match"
            return render(request, 'account/register.html')

    else:
        return render(request, 'account/register.html')
