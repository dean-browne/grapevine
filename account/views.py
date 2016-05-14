"""

This is starting to get messy... In particular the register method
For now i might create some helper functions for the registser function
But I think it would be best to look into some class based view system

Need to test the key generation for users!

At the moment python anywhere seems to be having some issues with the most
recently uploaded code.. Perhaps the issue is on their side?? Who knows

"""

from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from grapevine import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from datetime import datetime

from cryptonic import hash_string
from .models import InviteKey
from home.models import Post


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
    return HttpResponseRedirect(reverse('home:index'))


"""
View for registration
Need to set this up so that it checks to see if the users key is valid
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
            new_user = User.objects.create_user(username=hashed_username,
                                            password=password)

            # Add the user to the user group
            group = Group.objects.get(name='users')
            group.user_set.add(new_user)

            user = authenticate(username=hashed_username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)

            return HttpResponseRedirect(reverse('home:index'))


        else:
            print "[-] Passwords don't match"
            error_message = "Passwords do not match!"
            return render(request, 'account/register.html', {'error_message': error_message})

    else:
        return render(request, 'account/register.html')



"""
    View for creating a invite key

"""
# TODO -> This function and the does_key_exist functions are core to the
# functionality of the site.. They will require a lot of testing
@login_required
def create_new_invite_key(request):
    key_generator = hash_string.InviteGenerator()
    generated_key = key_generator.generate_invite_key()
    invite_key_list = InviteKey.objects.filter(is_used=False)
    key_exists = does_key_exist(generated_key, invite_key_list)

    # Loop until the key is unique... This probably won't happen to often..
    # TODO Calculate the maximum number of keys if the keys and 16 bits and
    # see is it worth uppinng the keys to 32bit
    while key_exists:
        generated_key = key_generator.generate_invite_key()
        key_exists = does_key_exist(generated_key, invite_key_list)

    print "[+] Generated a new key: " + generated_key
    # TODO -> Check if some of these values are set automatically
    new_invite_key = InviteKey(invite_key=generated_key, is_used=False, created_by_id=request.user.id)
    new_invite_key.save()
    users_key_list = InviteKey.objects.filter(created_by_id=request.user.id, is_used=False)
    # invite_key_list was filtered to contain keys created by all users so had to create users_key_list and filter to contain only this users keylist
    return render(request, 'account/dash.html', {'generated_key': generated_key, 'invite_key_list': users_key_list})


"""
Helper function for create_new_invite_key.
@params: key_requested, key_list
Returns true if the key_requested already exists
Returns False if the key is unique
"""
def does_key_exist(key_requested, key_list):
    for key in key_list:
        if key_requested == key:
            print "[+] Trying to create key: " + key_requested + "\nKey already exists"
            return True
        else:
            print "[+] Unique Key created: " + key_requested
            return False

"""
View for: The Dashboard
Requires login
"""
@login_required
def dash(request):
    permission_list = request.user.get_all_permissions()
    # this does not seem to be filtering the way I would have liked
    invite_key_list = InviteKey.objects.filter(created_by_id=request.user.id, is_used=False)
    post_list = Post.objects.filter(user_id=request.user.id).order_by('-date')

    # Calculate the total votes
    total_votes = 0
    for post in post_list:
        total_votes += post.votes
    print "[+] User has %i", total_votes

    return render(request, 'account/dash.html', {'permission_list': permission_list, 'invite_key_list': invite_key_list, 'post_list': post_list, 'total_votes': total_votes})
