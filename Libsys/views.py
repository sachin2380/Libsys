from pickle import TRUE
from string import punctuation
from rest_framework.response import Response
from django.http import HttpResponse, QueryDict
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
import traceback

#Libsys import
from .constants import *
from .models import *
from .response import *
from .exception import favoriteException, BookException, LanguageException, AuthorException, PublisherException,\
    UserException, EbookException, BookInfoException, Subscriptionexception, ApprovalException




class LanguageView(View):
    def __init__(self):
        self.response = init_response()

    def validation(self, lang_ids):
        language_obj = Language.objects.filter(lang_id__in=lang_ids)
        if language_obj:
            pass
        else:
            raise LanguageException("Invalid Langauge id")

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
        # name = params.get('name')
        # script = params.get('script')
        # about = params.get('about')
            Language.objects.add_language(params) #ame, script, about)
            self.response['res_str'] = LANG_SUC_ADDED
            return send_201(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)

    def get(self,request):
        params = request.GET.dict()
        lang_ids = params.get('lang_id').strip().split(',')
        try:
            self.validation(lang_ids)
            language = Language.objects.get_langauge(lang_ids)
            self.response['res_data'] = language
            self.response['res_str'] = LANG_SUC_FIND
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    

    def put(self,request):
        params = request.GET.dict()
        try:
            lang_id = params.get('lang_id')
            about = params.get('about')
            self.validation(lang_id)
            language_obj=Language.objects.get(lang_id=lang_id)
            language_obj.about = about
            language_obj.save(update_fields=['about'])
            self.response['res_str'] = LANG_DIS_UPDATE 
            return send_200(self.response)
        except LanguageException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)        


class AuthorView(View):
    def __init__(self):
        self.response = init_response()

    def validation(self,author_id):
        author_obj = Author.objects.filter(author_id__in=author_id)
        if author_obj:
            pass
        else:
            raise AuthorException("Invalid Author id")


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
        # name = params.get('name')
        # email_id = params.get('email_id')
            picture = request.FILES['picture']
            Author.objects.add_author(params,picture) #name, email_id, picture)
            self.response['res_str'] = AUTHOR_SUC_ADDED
            return send_201(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)

    def get(self,request):
        params = request.GET.dict()
        try:
            author_ids = params.get('author_id').strip().split(',')
            self.validation(author_ids)
            # author_obj = Author.objects.filter(author_id__in=author_ids)
            # if author_obj:
            author = Author.objects.get_author_details(author_ids)
            self.response['res_data'] = author
            self.response['res_str'] = AUTHOR_SUC_FOUND
            return send_200(self.response)
            # else:
            #     self.response['res_str'] = AUTHOR_DET_NOT_FOUND
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)

    def put(self,request):
        params = request.GET.dict()
        try:
            author_id = params.get('author_id')
            email_id = params.get('email_id')
            self.validation(author_id)
            author_obj = Author.objects.get(author_id=author_id)
            author_obj.email_id = email_id 
            author_obj.save(update_fields=['email_id'])
            self.response['res_str'] = AUTH_DET_UPDATE
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
  
    def delete(self,request):
        params = request.GET.dict()
        try:

            author_id = params.get('author_id')
            self.validation(author_id)
            # author_obj = Author.objects.filter(author_id=author_id)
            # if author_obj:
            Author.objects.get(author_id=author_id).delete()
            self.response['res_str'] = AUTH_DEL_SUC
            # else:
            #     self.response['res_str'] =  AUTHOR_DET_NOT_FOUND   
            return send_200(self.response)
        except  AuthorException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)             


