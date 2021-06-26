from django.contrib import admin
from .models import  Friends, Reports, Shouts, User

""" admin.site.register(Question)
admin.site.register(Answer) """

admin.site.register(User)
admin.site.register(Shouts)
admin.site.register(Friends)
admin.site.register(Reports)



# Register your models here.
