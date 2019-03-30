from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import generics
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers as django_serializers
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.http import FileResponse, HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils import timezone
from notify.signals import notify
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.authtoken.models import Token
from .decorators import check_recaptcha, casual_required, intermediate_required,extreme_required, check_signup_completed, user_is_approved
from .filters import *
from .forms import *
from .models import *
from .serializers import *
import ast
import random
import os
import time

@api_view(['POST'])
def api_login(request, user=None):
    if not user:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Login Failed'}, status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'token': token.key,
        'code': user.code,
	    'referral_count': user.referral_count})


@api_view(['POST'])
def api_logout(request):
    id = request.data.get('id')
    if not id:
        return Response({'error': 'Invalid Request'}, status=HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(id=id)
        auth_token = user.auth_token
    except:
        return Response({'error': 'Invalid Request'}, status=HTTP_401_UNAUTHORIZED)

    user.auth_token.delete()
    return Response({'id': id, 'token': auth_token.key}, status=HTTP_200_OK)


@api_view(['POST'])
def api_get_auth_token(request):
    id = request.data.get('id')
    if not id:
        return Response({'error': 'Invalid Request'}, status=HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(id=id)
        auth_token = user.auth_token
    except:
        return Response({'error': 'Invalid Request'}, status=HTTP_401_UNAUTHORIZED)

    return Response({'id': id, 'token': auth_token.key}, status=HTTP_200_OK)




def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    stranger = True
    if user == request.user:
        stranger = False
    return render(request=request, template_name='user/user.html', context={'stranger': stranger})



def password_reset_form(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    else:
        return redirect('reset_password')

def password_reset_done(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    else:
        return render(request=request, template_name='registration/password_reset_done.html')



def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    else:
        return render(request=request, template_name='signup/signup.html')


def signup_casual(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    return render(request=request, template_name='signup/casual/guidelines.html')


@check_recaptcha
def signup_casual_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            if request.recaptcha_is_valid:
                user = userform.save()
                user.user_type = User.CASUAL
                user.save()
                casual = Casual(user=user)
                casual.save()
                no1 = random.randint(0, 9)
                no2 = random.randint(0, 9)
                no3 = random.randint(0, 9)
                no4 = random.randint(0, 9)
                s = str(user)
                length = len(s)
                code = ''
                if length > 1:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + s[1] + str(no3) + s[-2] + str(no4))
                else:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + str((no2+no1)%10) + str(no3) + str((no4+no3)%10) + str(no4))

                Referral.objects.create(user=user,referral_code=code)
                casual = Casual.objects.get(user=user)
                # trainee.code = code
                user.code = code
                username = userform.cleaned_data.get('username')
                raw_password = userform.cleaned_data.get('password1')
                referral_code = userform.cleaned_data.get('referral_code')
                user.save()
                casual.save()
                if referral_code is not None:
                    # trainee.referral_code =referral_code
                    user.referral_code =referral_code
                    user.save()
                    # trainee.save()
                    referral_exists = Referral.objects.filter(referral_code = referral_code).exists()
                    if referral_exists:
                        referral = Referral.objects.get(referral_code = referral_code)
                        referral.referral_count = referral.referral_count + 1
                        referral.save()
                    # trainee_exists = Trainee.objects.filter(code = referral_code).exists()
                    # mentor_exists = Mentor.objects.filter(code = referral_code).exists()
                    # submentor_exists = SubMentor.objects.filter(code = referral_code).exists()
                    user_exists = User.objects.filter(code= referral_code).exists()
                    # if trainee_exists:
                    #     trainees = Trainee.objects.get(code = referral_code)
                    #     trainees.referral_count = referral.referral_count
                    #     trainees.save()
                    # if mentor_exists:
                    #     mentors = Mentor.objects.get(code = referral_code)
                    #     mentors.referral_count = referral.referral_count
                    #     mentors.save()
                    # if submentor_exists:
                    #     submentors = SubMentor.objects.get(code = referral_code)
                    #     submentors.referral_count = referral.referral_count
                    #     submentors.save()
                    if user_exists:
                        users = User.objects.get(code = referral_code)
                        users.referral_count = referral.referral_count
                        users.save()


                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.success(request, 'User registered successfully')
                return redirect(reverse('signup_casual_profile'))
            else:
                userform.add_error(None, 'Invalid reCAPTCHA. Please try again.')
    else:
        userform = UserForm()
    return render(request=request, template_name='signup/casual/user.html', context={'userform': userform})


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_profile(request):
    user = request.user
    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES)
        if profileform.is_valid():
            user.bio = profileform.cleaned_data.get('bio')
            date_of_birth = request.POST.get('date_of_birth')
            image_upload = request.FILES.get('profile_picture', False)
            if image_upload:
                user.profile_picture = image_upload
            user.date_of_birth = date_of_birth
            user.save()
            return redirect(reverse('signup_casual_personality'))
    else:
        profileform = ProfileForm(instance=user)
    return render(request=request, template_name='signup/casual/profile.html', context={'profileform': profileform})


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_personality(request):
    return render(request=request, template_name='signup/casual/personality.html')


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_vat(request):
    return redirect(signup_casual_complete)
    # return render(request=request, template_name='signup/trainee/verbal_ability.html', context={'test_pk': 1})


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_vat_test(request, test_pk=1):
    return redirect(signup_casual_complete)
    # return render(request=request, template_name='signup/trainee/verbal_ability_test.html')


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_social(request):
    return redirect(signup_casual_complete)
    # return render(request=request, template_name='signup/trainee/social.html')


@login_required(login_url='login')
@check_signup_completed
@casual_required
def signup_casual_complete(request):
    user = request.user
    user.signup_completed = True
    user.save()
    x = casual.objects.get(user=user)
    return render(request=request, template_name='signup/casual/complete.html')

def signup_intermediate(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    return render(request=request, template_name='signup/intermediate/guidelines.html')

@check_recaptcha
def signup_intermediate_user(request):
    if request.user.is_authenticated:
        # print("hello 6")
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            if request.recaptcha_is_valid:
                user = userform.save()
                user.user_type = User.INTERMEDIATE

                user.save()
                intermediate = Intermediate(user=user)
                intermediate.save()
                no1 = random.randint(0, 9)
                no2 = random.randint(0, 9)
                no3 = random.randint(0, 9)
                no4 = random.randint(0, 9)
                s = str(user)
                length = len(s)
                code = ''
                if length > 1:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + s[1] + str(no3) + s[-2] + str(no4))
                else:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + str((no2+no1)%10) + str(no3) + str((no4+no3)%10) + str(no4))
                names = Names.objects.create(user = user,name = user.first_name+" "+user.last_name)
                Referral.objects.create(user=user,referral_code=code)
                intermediate = Intermediate.objects.get(user=user)
                # mentor.code = code
                user.code = code
                username = userform.cleaned_data.get('username')
                raw_password = userform.cleaned_data.get('password1')
                referral_code = userform.cleaned_data.get('referral_code')
                user.save()
                mentor.save()
                referral_exists = Referral.objects.filter(referral_code = referral_code).exists()
                if referral_code is not None:
                    # trainee.referral_code =referral_code
                    user.referral_code =referral_code
                    user.save()
                    # trainee.save()
                    referral_exists = Referral.objects.filter(referral_code = referral_code).exists()
                    if referral_exists:
                        referral = Referral.objects.get(referral_code = referral_code)
                        referral.referral_count = referral.referral_count + 1
                        referral.save()
                    # trainee_exists = Trainee.objects.filter(code = referral_code).exists()
                    # mentor_exists = Mentor.objects.filter(code = referral_code).exists()
                    # submentor_exists = SubMentor.objects.filter(code = referral_code).exists()
                    user_exists = User.objects.filter(code = referral_code).exists()
                 
                    if user_exists:
                        users = User.objects.get(code = referral_code)
                        users.referral_count = referral.referral_count
                        users.save()

                user = authenticate(username=username, password=raw_password)
                login(request, user)
                # print("hello 8")
                messages.success(request, 'User registered successfully')
                return redirect(reverse('signup_men_profile'))
            else:
                userform.add_error(None, 'Invalid reCAPTCHA. Please try again.')
    else:
        userform = UserForm()
    return render(request=request, template_name='signup/intermediate/user.html', context={'userform': userform})


@login_required(login_url='login')
@intermediate_required
def signup_intermediate_profile(request):
    user = request.user
    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES)
        if profileform.is_valid():
            user.bio = profileform.cleaned_data.get('bio')
            date_of_birth = request.POST.get('date_of_birth')
            image_upload = request.FILES.get('profile_picture', False)
            if image_upload:
                user.profile_picture = image_upload
            user.date_of_birth = date_of_birth
            user.save()
            return redirect(reverse('signup_intermediate_skills'))
    else:
        profileform = ProfileForm(instance=user)
    return render(request=request, template_name='signup/intermediate/profile.html', context={'profileform': profileform})


