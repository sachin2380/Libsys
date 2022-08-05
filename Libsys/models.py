from __future__ import unicode_literals
from datetime import timedelta
from distutils.command.upload import upload
import email
#from email.policy import default
from operator import truediv
from pickle import TRUE
from pyexpat import model
from sys import maxsize
from turtle import up
from unicodedata import category
from django.contrib.postgres.fields import JSONField
import json
import uuid
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import CharField
from .constants import *

#from Librarymanagement.Libsys.response import init_response


# Create your models here.
class Base(models.Model):
    ACTIVE = 0
    INACTIVE = 1

    STATUS_CHOICE = ((ACTIVE, 'Active'),
                     (INACTIVE, 'Inactive')
                     )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.SmallIntegerField(default=ACTIVE,
                                          choices=STATUS_CHOICE)
    class Meta:
        abstract = True

class languageManager(models.Manager):
    def add_language(self, name):
        language = self.create(**name)
        return language

    def get_langauge(self, lang_ids):
        language_obj = self.filter(lang_id__in=lang_ids)
        language_list=[]
        for langu in language_obj:
            language_dict={}
            language_dict['lang_id'] = langu.pk
            language_dict['name'] = langu.name
            language_dict['script'] = langu.script
            language_dict['about'] = langu.about
            language_list.append(language_dict)
        return language_list    



class Language(models.Model):
    lang_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    script = models.CharField(max_length=20)
    about = models.TextField()

    objects = languageManager()

    def __unicode__(self):
        return str(self.name)

class AuthorsManager(models.Manager):
    def add_author(self,name, picture): #, email_id, picture_url):
        author = self.create(**name) #=name, email_id=email_id ,picture=picture_url)
        return author

    def get_author_details(self, author_ids):
        #import pdb;pdb.set_trace()
        author_obj = self.filter(author_id__in=author_ids)
        authors=[]
        for author in author_obj:
            author_det={}
            author_det['name'] = author.name
            author_det['email_id'] = author.email_id
            author_det['author_id'] = author.pk
            #author_det['picture'] = author.picture.url
            authors.append(author_det)
        return authors          


class Author(Base):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=50, unique=True)
    picture = models.ImageField(upload_to='my_picture', blank=True)
    objects = AuthorsManager()


    def __unicode__(self):
        return str(self.name)

class PublisherManager(models.Manager):
    def add_publisher(self, name): #, contact_details):
        publisher = self.create(**name) #=name, contact_details=contact_details)
        return publisher

    def publisher_details(self, pub_ids) :
        publisher_obj = Publisher.objects.filter(pub_id__in=pub_ids)
        publisher_det=[]
        for publisher in publisher_obj:
            publisher_dic={}
            publisher_dic['pub_id'] = publisher.pk
            publisher_dic['name'] = publisher.name
            publisher_dic['contact_details'] = publisher.contact_details

            publisher_det.append(publisher_dic)
        return publisher_det


class Publisher(models.Model):
    pub_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_details= models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.name)

    objects = PublisherManager()    

class BookManager(models.Manager):
       
    def add_book(self, name, lang_obj, publisher, author, category, book_type, extra_det, book_file):
        book = self.create(name=name, publisher=publisher, category=category, book_type=book_type, extra_det=extra_det, book_file=book_file)
        #book.publisher = publisher
        book.language.add(lang_obj)
        book.author.add(author)
        return book

    def get_book_details(self,book_id):
        book_obj = self.prefetch_related("language", 'author').select_related("publisher").filter(book_id__in=book_id)
        book_det=[]
        for book in book_obj:
            book_dic={}
            book_dic['book_id']=book.pk
            book_dic['name']=book.name
            book_dic['language'] = book.language.name
            book_dic['author'] = book.author.name
            book_dic['publisher'] = book.publisher.name
            book_dic['category']=book.category
            book_dic['book_type']=book.book_type
            book_dic['extra_det'] = book.extra_det
            book_dic['book_file'] = book.book_file.url
            book_det.append(book_dic)
        return book_det


