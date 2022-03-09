from django.contrib import admin
from .models import Dep, UserDetail, Doc,Branches

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Doc)
admin.site.register(Branches)
admin.site.register(Dep)



