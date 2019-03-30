from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
import random

class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, style={'input_type': 'password'})
    referral_code = serializers.CharField(max_length=100, required=False)
    code = serializers.CharField(max_length=100, required=False)

    first_name = serializers.CharField(min_length=1,required=True)
    last_name = serializers.CharField(min_length=1, required=True)
    cigs_per_day= serializers.CharField(required= True)    
    cost_per_packet = serializers.CharField(required=True)
    started_since =serializers.CharField(required = True)
    class Meta:
        model = User
        fields = (
            'url','id', 'username', 'email', 'first_name', 'last_name', 'password', 'user_type', 'bio',
            'date_of_birth', 'profile_picture',  'is_approved', 'has_paid_subscription',
            'referral_code','code','referral_count','cigs_per_day','cost_per_packet','started_since',
        )
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined','code','referral_count')
        required = ('first_name', 'last_name','cigs_per_day','cost_per_packet','started_since',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   #user.save(....)
        no1 = random.randint(0, 9)
        no2 = random.randint(0, 9)
        no3 = random.randint(0, 9)
        no4 = random.randint(0, 9)
        # instance.username = validated_data.get('username', instance.username)
        username = user.username
        s = str(username)
        length = len(s)
        code = ''
        if length > 1:
            code = str(s[0] + str(no1) + s[-1] + str(no2) + s[1] + str(no3) + s[-2] + str(no4))
        else:
            code = str(s[0] + str(no1) + s[-1] + str(no2) + str((no2+no1)%10) + str(no3) + str((no4+no3)%10) + str(no4))

        Referral.objects.create(referral_code=code)
        user.code = code
        user.save()
        if user.referral_code is not None:
            referral_exists = Referral.objects.filter(referral_code = user.referral_code)
            if referral_exists:
                referral = Referral.objects.get(referral_code = user.referral_code)
                referral.referral_count = referral.referral_count + 1
                user_exists = User.objects.filter(referral_code = user.referral_code)
                if user_exists:
                    referred_user = User.objects.get(code = user.referral_code)
                    referred_user.referral_count = referral.referral_count
                    referred_user.save()
                    referral.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class CasualSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Casual.objects.all())
     
    class Meta:
        model = Casual
        fields='__all__'


class QuotesSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Quotes.objects.all())
    
    class Meta:
        model = Quotes
        fields='__all__'
    
class IntermediateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Intermediate.objects.all())
    class Meta:
        model = Intermediate
        fields='__all__'
    
    

class ExtremeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Extreme.objects.all())
    
    class Meta:
        model = Extreme
        fields='__all__'
    

