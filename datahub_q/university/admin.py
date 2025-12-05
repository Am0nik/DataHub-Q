from django.contrib import admin
from .models import UniversitySection, University, UniversityImage, Program, UniversityRanking

class UniversityImageInline(admin.TabularInline):
    model = University.gallery_images.through
    extra = 1

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    filter_horizontal = ("gallery_images", "sections")

admin.site.register(UniversityImage)
admin.site.register(UniversitySection)
admin.site.register(Program)
admin.site.register(UniversityRanking)
