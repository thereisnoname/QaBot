from django.contrib import admin
from app.models import *

# for Django Admin app use
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Keyword)
admin.site.register(Tag)
admin.site.register(Log)