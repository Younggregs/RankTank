from __future__ import unicode_literals
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password , make_password
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.core import serializers
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth import authenticate , login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Account, Contest, Contestant, PrivateVoter, ForgotPassword
from .serializers import AccountSerializer, FetchAccountSerializer, ContestSerializer, ContestantSerializer, ContestantTankerSerializer, SuccessSerializer, ErrorCheckSerializer
import random
import string
import json











def url_code_generator(size=16, chars=string.ascii_lowercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))






def get_account(request):

    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        email = user.username


        account = Account.objects.get(email = email)

        return account

    else:
        
        return -1
















class IsLoggedIn(APIView):

    def get(self, request):

        signed_in = False

        try:
            account = get_account(request)
            signed_in = True

        except:

            pass
            

        return Response(signed_in)


    
    def post(self, request):

        pass



















class SignUp(APIView):

    def get(self,request):

        account = Account.objects.all()
        serializer = FetchAccountSerializer(account, many=True)

        return Response(serializer.data)





    def post(self,request):


        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():


            email = serializer.data['email']
            password = serializer.data['password']
            firstname = serializer.data['firstname']
            lastname = serializer.data['lastname']
            is_admin = serializer.data['is_admin']
            is_super = serializer.data['is_super']

            try:

                User.objects.get(username = email)
                Account.objects.get(email = email)

                error = 'Oops an account with that email already exist'
                err = {
                    'error' : error
                }
                serializer = ErrorCheckSerializer( err, many=False)

                return Response(serializer.data)

            except:
                pass


            password = serializer.data['password']
            raw_password = password
            password = make_password(password)
            

            user = User()
            user.username = email
            user.password = password
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            user = authenticate(username=email, password=raw_password)


            if user is not None and user.is_active:

                login(request, user)

                account = Account()
                account.firstname = firstname
                account.lastname = lastname
                account.email = email
                account.is_admin = is_admin
                account.is_super = is_super
                account.password = password
                account.save()

                code = 11

                success = {
                    'code' : code
                }

                serializer = SuccessSerializer(success , many = False)

                return Response(serializer.data)

            else:

                error = 'Yay something broke, please try again '
                err = {
                    'error' : error
                }
                serializer = ErrorCheckSerializer( err, many=False)

                return Response(serializer.data)




        else :
            error = 'oooouu something went wrong, please try again '
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)














































class SignIn(APIView):

    def get(self,request):
        pass

    def post(self,request):

        email = request.POST.get("email","")
        password = request.POST.get("password","")


        user = authenticate(username=email, password=password)

        
        if user is not None and user.is_active:
            login(request, user)

            code = 11
            success = {
                'code' : code
            }

            serializer = SuccessSerializer(success, many = False)

            return Response(serializer.data)

        else:

            error = 'email and password did not match '
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)


        error = 'Invalid login, try again please '
        
        err = {
            'error' : error
        }
        serializer = ErrorCheckSerializer( err, many=False)

        return Response(serializer.data)





















class NewContest(APIView):

    def get(self, request):
        

        contest = Contest.objects.all()

        serializer = ContestSerializer( contest, many=True)
        return Response(serializer.data)


    def post(self, request):

        ####Auth
        account = get_account(request)

        title = request.POST.get("title","")
        contestants = request.POST.get("contestants","")

        url = url_code_generator()
        url_exist = False
        try:
            url_check = Contest.objects.get(url = url)
            url_exist = True

        except:
            pass

        if url_exist :
            url = url_code_generator()


        new_contest = Contest()
        new_contest.account = account
        new_contest.title = title
        new_contest.url = url
        new_contest.save()


        contestants_bucket = contestants.split(",")

        for contestant in contestants_bucket:

            new_contestant = Contestant()
            new_contestant.contest = new_contest
            new_contestant.contestant = contestant
            new_contestant.points = 0
            new_contestant.rank = 0
            new_contestant.save()

        
        code = url
        success = {
            'code' : code
        }

        serializer = SuccessSerializer(success, many = False)

        return Response(serializer.data)



















