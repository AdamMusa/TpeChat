from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile

admin.site.register(Profile)
admin.site.site_header = 'Diffusion administration'