@login_required(login_url='login')
@intermediate_required
def signup_intermediate_skills(request):
    return redirect(signup_intermediate_account)
    # return render(request=request, template_name='signup/mentor/skills.html')


@login_required(login_url='login')
@intermediate_required
def signup_intermediate_account(request):
    user = request.user
    if request.method == 'POST':
        Intermediateform = IntermediateForm(request.POST)
        if Intermediateform.is_valid():
            intermediate = Intermediate.objects.get(user=user)
            intermediate.save()
            return redirect(reverse('signup_men_social'))
    else:
        intermediateform = IntermediateForm(instance=user)
    print(intermediateform)
    return render(request=request, template_name='signup/intermediate/account.html', context={'intermediateform': intermediateform})


@login_required(login_url='login')
@intermediate_required
def signup_intermediate_social(request):
    return redirect(signup_men_complete)
    # return render(request=request, template_name='signup/intermediate/social.html')


@login_required(login_url='login')
@intermediate_required
def signup_men_complete(request):
    request.user.signup_completed = True
    request.user.save()
    return render(request=request, template_name='signup/intermediate/complete.html')


@login_required(login_url='login')
def motivational_quote(request):

    quote = Quotes.objects.all()
    return render(request=request, template_name='quotes/next.html',
                      context={'quote':quote})
   