class NewPrivateContest(APIView):

    def get(self, request):
        
        contest = Contest.objects.all()

        serializer = ContestSerializer( contest, many=True)
        return Response(serializer.data )


    def post(self, request):

        ####Auth
        account = get_account(request)

        title = request.POST.get("title","")
        contestants = request.POST.get("contestants","")
        email_list = request.POST.get("email_list","")


        url = url_code_generator()
        url_exist = False
        try:
            url_check = Contest.objects.get(url = url)
            url_exist = True

        except:
            pass

        if url_exist :
            url = url_code_generator()


        new_contest = Contest()
        new_contest.account = account
        new_contest.title = title
        new_contest.url = url
        new_contest.save()


        contestants_bucket = contestants.split(",")

        for contestant in contestants_bucket:

            new_contestant = Contestant()
            new_contestant.contest = new_contest
            new_contestant.contestant = contestant
            new_contestant.points = 0
            new_contestant.rank = 0
            new_contestant.save()

        
        email_list_bucket = email_list.split(",")

        for voter in email_list_bucket:

            v_url = url_code_generator()

            message = 'RankTank Title: ' + name + '\n\nHello dear, use this RankTank link to vote -> http://127.0.0.1:3000/private_rank/' +  str(v_url) + '\n\n RankTank, fair and smooth!\n'
            email = EmailMessage('RankTank Private Vote', message, to=[voter])
            email.send()

            new_contestant = PrivateVoter()
            new_contestant.contest = new_contest
            new_contestant.voter = voter
            new_contestant.url = v_url
            new_contestant.save()

        
        code = url
        success = {
            'code' : code
        }

        serializer = SuccessSerializer(success, many = False)

        return Response(serializer.data)
































class RankVote(APIView):

    def get(self, request, url):
        
        contest = Contest.objects.all()

        serializer = ContestSerializer( contest, many=True)
        return Response(serializer.data)


    def post(self, request, url):

        ####Auth
        account = get_account(request)

        bug_net = 20
        
        json_data = json.loads(request.body)
        try:
            
            bug_net = 22
            contest = Contest.objects.get(url = url)
            contest_id = contest.id

            total_points = 0

            i = 0
            high = len(json_data)

            for name in json_data: 

                try:
                    contestant = Contestant.objects.get(contestant = name, contest_id = contest_id)
                    v = high - i
                    p = contestant.points
                    x = v + p
                    contestant.points = x
                    contestant.save()

                    total_points = total_points + x
                    
                except:
                    pass

                i = i + 1


            
            
            for rank in json_data: 

                try:
                    contestant_r = Contestant.objects.get(contestant = rank , contest_id= contest_id)
                    
                    rank = contestant_r.points * 100 / total_points
                    contestant_r.rank = rank
                    contestant_r.save()
                
                except:
                    pass



            result = Contestant.objects.filter(contest_id = contest_id)
            
            serializer = ContestantSerializer(result, many = True)
            return Response(serializer.data)
            



        except:

            error = 'Oops Something broke, please refresh and try again'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)
            
            

        





class RankResult(APIView):

    def get(self, request, url):

        try: 
            account = get_account(request)

            try:
                contest = Contest.objects.get(url = url)

                try: 
                    contest = Contest.objects.get(url = url, account_id = account.id)
                    contest_id = contest.id 

                    result = Contestant.objects.filter(contest_id = contest_id)
            
                    serializer = ContestantSerializer(result, many = True)
                    return Response(serializer.data)

                except: 
                    error = 'Sorry you do not have permission to access this page.'
        
                    err = {
                        'error' : error
                    }
                    serializer = ErrorCheckSerializer( err, many=False)

                    return Response(serializer.data)


            except:
                error = 'Sorry wrong address, check the url and try again'
        
                err = {
                    'error' : error
                }
                serializer = ErrorCheckSerializer( err, many=False)

                return Response(serializer.data)

            

            

        except:
            error = 'You must be logged in to access this page.'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)
        
        

    def post(self, request):
        pass
        

































