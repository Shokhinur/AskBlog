from django.contrib import admin
from .models import Poll


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['author', 'question', 'answer', 'created_date']
    list_filter = ['author']

admin.site.register(Poll, QuestionAdmin)
# Register your models here.
