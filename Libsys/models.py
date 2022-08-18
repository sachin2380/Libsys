from __future__ import unicode_literals
from datetime import timedelta
from django.db import models
from .constants import *

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
    def add_language_details(self, language_details):
        language_obj = self.create(**language_details)
        return language_obj

    def get_langauge_details(self, language_ids):
        language_objs = self.filter(language_id__in=language_ids)
        language_list=[]
        for language_obj in language_objs:
            language_dict={}
            language_dict['language_id'] = language_obj.pk
            language_dict['name'] = language_obj.name
            language_dict['script'] = language_obj.script
            language_dict['about'] = language_obj.about
            language_list.append(language_dict)
        return language_list    



class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    script = models.CharField(max_length=20)
    about = models.TextField()

    objects = languageManager()

    def __unicode__(self):
        return str(self.name)

class AuthorsManager(models.Manager):
    def add_author(self,author_data):
        author_obj = self.create(**author_data)
        return author_obj

    def get_author_details(self, author_ids):
        author_objs = self.filter(author_id__in=author_ids)
        authors=[]
        for author in author_objs:
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
   
    def add_publisher_details(self, publisher_data):
        publisher_obj = self.create(**publisher_data)
        return publisher_obj

    def get_publisher_details(self, publisher_ids) :
        publisher_obj = Publisher.objects.filter(publisher_id__in=publisher_ids)
        publisher_det=[]
        for publisher in publisher_obj:
            publisher_dic={}
            publisher_dic['publisher_id'] = publisher.pk
            publisher_dic['name'] = publisher.name
            publisher_dic['contact_details'] = publisher.contact_details

            publisher_det.append(publisher_dic)
        return publisher_det


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_details= models.CharField(max_length=100)

    objects = PublisherManager()

    def __unicode__(self):
        return str(self.name)


# class BookManager(models.Manager):
       
#     # def add_book(self, name, lang_obj, publisher, author, category, book_type, extra_det, book_file):
#     #     book = self.create(name=name, publisher=publisher, category=category, book_type=book_type, extra_det=extra_det, book_file=book_file)
#     #     book.language.add(lang_obj)
#     #     book.author.add(author)
#     #     return book
#     def add_book(self, book_data):
#         # import pdb;pdb.set_trace()
#         book_obj = self.create(**book_data)
#         # book = self.create(name=as_dict['name'], language = as_dict['language'], author = as_dict['author'], publisher=as_dict['publisher'], category=as_dict['category'], book_type=as_dict['book_type'], extra_det=as_dict['extra'])

#         return book_obj

class BookManager(models.Manager):

    def add_book_details(self,book_data):
        book_dict={}
        book_dict['name'] = book_data.get('name')
        book_dict['language'] = book_data.get('language')
        book_dict['author'] = book_data.get('author')
        book_dict['publisher'] = book_data.get('publisher')
        book_dict['category'] = book_data.get('category')
        book_dict['book_type'] = book_data.get('book_type')
        book_dict['extra_det'] = book_data.get('extra_det')
        #book_dict['book_file'] = book_data.book_file.url
        book_obj = self.create(**book_dict)
        return book_obj

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

    objects = BookManager()


    def __unicode__(self):
        return str(self.name)

    def as_dict(self):
        return {
                "book_id": self.pk,
                "name": self.name,
                "language": [language_det.pk for language_det in self.language.all()],
                "author": [author_det.pk for author_det in self.author.all()],
                "publisher": self.publisher.pk if self.publisher else None,
                "category": self.category,
                "book_type": self.book_type,
                "extra_det": self.extra_det,
                "book_file": self.book_file,
        }    





class UserManager(models.Manager):
    def add_user(self, user_data):
        user_obj = self.create(**user_data)
        return user_obj

    def get_user_details(self, user_ids):
        user_objs = self.filter(user_id__in=user_ids)
        user_details=[]
        for user in user_objs:
            user_dic={}
            user_dic['user_id'] = user.pk
            user_dic['name'] = user.first_name
            user_dic['mobile_no'] = user.mobile_no
            user_dic['email_id'] = user.email_id
            user_dic['role'] = user.role
            user_details.append(user_dic)
        return user_details

    def add_favourite_book(self,book_id, user_id):
        book = Book.objects.filter(book_id__in=book_id)
        user_objs = User.objects.filter(user_id=user_id)
        for user in user_objs:
            user.favourite= book
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
    role = models.CharField(max_length=30, choices=role_choice)
    subscription = models.BooleanField(default=False)
    favourite = models.ManyToManyField(Book, related_name='favourite', blank=True)
    

    def __unicode__(self):
        return str(self.first_name)


    objects = UserManager()   

class BookInfoManager(models.Manager):
    def add_ebook_info(self, b_id, isLent, lentTo):
        bookInfo_obj = self.create(book_name=b_id, isLent=isLent, lentTo=lentTo)
        return bookInfo_obj

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
        ebook_obj = self.create(ebook=ebook, book_location=location, uploaded_by=user)
        return ebook_obj

    def get_ebook_info(self,book_id):
        ebook_objs = Ebook.objects.filter(book_id__in=book_id)
        ebook_list=[]
        for ebook in ebook_objs:
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
    book_location = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, related_name='ebook_user', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.book_id)

    objects = EbookManager()




    

    