from django.contrib import admin
from sre_parse import CATEGORIES
from unicodedata import category
from django.contrib.admin.sites import site
from .models import Book

# Register your models here. 
from Libsys.models import Language, Author, Book, Ebook, User, Publisher, BookInfo
class languageAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('lang_id', 'name', 'script', 'about')
      list_display_links=['lang_id']

class BookAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('book_id','name','author', 'language', 'publisher', 'book_file')
      raw_id_fields=['language', 'author', 'publisher']     
      search_fields=['author__name', 'language__name', 'name', 'category','publisher__pub_id'] 
      def author(self, obj):
            return "\n".join([author.author for author in obj.author.all()])
      def language(self, obj):
            return "\n".join([Lang.language for Lang in obj.language.all()])  

class AuthoAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('author_id', 'name', 'email_id', 'picture')
      list_display_links=['author_id']

class ebookAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('book_id', 'ebook', 'approval_status', 'book_location', 'uploaded_by')    
      search_fields=['ebook_id']

class userAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('user_id', 'first_name', 'email_id', 'mobile_no', 'subscription', 'created_on', 'updated_on',\
            'favorite', 'role')
      raw_id_fields=['favorite']
      def favorite(self, obj):
        return "\n".join([fav.favorite for fav in obj.favorite.all()])

class publisherAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('pub_id', 'name', 'contact_details')               


class BookInfoAdmin(admin.ModelAdmin):
      list_per_page = 20
      list_display=('book_name', 'hardCopy_id', 'isLent', 'lentTo')
      raw_id_fields=['lentTo']

# class UserRoleAdmin(admin.ModelAdmin):
#       list_per_page = 20
#       list_display=['user_role']







admin.site.register(Language, languageAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthoAdmin)
admin.site.register(Ebook, ebookAdmin)
admin.site.register(User ,userAdmin)
admin.site.register(Publisher ,publisherAdmin)
admin.site.register(BookInfo ,BookInfoAdmin)
# admin.site.register(UserRoles ,UserRoleAdmin)

