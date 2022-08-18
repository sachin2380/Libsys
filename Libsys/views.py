from pickle import TRUE
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Q
import traceback
from .response import *
import json

#Libsys import
from .constants import (LANGUAGE_SUCCESSFULLY_ADDED, LANGUAGE_DETAILS_FOUND, LANGUAGE_UPDATED_SUCCESSFULLY,
                        AUTHOR_SUCCESSFULLY_ADDED,AUTHOR_SUCCESSFULLY_FOUND, AUTHOR_DETAILS_UPDATED, AUTHOR_DETAILS_DELETED,
                        BOOK_SUCCESSFULLY_ADDED,BOOK_DETAILS_FOUND, BOOK_DELETED, BOOK_INFO_FOUND,
                        USER_ADDED, USER_DETAILS_FOUND, USER_DETAILS_UPDATED, USER_DELETED, USER_SUBSCRIPTION_ERR,
                        PUBLISHER_ADDED, PUBLISHER_DETAILS_FOUND, PUBLISHER_DETAILS_UPDATED, PUBLISHER_DELETED,
                        BOOK_ISSUED, BOOK_INFO_FOUND, BOOK_STATUS_CHANGE,
                        EBOOK_ADDED, EBOOK_DETAILS_FOUND,
                        FAVOURITE_BOOK_ADDED,
                        SUBSCRIPTION_ACTIVATED, SUBSCRIPTION_DEACTIVATED)
from .models import Language, Author, Publisher, Book, BookInfo, Ebook, User
from .exception import favoriteException, BookException, LanguageException, AuthorException, PublisherException,\
    UserException, EbookException, BookInfoException, SubscriptionException, ApprovalException




class LanguageView(View):
    def __init__(self):
        self.response = init_response()

    def validate_language_ids(self, language_ids):
        language_objs = Language.objects.filter(language_id__in=language_ids)
        if language_objs:
            pass
        else:
            raise LanguageException("Invalid Langauge id")

    def post(self, request):
        params = request.POST.dict()
        try:
            Language.objects.add_language_details(params)
            self.response['res_str'] = LANGUAGE_SUCCESSFULLY_ADDED
            return send_201(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)

    def get(self,request):
        params = request.GET.dict()
        language_ids = params.get('language_id').strip().split(',')
        try:
            self.validate_language_ids(language_ids)
            language = Language.objects.get_langauge_details(language_ids)
            self.response['res_data'] = language
            self.response['res_str'] = LANGUAGE_DETAILS_FOUND
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    

    def put(self,request):
        params = request.GET.dict()
        try:
            language_id = params.get('language_id')
            about = params.get('about')
            self.validate_language_ids(language_id)
            language_obj=Language.objects.get(language_id=language_id)
            language_obj.about = about
            language_obj.save(update_fields=['about'])
            self.response['res_str'] = LANGUAGE_UPDATED_SUCCESSFULLY 
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)        


class AuthorView(View):
    def __init__(self):
        self.response = init_response()

    def validate_author_ids(self,author_id):
        author_objs = Author.objects.filter(author_id__in=author_id)
        if not author_objs:
            raise AuthorException("Invalid Author id")


    def post(self, request):
        params = request.POST.dict()
        try:
            #picture = request.FILES['picture']
            Author.objects.add_author(params)
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_ADDED
            return send_200(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)
      
    def get(self,request):
        params = request.GET.dict()
        try:
            author_ids = params.get('author_id').strip().split(',')
            self.validate_author_ids(author_ids)
            author = Author.objects.get_author_details(author_ids)
            self.response['res_data'] = author
            self.response['res_str'] = AUTHOR_SUCCESSFULLY_FOUND
            return send_200(self.response)
        except AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)  
    def put(self,request):
        params = request.GET.dict()
        try:
            author_id = params.get('author_id')
            email_id = params.get('email_id')
            self.validate_author_ids(author_id)
            author_obj = Author.objects.get(author_id=author_id)
            author_obj.email_id = email_id 
            author_obj.save(update_fields=['email_id'])
            self.response['res_str'] = AUTHOR_DETAILS_UPDATED
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)          
  
    def delete(self,request):
        params = request.GET.dict()
        try:

            author_id = params.get('author_id')
            self.validate_author_ids(author_id)
            Author.objects.get(author_id=author_id).delete()
            self.response['res_str'] = AUTHOR_DETAILS_DELETED   
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)             
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)  

