from django.contrib import admin

# Register your models here.

from .models import Candidates, Voters, Positions, Admin, Record

admin.site.register(Candidates)
admin.site.register( Voters)
admin.site.register( Positions)
admin.site.register( Admin)
admin.site.register(Record)