class BookView(View):
    def __init__(self):
        self.response = init_response()


    def validation(self,book_id):
        book_obj = Book.objects.filter(book_id__in=book_id)
        if book_obj:
            pass
        else:
            raise BookException("Invalid Book id")


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
            name = params.get('name')
            category = params.get('category')
            book_type = params.get('book_type')
            extra = params.get('extra')
            language_id = params.get('language_id')
            lang_obj = Language.objects.get(lang_id = language_id)
            publisher_id = params.get('pub_id')
            publisher_obj = Publisher.objects.get(pub_id = publisher_id)
            author_id =params.get('author_id')
            author_obj = Author.objects.get(author_id=author_id)
            file_url = request.FILES['e_book']
            Book.objects.add_book(name, lang_obj, publisher_obj, author_obj, category, book_type, extra, file_url)
            self.response['res_str'] = BOOK_SUC_ADDED
            return send_201(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)

    def get(self, request):
        params=request.GET.dict()
        try:
            per_page= params.get('per_page')
            book_ids = params.get('book_id').strip().split(',')
            # book_obj = Book.objects.filter(book_id__in=book_ids)
            # if book_obj:
            self.validation(book_ids)
            book = Book.objects.get_book_details(book_ids)
            paginator = Paginator(book,per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.page(page_number)
            book_data = page_obj.object_list
            self.response['res_data'] = book_data
            self.response['res_str'] = BOOK_DET_FOUND_SUC
            # else:
            #     self.response['res_str'] = BOOK_DET_NOT_FOUND
            return send_201(self.response)
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)


           
    def delete(self,request):
        params = request.GET.dict()
        try:
            book_id = params.get('book_id')
            # book_obj = Book.objects.filter(book_id=book_id)
            # if book_obj:
            self.validation(book_id)
            Book.objects.get(book_id=book_id).delete()
            self.response['res_str'] = BOOK_DEL_SUC
            # else:
            #     self.response['res_str'] = BOOK_DET_NOT_FOUND   
            return send_200(self.response)       
        except BookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)  


class UserView(View):
    def __init__(self):
        self.response = init_response()


    def validation(self,user_id):
        user_obj = User.objects.filter(user_id__in = user_id)
        if user_obj:
            pass
        else:
            raise UserException("Invalid User Id")


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
        # first_name = params.get('first_name')
        # middle_name = params.get('middle_name')
        # last_name = params.get('last_name')
        # mobile_no = params.get('mobile_no')
        # email_id = params.get('email_id')
        # role = params.get('role')
        #role_id = params.get('role')
        #role_obj = UserRoles.objects.get(id = role_id)
        # book_id = params.get('book_id')
        # favorite = Book.objects.get(book_id = book_id)
            #file_url = request.FILES['e_book']
            User.objects.add_user(params) #first_name, middle_name, last_name, mobile_no, email_id, role) #, favorite, approve) , file_url, role_obj,)
            self.response['res_str'] = USER_SUC_ADDED
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
            self.validation(user_ids)
            # user_obj = User.objects.filter(user_id__in = user_ids)
            # if user_obj:
            user = User.objects.get_user_details(user_ids)
            self.response['res_data'] = user
            self.response['res_str'] = USER_SUC_FOUND
            # else:
            #     self.response['res_str'] = USER_DET_NOT_FOUND
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)    



    def put(self,request):
        #import pdb;pdb.set_trace()
        params = request.GET.dict()
        try:
            user_id = params.get('user_id')
            role = params.get('role')
            mobile_no = params.get('mobile_no')
            email_id = params.get('email_id')
            self.validation(user_id)
            user_obj = User.objects.get(user_id=user_id)
            user_obj.mobile_no = mobile_no
            user_obj.email_id = email_id
            user_obj.role = role
            user_obj.save(update_fields=['email_id', 'mobile_no', 'role'])
            self.response['res_str'] = USER_DET_UPDATE
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response) 

    def delete(self,request):
        params = request.GET.dict()
        try:
            user_id = params.get('user_id')
            # user_obj = User.objects.filter(user_id=user_id)
            # if user_obj:
            self.validation(user_id)
            User.objects.get(user_id=user_id).delete()
            self.response['res_str'] = USER_DEL_SUC
            # else:
            #     self.response['res_str'] = USER_DET_NOT_FOUND
            return send_200(self.response)
        except UserException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)     
            
