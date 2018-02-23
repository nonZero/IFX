from authtools.admin import UserAdmin
from django.contrib import admin

from . import models

admin.register(models.User, UserAdmin)