class Book(Base):
    Book_type_choices = (
        ('ebook', 'ebook'),
        ('nbook', 'nbook')
    )
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    language = models.ManyToManyField(Language, related_name='book_language', blank=True)
    author = models.ManyToManyField(Author, related_name='book_author', blank=True)
    publisher = models.ForeignKey(Publisher, related_name='book_publisher' ,on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    book_type = models.CharField(max_length=50, choices=Book_type_choices)
    extra_det = models.CharField(max_length=100)
    book_file = models.FileField(upload_to='my_file', blank=True)
    #status = models.SmallIntegerField(max_length=30, default=PENDING, choices=STATUS_CHOICE)

    objects = BookManager()


    def __unicode__(self):
        return str(self.name)




class UserManager(models.Manager):
    def add_user(self, data): #first_name, middle_name, last_name, mobile_no, email_id, role, favorite, approve): #, file_url):
        user = self.create(**data) #first_name=first_name, middle_name=middle_name,\
        #last_name=last_name, mobile_no=mobile_no, email_id=email_id, role=role, approve=approve) #, e_book=file_url)
        #user.favorite.add(favorite)
        return user

    def get_user_details(self, user_ids):
        user_obj = self.filter(user_id__in=user_ids)
        user_details=[]
        for user in user_obj:
            user_dic={}
            user_dic['user_id'] = user.pk
            user_dic['name'] = user.first_name
            user_dic['mobile_no'] = user.mobile_no
            user_dic['email_id'] = user.email_id
            user_dic['role'] = user.role
            user_details.append(user_dic)
        return user_details

    def add_favorite(self,book_id, user_id):
        #import pdb;pdb.set_trace()
        book = Book.objects.filter(book_id__in=book_id)
        user_obj = User.objects.filter(user_id=user_id)
        for user in user_obj:
            user.favorite= book
            #user.favorite.add(book)

        return user    
            


class User(Base):
    role_choice = (
        ('student','student'),
        ('teacher', 'teacher'),
        ('admin', 'admin'),
        ('moderator', 'moderator')
    )
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=12)
    email_id = models.EmailField(max_length=50)
    role = models.CharField(max_length=30, choices=role_choice)    #ForeignKey(UserRoles, related_name='role', on_delete=models.CASCADE)
    subscription = models.BooleanField(default=False)
    favorite = models.ManyToManyField(Book, related_name='favorite', blank=True)
    #approve = models.BooleanField('approve', default=False)
    #e_book = models.FileField(upload_to='my_file', blank=True)
    

    def __unicode__(self):
        return str(self.first_name)


    objects = UserManager()   

class Subscription(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    duration = timedelta(days=7)

    def finish(self):
        return self.start + self.duration




class BookInfoManager(models.Manager):
    def add_ebook_info(self, b_id, isLent, lentTo):
        bookInfo = self.create(book_name=b_id, isLent=isLent, lentTo=lentTo)
        return bookInfo

    def get_book_info(self,hardCopy_id):
        book_info_obj = BookInfo.objects.filter(hardCopy_id__in=hardCopy_id)
        book_info=[]
        for info in book_info_obj:
            book_info_dict={}
            book_info_dict['hardCopy_id'] = info.hardCopy_id
            book_info_dict['book_name'] = info.book_name.name
            book_info_dict['isLent'] = info.isLent
            book_info_dict['lentTo'] = info.lentTo.first_name
            book_info.append(book_info_dict)
        return book_info

class BookInfo(models.Model):
    hardCopy_id = models.AutoField(primary_key=True)
    book_name = models.ForeignKey(Book, related_name='book_info', on_delete=models.CASCADE)
    isLent = models.BooleanField(default=False)
    lentTo = models.ForeignKey(User, related_name='lent_book', null=True)


    def __unicode__(self):
        return str(self.pk)

    objects = BookInfoManager()




class EbookManager(models.Manager):
    def add_ebook(self, ebook, location,user):
        ebook = self.create(ebook=ebook, book_location=location, uploaded_by=user)
        return ebook

    def get_ebook_info(self,book_id):
        ebook_obj = Ebook.objects.filter(book_id__in=book_id)
        ebook_list=[]
        for ebook in ebook_obj:
            ebook_dict = {}
            ebook_dict['book_id'] = ebook.book_id
            ebook_dict['name'] = ebook.ebook.name
            ebook_dict['approval_status'] = ebook.approval_status
            ebook_dict['book_location'] = ebook.book_location
            ebook_dict['uploaded_by'] = ebook.uploaded_by.first_name
            ebook_list.append(ebook_dict)
        return  ebook_list   


class Ebook(models.Model):

    STATUS_CHOICE = ((APPROVED, 'Approved'),
                     (REJECTED, 'Rejected'),
                     (PENDING, 'Pending for approval')
                     )
    book_id = models.AutoField(primary_key=True)
    ebook = models.ForeignKey(Book, related_name= 'book' ,on_delete=models.CASCADE)
    approval_status = models.SmallIntegerField(default=PENDING, choices=STATUS_CHOICE)
    book_location = models.CharField(max_length=100)#ForeignKey(Book, related_name='book_location', on_delete=models.CASCADE, editable=True)
    uploaded_by = models.ForeignKey(User, related_name='ebook_user', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.book_id)

    objects = EbookManager()




    

    