class BookView(View):
    def __init__(self):
        self.response = init_response()


    def validate_book_ids(self,book_id):
        book_objs = Book.objects.filter(book_id__in=book_id)
        if not book_objs:
            raise BookException("Invalid Book id")

    # def post(self, request, *args, **kwargs):
    #     params = request.POST.dict()
    #     try:
    #         # name = params.get('name')
    #         # category = params.get('category')
    #         # book_type = params.get('book_type')
    #         # extra = params.get('extra')
    #         # language_id = params.get('language_id')
    #         # lang_obj = Language.objects.get(lang_id = language_id)
    #         # publisher_id = params.get('pub_id')
    #         # publisher_obj = Publisher.objects.get(pub_id = publisher_id)
    #         # author_id =params.get('author_id')
    #         # author_obj = Author.objects.get(author_id=author_id)
    #         # file_url = request.FILES['e_book']
    #         # Book.objects.add_book(name, lang_obj, publisher_obj, author_obj, category, book_type, extra, file_url)
    #         Book.objects.add_book(params)
    #         self.response['res_str'] = BOOK_SUCCESSFULLY_ADDED
    #         return send_200(self.response)
    #     except Exception as ex:
    #         str(traceback.format_exc())
    #         self.response['res_str'] = str(ex)
    #         return send_400(self.response)

    def post(self,request,*args, **kwargs):

        def __init__(self):
            self.response = init_response()

        try:
            data = request.POST.dict()
            #self.validate_data(data)
            self.response['res_data'] = Book.objects.add_book_details(data)
            self.response['res_str'] = BOOK_DETAILS_FOUND
            return send_200(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)  

    def get(self, request):
        params=request.GET.dict()
        try:
            per_page= params.get('per_page')
            book_ids = params.get('book_id').strip().split(',')
            self.validate_book_ids(book_ids)
            book = Book.objects.get_book_details(book_ids)
            paginator = Paginator(book,per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.page(page_number)
            book_data = page_obj.object_list
            self.response['res_data'] = book_data
            self.response['res_str'] = BOOK_DETAILS_FOUND
            return send_200(self.response)
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)
   
    def delete(self,request):
        params = request.GET.dict()
        try:
            book_id = params.get('book_id')
            self.validate_book_ids(book_id)
            Book.objects.get(book_id=book_id).delete()
            self.response['res_str'] = BOOK_DELETED 
            return send_200(self.response)       
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)  


class UserView(View):
    def __init__(self):
        self.response = init_response()


    def validate_user_ids(self,user_id):
        user_objs = User.objects.filter(user_id__in = user_id)
        if not user_objs:
            raise UserException("Invalid User Id")

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            User.objects.add_user(params)
            self.response['res_str'] = USER_ADDED
            return send_200(self.response) 
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)       

    def get(self,request):
        params = request.GET.dict()
        try:

            user_ids = params.get('user_id').strip().split(',')
            self.validate_user_ids(user_ids)
            user = User.objects.get_user_details(user_ids)
            self.response['res_data'] = user
            self.response['res_str'] = USER_DETAILS_FOUND
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    

    def put(self,request):
        params = request.GET.dict()
        try:
            user_id = params.get('user_id')
            role = params.get('role')
            mobile_no = params.get('mobile_no')
            email_id = params.get('email_id')
            self.validate_user_ids(user_id)
            user_obj = User.objects.get(user_id=user_id)
            user_obj.mobile_no = mobile_no
            user_obj.email_id = email_id
            user_obj.role = role
            user_obj.save(update_fields=['email_id', 'mobile_no', 'role'])
            self.response['res_str'] = USER_DETAILS_UPDATED
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response) 

    def delete(self,request):
        params = request.GET.dict()
        try:
            user_id = params.get('user_id')
            self.validate_user_ids(user_id)
            User.objects.get(user_id=user_id).delete()
            self.response['res_str'] = USER_DELETED
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
            