class RankPrivateVote(APIView):

    def get(self, request, url):
        
        contest = Contest.objects.all()

        serializer = ContestSerializer( contest, many=True)
        return Response(serializer.data)


    def post(self, request, url):

        bug_net = 20
        
        json_data = json.loads(request.body)

        # check private voter
        try:
            private_voter = PrivateVoter.objects.get(url = url)
        except:

            error = 'Oops wrong link, wrong turn!'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)

        
        # check if private voter has voted
        try:
            private_voter = PrivateVoter.objects.get(url = url, is_vote = True)

            error = 'Looks like you have voted already!'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)

        except:

            pass

            

        try:
            
            bug_net = 22
            contest_id = private_voter.contest_id

            total_points = 0

            i = 0
            high = len(json_data)

            for name in json_data: 

                try:
                    contestant = Contestant.objects.get(contestant = name, contest_id = contest_id)
                    v = high - i
                    p = contestant.points
                    x = v + p
                    contestant.points = x
                    contestant.save()

                    total_points = total_points + x
                    
                except:
                    pass

                i = i + 1


            
            
            for rank in json_data: 

                try:
                    contestant_r = Contestant.objects.get(contestant = rank , contest_id= contest_id)
                    
                    rank = contestant_r.points * 100 / total_points
                    contestant_r.rank = rank
                    contestant_r.save()
                
                except:
                    pass


            private_voter.is_vote = True
            result = Contestant.objects.filter(contest_id = contest_id)
            
            serializer = ContestantSerializer(result, many = True)
            return Response(serializer.data)
            



        except:

            error = 'Oops Something broke, please refresh and try again'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)
            
































class MyRTList(APIView):

    def get(self, request):
        
        account = get_account(request)
        contest = Contest.objects.filter(account_id = account.id)

        serializer = ContestSerializer( contest, many=True)
        return Response(serializer.data)


    def post(self, request):
        pass

















class MyAdmin(APIView):

    def get(self, request):
        
        account = Account.objects.all()

        serializer = AccountSerializer( account, many=True)
        return Response(serializer.data)


    def post(self, request):
        pass
























class RankTitle(APIView):

    def get(self, request, url):
        
        try: 
            contest = Contest.objects.get(url = url)

            serializer = ContestSerializer(contest, many=False)
            return Response(serializer.data)

        except: 
            pass

        return Response(False)

    def post(self, request):
        pass



















class PrivateRankTitle(APIView):

    def get(self, request, url):
        
        try: 
            private = PrivateVoter.objects.get(url = url)
            contest = Contest.objects.get(id = private.contest_id)

            serializer = ContestSerializer(contest, many=False)
            return Response(serializer.data)

        except: 
            pass

        return Response(False)

    def post(self, request):
        pass


















class RankTanker(APIView):

    def get(self, request, url):
        
        try:
            contest = Contest.objects.get(url = url)

            contestant = Contestant.objects.filter(contest_id = contest.id)

            bucket = []   

            i = 0
            for c in contestant:

                buffer = {
                    'id': i,
                    'contestant': c.contestant,
                }

                i = i + 1

                bucket.append(buffer)

            serializer = ContestantTankerSerializer( bucket, many=True)
            return Response(serializer.data)
        
        except:
            pass


        return Response(False)


    def post(self, request):
        pass
        
        



                
                



















class ResetPasswordEmail(APIView):

    def get(self, request):
        pass

    def post(self, request):

        try: 
            email_adr = request.POST.get("email","")
            account = Account.objects.get(email = email_adr)

            reset_code = url_code_generator()

            forgotPassword = ForgotPassword()
            forgotPassword.account = account
            forgotPassword.reset_code = reset_code
            forgotPassword.save()

            message = 'RankTank Password Recovery: ' + name + '\n\nHello dear, use this RankTank link to reset your password -> http://127.0.0.1:3000/reset_password/' +  str(reset_code) + '\n\n RankTank, fair and smooth!\n'
            email = EmailMessage('RankTank Password Recovery', message, to=[email_adr])
            email.send()


            code = 'Password Recovery details sent to your email at ' + email_adr
            success = {
                'code' : code
            }

            serializer = SuccessSerializer(success, many = False)
            return Response(serializer.data)

        
        except:
           
            error = 'Account with this email, doesnt exist'
        
            err = {
                'error' : error
            }
            serializer = ErrorCheckSerializer( err, many=False)

            return Response(serializer.data)
    

        
        
        error = 'Account with this email, doesnt exist'
        
        err = {
            'error' : error
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


       
        