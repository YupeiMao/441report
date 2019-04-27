from django.contrib import admin
from basic_app.models import UserProfileInfo,Company,Position,Review,DeleteID,EditID,Images,AddID,UserProperties
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(Review)
admin.site.register(DeleteID)
admin.site.register(EditID)
admin.site.register(Images)
admin.site.register(AddID)
admin.site.register(UserProperties)

from .models import Choice, Poll, Vote

# Register your models here.
admin.site.register(Choice)
admin.site.register(Poll)
admin.site.register(Vote)