class PublisherView(View):
    def __init__(self):
        self.response = init_response()

    def validate_publisher_ids(self,publisher_id):
        publisher_objs = Publisher.objects.filter(publisher_id__in = publisher_id)
        if not publisher_objs:
            raise PublisherException("Invalid Publisher Id")   

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            Publisher.objects.add_publisher_details(params)
            self.response['res_str'] = PUBLISHER_ADDED
            return send_200(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
    
    def get(self, request):
        params = request.GET.dict()
        try:
            publisher_ids = params.get('publisher_id').strip().split(',')
            self.validate_publisher_ids(publisher_ids)
            publisher_det = Publisher.objects.get_publisher_details(publisher_ids)
            self.response['res_data'] = publisher_det
            self.response['res_str'] = PUBLISHER_DETAILS_FOUND
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)          
        

    def put(self,request):
        params = request.GET.dict()
        try:
            publisher_id = params.get('publisher_id')
            self.validate_publisher_ids(publisher_id)
            publisher_obj = Publisher.objects.get(publisher_id=publisher_id)
            contact_details = params.get('contact_details')
            publisher_obj.contact_details = contact_details
            publisher_obj.save(update_fields=['contact_details'])
            self.response['res_str'] = PUBLISHER_DETAILS_UPDATED
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response) 
    
    def delete(self,request):
        params = request.GET.dict()
        try:
            publisher_id = params.get('publisher_id')
            self.validate_publisher_ids(publisher_id)
            Publisher.objects.get(publisher_id=publisher_id).delete()
            self.response['res_str'] = PUBLISHER_DELETED
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)

class EbookView(View):

    def __init__(self):
        self.response = init_response()

    def validate_ebook_ids(self,book_id):
        ebook_objs = Ebook.objects.filter(book_id__in = book_id)
        if not ebook_objs:
            raise EbookException("Invalid Ebook Id")        

    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id')
            book_obj = Book.objects.get(book_id = book_id)
            location_objs = Book.objects.filter(book_id=book_id)
            for location in location_objs:
                location = location.book_file
            user_id = params.get('user_id')
            user = User.objects.get(user_id=user_id)
            Ebook.objects.add_ebook(book_obj, location, user)
            self.response['res_str'] = EBOOK_ADDED
            return send_200(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)            

    def get(self,request):
        params =  request.GET.dict()
        try:
            book_id = params.get('book_id').strip().split(',')
            self.validate_ebook_ids(book_id)
            ebook = Ebook.objects.get_ebook_info(book_id)
            self.response['res_data'] = ebook
            self.response['res_str'] = EBOOK_DETAILS_FOUND
            return send_200(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)


class Book_approval(View):
    def __init__(self):
        self.response = init_response()

    def BooKValidation(self,book_id):
        book_objs = Ebook.objects.filter(book_id=book_id)
        if not book_objs:
            raise ApprovalException("This action is not allowed. enter valid book d")


    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id')
            approval_status = params.get('approval_status')
            self.BooKValidation(book_id)
            book_obj = Ebook.objects.get(book_id=book_id)
            book_obj.approval_status =  approval_status 
            book_obj.save(update_fields = ['approval_status'])
            self.response['res_str'] = BOOK_STATUS_CHANGE
            return send_200(self.response)    
        except ApprovalException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)

