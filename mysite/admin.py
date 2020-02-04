from django.contrib import admin
from .models import User, Movies, MovieType

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    search_fields = ('UserName',)
    list_display = ('UserID', 'UserName',  'Age', 'Gender')
    fields = ['UserName', 'Password']


class MoviesAdmin(admin.ModelAdmin):
    search_fields = ('MovieName',)
    list_display = ("MovieID", "MovieName", "Hours", "Rating")


class MoviestypeAdmin(admin.ModelAdmin):
    search_fields = ("TypeName",)
    list_display = ("TypeName",)


admin.site.register(User, UserAdmin)
admin.site.register(Movies, MoviesAdmin)
admin.site.register(MovieType, MoviestypeAdmin)
