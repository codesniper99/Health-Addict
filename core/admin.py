from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Casual)
admin.site.register(Intermediate)
admin.site.register(Extreme)
admin.site.register(Referral)
admin.site.register(Quotes)