class PublisherView(View):
    def __init__(self):
        self.response = init_response()


    
    def validation(self,pub_id):
        publisher_obj = Publisher.objects.filter(pub_id__in = pub_id)
        if publisher_obj:
            pass
        else:
            raise PublisherException("Invalid Publisher Id")    

    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        try:
        # name = params.get('name')
        # contact_details = params.get('contact_details')
            Publisher.objects.add_publisher(params) #name, contact_details)
            self.response['res_str'] = PUBS_SUC_ADDED
            return send_200(self.response)
        except Exception as ex:
            trace_err = traceback.format_exc()
            trace_err=str(trace_err)
            self.response['res_str'] = str(ex)
            return send_400(self.response)            
    
    def get(self, request):
        params = request.GET.dict()
        try:
            pub_ids = params.get('pub_id').strip().split(',')
            # publisher_obj = Publisher.objects.filter(pub_id__in=pub_ids)
        # if publisher_obj:
            self.validation(pub_ids)
            publisher_det = Publisher.objects.publisher_details(pub_ids)
            self.response['res_data'] = publisher_det
            self.response['res_str'] = PUBS_SUC_FIND
            # else:
            #     self.response['res_str'] = PUBLISHER_DET_NOT_FOUND 
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)      
        

    def put(self,request):
        params = request.GET.dict()
        try:
            pub_id = params.get('pub_id')
            self.validation(pub_id)
            # pub_obj = Publisher.objects.filter(pub_id=pub_id)
            # if pub_obj:
            publisher_obj = Publisher.objects.get(pub_id=pub_id)
            contact_details = params.get('contact_details')
            publisher_obj.contact_details = contact_details
            publisher_obj.save(update_fields=['contact_details'])
            self.response['res_str'] = PUBLISHER_DET_UPDATE_SUCC
            # else:
            #     self.response['res_str'] = PUBLISHER_DET_NOT_FOUND   
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
    
    def delete(self,request):
        params = request.GET.dict()
        try:
            pub_id = params.get('pub_id')
            self.validation(pub_id)
            # publisher_obj = Publisher.objects.filter(pub_id=pub_id)
            # if publisher_obj:
            Publisher.objects.get(pub_id=pub_id).delete()
            self.response['res_str'] = PUBLI_DEL_SUC
        # else:
        #     self.response['res_str'] = PUBLISHER_DET_NOT_FOUND 
            return send_200(self.response)
        except PublisherException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)


class EbookView(View):

    def __init__(self):
        self.response = init_response()

    def validation(self,book_id):
        ebook_obj = Ebook.objects.filter(book_id__in = book_id)
        if ebook_obj:
            pass
        else:
            raise EbookException("Invalid Ebook Id")        

    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id')
            book_obj = Book.objects.get(book_id = book_id)
            location_obj = Book.objects.filter(book_id=book_id)
            for local in location_obj:
                location = local.book_file
            user_id = params.get('user_id')
            user = User.objects.get(user_id=user_id)
            Ebook.objects.add_ebook(book_obj, location, user)
            self.response['res_str'] = EBOOK_SUC_ADDED
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
            self.validation(book_id)
            ebook = Ebook.objects.get_ebook_info(book_id)
            self.response['res_data'] = ebook
            self.response['res_str'] = PUBS_SUC_FIND
            return send_200(self.response)
        except EbookException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)


class Book_approval(View):
    def __init__(self):
        self.response = init_response()

    def validation(self,book_id):
        book_obj = Ebook.objects.filter(book_id=book_id)
        if book_obj:
            pass
        else:
            raise ApprovalException("This action is not allowed")


    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id')
            approval_status = params.get('approval_status')
            # book_obj = Ebook.objects.filter(book_id=book_id)
            # if book_obj:
            self.validation(book_id)
            book_obj = Ebook.objects.get(book_id=book_id)
            book_obj.approval_status =  approval_status 
            book_obj.save(update_fields = ['approval_status'])
            self.response['res_str'] = BOOK_STATUS_CHANG
        # else:
        #     self.response['res_str'] = BOOK_DET_NOT_FOUND 
            return send_200(self.response)    
        except ApprovalException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)            