def signup_extreme(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    return render(request=request, template_name='signup/extreme/guidelines.html')

@check_recaptcha
def signup_extreme_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered as a valid user')
        return redirect(reverse('home'))
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            if request.recaptcha_is_valid:
                user = userform.save()
                user.user_type = User.EXTREME
                user.save()
                extreme = Extreme(user=user)
                print(Extreme.objects.count())
                extreme.save()
                print(Extreme.objects.count())
                no1 = random.randint(0, 9)
                no2 = random.randint(0, 9)
                no3 = random.randint(0, 9)
                no4 = random.randint(0, 9)
                s = str(user)
                length = len(s)
                code = ''
                if length > 1:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + s[1] + str(no3) + s[-2] + str(no4))
                else:
                    code = str(s[0] + str(no1) + s[-1] + str(no2) + str((no2+no1)%10) + str(no3) + str((no4+no3)%10) + str(no4))
                names = Names.objects.create(user = user,name = user.first_name+" "+user.last_name)
                Referral.objects.create(user=user,referral_code=code)
                extreme = Extreme.objects.get(user=user)
                # submentor.code = code
                user.code = code
                username = userform.cleaned_data.get('username')
                raw_password = userform.cleaned_data.get('password1')
                referral_code = userform.cleaned_data.get('referral_code')
                user.save()
                extreme.save()
                referral_exists = Referral.objects.filter(referral_code = referral_code).exists()
                if referral_code is not None:
                    # trainee.referral_code =referral_code
                    user.referral_code =referral_code
                    user.save()
                    # trainee.save()
                    referral_exists = Referral.objects.filter(referral_code = referral_code).exists()
                    if referral_exists:
                        referral = Referral.objects.get(referral_code = referral_code)
                        referral.referral_count = referral.referral_count + 1
                        referral.save()
                    # trainee_exists = Trainee.objects.filter(code = referral_code).exists()
                    # mentor_exists = Mentor.objects.filter(code = referral_code).exists()
                    # submentor_exists = SubMentor.objects.filter(code = referral_code).exists()
                    user_exists = User.objects.filter(code = referral_code).exists()
                    # if trainee_exists:
                    #     trainees = Trainee.objects.get(code = referral_code)
                    #     trainees.referral_count = referral.referral_count
                    #     trainees.save()
                    # if mentor_exists:
                    #     mentors = Mentor.objects.get(code = referral_code)
                    #     mentors.referral_count = referral.referral_count
                    #     mentors.save()
                    # if submentor_exists:
                    #     submentors = SubMentor.objects.get(code = referral_code)
                    #     submentors.referral_count = referral.referral_count
                    #     submentors.save()
                    if user_exists:
                        users = User.objects.get(code = referral_code)
                        users.referral_count = referral.referral_count
                        users.save()

                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.success(request, 'User registered successfully')
                return redirect(reverse('signup_extreme_profile'))
            else:
                userform.add_error(None, 'Invalid reCAPTCHA. Please try again.')
    else:
        userform = UserForm()
    return render(request=request, template_name='signup/extreme/user.html', context={'userform': userform})


