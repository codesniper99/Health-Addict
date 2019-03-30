import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token



def media_path(instance, filename):
    return os.path.join(instance.__class__.__name__.lower(),
                        instance.__class__.__name__.lower() + '_' + str(instance.id), filename)


def course_picture_media_path(instance, filename):
    return os.path.join('course', str(instance), filename)


def lesson_media_path(instance, filename):
    return os.path.join('course', str(instance.module.course), str(instance.module), filename)


def exam_media_path(instance, filename):
    return os.path.join('course', str(instance.module.course), str(instance.module), str(instance), filename)


def exam_submission_media_path(instance, filename):
    return os.path.join('course', str(instance.exam.module.course), str(instance.exam.module), str(instance.exam),
                        'submissions', str(instance.user), filename)


def project_media_path(instance, filename):
    return os.path.join('project', str(instance), filename)


def project_picture_media_path(instance, filename):
    return os.path.join('project', str(instance), filename)


def project_submission_media_path(instance, filename):
    return os.path.join('project', str(instance.project), str(instance.user), filename)


def profile_media_path(instance, filename):
    return os.path.join('profile', str(instance), filename)


def query_media_path(instance, filename):
    return os.path.join('forum', 'query_' + str(instance.id), filename)


def answer_media_path(instance, filename):
    return os.path.join('forum', 'query_' + str(instance.query.id), 'answer', 'answer_' + str(instance.id), filename)

class User(AbstractUser):
    CASUAL = 1
    INTERMEDIATE = 2
    MODERATOR = 3
    EXTREME = 4
    USER_TYPES = (
        (CASUAL, 'Beginner'),
        (INTERMEDIATE, 'Regular user'),
        (MODERATOR, 'Moderator'),
        (EXTREME,'Abuser')
    )


    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    has_paid_subscription = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=2000, validators=[MinLengthValidator(100)], blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_media_path, default='default_profile_pic.jpg', blank=True, null=True)
    signup_completed = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=100,null=True,blank=True)
    referral_count = models.PositiveIntegerField(default=0,blank=True,null=True)
    code = models.CharField(max_length=100,blank=True,null=True)
    cigs_per_day = models.IntegerField(blank=True)
    cost_per_packet= models.IntegerField(null = True,blank=True)
    started_since=models.DateField(blank=True)
    def __str__(self):
        return self.username


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(self,sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Quotes(models.Model):

    quote=models.CharField(max_length=200,blank=True)
    quote_id=models.IntegerField(unique=True,blank=True)

    def __str__(self):
        return self.quote



class Intermediate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.get_full_name()

   


class Casual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.get_full_name()



class Extreme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.get_full_name()

    # def referral_code(self):


class Referral(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    referral_count = models.PositiveIntegerField(default=0,blank=True,null=True)
    referral_code = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.referral_code
