from django.contrib import admin
from .models import Prediction

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'disease', 'confidence', 'solution', 'image')
admin.site.register(Prediction, PredictionAdmin)