class BookInfoView(View):
    def __init__(self):
        self.response = init_response()

    def validate_hardcopy_ids(self,hardCopy_id):
        bookinfo_objs = BookInfo.objects.filter(hardCopy_id__in = hardCopy_id)
        if bookinfo_objs:
            pass
        else:
            raise BookInfoException("Invalid hardCopy Id")     

    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id')
            book_obj = Book.objects.get(book_id=book_id)
            isLent = params.get('isLent')
            user_id = params.get('user_id')
            user_obj = User.objects.get(user_id=user_id)
            if user_obj.subscription == True:
                BookInfo.objects.add_ebook_info(book_obj, isLent, user_obj)
                self.response['res_str'] = BOOK_ISSUED
            else:
                self.response['res_str'] = USER_SUBSCRIPTION_ERR   
            return send_200(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)    

    def get(self,request):
        params = request.GET.dict()
        try:
            hardCopy_id = params.get('hardCopy_id').strip().split(',')
            self.validate_hardcopy_ids(hardCopy_id)
            book_info =  BookInfo.objects.get_book_info(hardCopy_id)
            self.response['res_data'] = book_info
            self.response['res_str'] = BOOK_INFO_FOUND
            return send_200(self.response)
        except BookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        

    def delete(self,request):
        params = request.GET.dict()
        try:
            hardCopy_id = params.get('hardCopy_id')
            self.validate_hardcopy_ids(hardCopy_id)
            BookInfo.objects.get(hardCopy_id=hardCopy_id).delete()
            self.response['res_str'] = BOOK_DELETED
            return send_200(self.response)
        except BookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)    

class searchView(View):

    def __init__(self):
        self.response = init_response()



    # def validation(self,author,publisher,category,book_name):
    #     book_obj = Book.objects.filter(author__name=author or publisher__name = publisher or category=category or book_name=book_name)   
    #     if book_obj:
    #         pass
    #     else:
    #         raise BookException("")  

    def get(self, request):
        params = request.GET.dict()
        try:
            author = params.get('author')
            book_name = params.get('name')
            category = params.get('category')
            publisher = params.get('publisher')
            book_list = Book.objects.filter(Q(author__name=author)|Q(publisher__name=publisher)|Q(category=category)|Q(name=book_name)).values_list("name",flat=True)
            book_lis=[]
            for book in book_list:
                book_lis.append(book)           
            self.response['res_data'] = book_lis
            self.response['res_str'] = BOOK_DETAILS_FOUND
            return send_200(self.response)    
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)     

class favoriteView(View):
    
    def __init__(self):
        self.response = init_response()


    def validate_user_book_ids(self,book_id, user_id):
        user_obj = User.objects.get(user_id=user_id)
        book_objs = Book.objects.filter(book_id__in=book_id)
        if user_obj and book_objs:
            pass
        else:
            raise favoriteException("user id or book id error. check the user id and book id ")       

    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id').strip().split(',')
            user_id = params.get('user_id')
            self.validate_user_book_ids(book_id,user_id)
            User.objects.add_favourite_book(book_id,user_id)
            self.response['res_str'] = FAVOURITE_BOOK_ADDED
            return send_200(self.response)
        except favoriteException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)
                   

class Subscription(View):

    def __init__(self):
        self.response = init_response()

    def validate_subscription(self,user_id):
        user_obj = User.objects.get(user_id=user_id)
        if not user_obj:
            raise SubscriptionException("User does not exist. enter valid user id")

    def put(self,request):
        params = request.GET.dict()
        try:
            user_id= params.get('user_id')
            choice = params.get('choice')
            self.validate_subscription(user_id)
            user_subs = User.objects.get(user_id=user_id)
            if int(choice)==1:    # choice=1 for subscription activation and "0" for subscription deactivaion
                user_subs.subscription = True
                self.response['res_str'] = SUBSCRIPTION_ACTIVATED
            else:
                user_subs.subscription = False
                self.response['res_str'] = SUBSCRIPTION_DEACTIVATED
            user_subs.save(update_fields=['subscription'])
            return send_200(self.response)
        except SubscriptionException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
        except Exception as ex:
            str(traceback.format_exc())
            self.response['res_str'] = str(ex)
            return send_400(self.response)           
       

