import site
from django.contrib import admin
from django.conf.urls import url, include
from .views import AuthorView, LanguageView, UserView, BookView, PublisherView, EbookView,\
    BookInfoView, searchView , Book_approval, favoriteView, Subscription
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url('language_details',csrf_exempt(LanguageView.as_view())),
    url('author_details',csrf_exempt(AuthorView.as_view())),
    url('user_details',csrf_exempt(UserView.as_view())),
    url('book_details',csrf_exempt(BookView.as_view())),
    url('publisher_details',csrf_exempt(PublisherView.as_view())),
    url('favorite',csrf_exempt(favoriteView.as_view())),
    url('ebook',csrf_exempt(EbookView.as_view())),
    url('book_info',csrf_exempt(BookInfoView.as_view())),
    url('search_book',csrf_exempt(searchView.as_view())),
    url('subscription',csrf_exempt(Subscription.as_view())),
    url('approval',csrf_exempt(Book_approval.as_view())),

]