@login_required(login_url='login')
@extreme_required
def signup_extreme_profile(request):
    user = request.user
    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES)
        if profileform.is_valid():
            user.bio = profileform.cleaned_data.get('bio')
            date_of_birth = request.POST.get('date_of_birth')
            image_upload = request.FILES.get('profile_picture', False)
            if image_upload:
                user.profile_picture = image_upload
            user.date_of_birth = date_of_birth
            user.save()
            return redirect(reverse('signup_extreme_skills'))
    else:
        profileform = ProfileForm(instance=user)
    return render(request=request, template_name='signup/extreme/profile.html', context={'profileform': profileform})


@login_required(login_url='login')
@extreme_required
def signup_extreme_skills(request):
    return redirect(signup_extreme_account)
    # return render(request=request, template_name='signup/mentor/skills.html')




@login_required(login_url='login')
@extreme_required
def signup_extreme_account(request):
    user = request.user
    if request.method == 'POST':
        extremeform = ExtremeForm(request.POST)
        if extremeform.is_valid():
            extreme = Extreme.objects.get(user=user)
            extreme.save()
            return redirect(reverse('signup_extreme_social'))
    else:
        extremeform = ExtremeForm(instance=user)
    print(extremeform)
    return render(request=request, template_name='signup/extreme/account.html', context={'extremeform': extremeform})


@login_required(login_url='login')
@extreme_required
def signup_extreme_social(request):
    return redirect(signup_extreme_complete)
    # return render(request=request, template_name='signup/mentor/social.html')


@login_required(login_url='login')
@extreme_required
def signup_extreme_complete(request):
    request.user.signup_completed = True
    request.user.save()
    return render(request=request, template_name='signup/extreme/complete.html')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if user.user_type == User.CASUAL:
        casual = Casual.objects.get(user=user)
        return render(request=request, template_name='dashboard/dashboard_casual.html',
                      context={'casual': casual, 'refcount':user.referral_count})
    elif user.user_type == User.INTERMEDIATE:
        intermediate = Intermediate.objects.get(user=user)
        return render(request=request, template_name='dashboard/dashboard_intermediate.html',
                      context={'intermediate': intermediate,'refcount':user.referral_count})

    elif user.user_type == User.EXTREME:
        extreme = Extreme.objects.get(user=user)
        
        return render(request=request, template_name='dashboard/dashboard_extreme.html',
                      context={'extreme': extreme,'refcount':user.referral_count})
    else:
        return render(request=request, template_name='dashboard/dashboard_moderator.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    score = 1
    queries = Query.objects.filter(query_author=user)
    answers = Answer.objects.filter(answer_author=user)
    return render(request=request, template_name='profile/profile.html',
                  context={'score': score, 'queries': queries, 'answers': answers})


@login_required(login_url='login')
def profile_settings(request):
    return render(request=request, template_name='settings/profile.html')


@login_required(login_url='login')
def account_settings(request):
    return render(request=request, template_name='settings/account.html')


@login_required(login_url='login')
def email_settings(request):
    return render(request=request, template_name='settings/email.html')


@login_required(login_url='login')
def notification_settings(request):
    return render(request=request, template_name='settings/notification.html')



@login_required(login_url='login')
def mod_settings(request):
    if request.user.user_type != User.MODERATOR:
        messages.error(request,
                       'This account does not have permission to access this page, please login with authorised account')
        return redirect('login')
    else:
        return render(request=request, template_name='moderator/settings.html')




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IntermediateViewSet(viewsets.ModelViewSet):
    queryset = Intermediate.objects.all()
    serializer_class = IntermediateSerializer


class ExtremeViewSet(viewsets.ModelViewSet):
    queryset = Extreme.objects.all()
    serializer_class = ExtremeSerializer

class CasualViewSet(viewsets.ModelViewSet):
    queryset = Casual.objects.all()
    serializer_class = CasualSerializer


class QuotesViewSet(viewsets.ModelViewSet):
    queryset = Quotes.objects.all()
    serializer_class = QuotesSerializer