class BookInfoView(View):
    def __init__(self):
        self.response = init_response()

    def validation(self,hardCopy_id):
        bookinfo_obj = BookInfo.objects.filter(hardCopy_id__in = hardCopy_id)
        if bookinfo_obj:
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
                self.response['res_str'] = BOOK_INFO_ADD
            else:
                self.response['res_str'] = USER_SUBS_DEACTIVATE   
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
            self.validation(hardCopy_id)
            book_info =  BookInfo.objects.get_book_info(hardCopy_id)
            self.response['res_data'] = book_info
            self.response['res_str'] = BOOK_INFO_SUC_FIND
            return send_200(self.response)
        except BookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)

        

    def delete(self,request):
        params = request.GET.dict()
        try:
            hardCopy_id = params.get('hardCopy_id')
            # name=params.get('name')
            # bookinfo_obj = BookInfo.objects.get(hardCopy_id=hardCopy_id)
            # if bookinfo_obj:
            self.validation(hardCopy_id)
            BookInfo.objects.get(hardCopy_id=hardCopy_id).delete()
            self.response['res_str'] = BOOK_DEL_SUC
            return send_200(self.response)
        except BookInfoException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)
    

        # book_count = BookInfo.objects.select_related('book_name').all().count()
        # if book_count<3:
        #     user_subs = User.objects.get(first_name=name)
        #     user_subs.subscription = False
        #     user_subs.save(update_fields=['subscription'])
        #     self.response['res_str'] = SUBS_DEACTIVATE   
        # return send_200(self.response)
            
                          




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
        author = params.get('author')
        book_name = params.get('name')
        category = params.get('category')
        publisher = params.get('publisher')
        book_list = Book.objects.filter(Q(author__name__contains=author)|Q(publisher__name__contains=publisher)|Q(category__contains__contains=category) |Q(name__contains=book_name)).\
            values_list("name",flat=True)
        book_lis=[]
        for book in book_list:
            book_lis.append(book)           
        self.response['res_data'] = book_lis
        self.response['res_str'] = BOOK_DET_FOUND_SUC
        return send_200(self.response)    
    

class favoriteView(View):
    
    def __init__(self):
        self.response = init_response()


    def validation(self,book_id, user_id):
        user_obj = User.objects.get(user_id=user_id)
        book_obj = Book.objects.filter(book_id__in=book_id)
        if user_obj and book_obj:
            pass
        else:
            raise favoriteException("check the user id and book id that you enter")       

    def post(self,request):
        params = request.POST.dict()
        try:
            book_id = params.get('book_id').strip().split(',')
            user_id = params.get('user_id')
            self.validation(book_id,user_id)
            User.objects.add_favorite(book_id,user_id)
            self.response['res_str'] = FAV_BOOK
            return send_200(self.response)
        except favoriteException as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)        

class Subscription(View):

    def __init__(self):
        self.response = init_response()

    def validation(self,user_id):
        user_subs = User.objects.get(user_id=user_id)
        if user_subs.subscription == True:
            raise Subscriptionexception("This action is not allowed. User has already active subscription")


    def put(self,request):
        params = request.GET.dict()
        try:
            user_id= params.get('user_id')
            self.validation(user_id)
            user_subs = User.objects.get(user_id=user_id)
            user_subs.subscription = True
            user_subs.save(update_fields=['subscription'])
            self.response['res_str'] = SUBS_ACTIVATE 
            return send_200(self.response)
        except Subscriptionexception as ex:
            self.response['res_str'] = str(ex)
            return send_400(self.response)     

    # def post(self,request):
    #     params = request.POST.dict()
    #     name= params.get('name')
    #     book_count = BookInfo.objects.select_related('book_name').filter(lentTo__first_name=name).count()
    #     if book_count>=3:
    #         user_subs = User.objects.get(first_name=name)
    #         user_subs.subscription = True
    #         user_subs.save(update_fields=['subscription'])
    #     self.response['res_str'] = SUBS_ACTIVATE
    #     return send_200(self.response)        


   
