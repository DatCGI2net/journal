import json
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from rest_framework import  status, views, authentication, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser
from app.serializers import UserSerializer,BalanceSerializer,EntrySerializer
from app.models import Profile,Balance, Entry
from django.db.models import Sum
import re
from random import randint
from django.core.mail import send_mail,mail_admins
from django.http import HttpResponse
import csv

class AppDebug(object):
	
	def debug(self,text):
		import sys
		print sys.stderr, text
		

def unautorized_response():
		return Response({'status':'unauthorized', 'message':'Please login'}, status=status.HTTP_403_FORBIDDEN)		

class APIProfileView(views.APIView):
	permissions_classes=(permissions.IsAuthenticated,)
	authentication_classes= (authentication.SessionAuthentication, authentication.BasicAuthentication,)
	serializer_class = UserSerializer
	
	def put(self,request):
		postData=request.data
		user = User.objects.get(pk=postData['id'])
		serializer = UserSerializer(user,data=postData)
		
		if serializer.is_valid():
			serializer.save()
			res=ResponseRes.get_serializer_res(serializer,'Profile has been updated successfully')
			
			
			
			return Response(res)
		
		return Response({'status': 'Modify error', 
						'message':'Profile could not be modified. Reason:' + ResponseRes.get_serializer_error(serializer.errors)}, 
					status=status.HTTP_400_BAD_REQUEST)
			
		
	def get(self,request):
		anonUser = AnonymousUser()
		
		if request.user is not anonUser:
			serializer = UserSerializer(request.user)
			print serializer
			
			return Response(serializer.data)
		
		return Response({'status': 'Profile error', 
						'message':'Profile could not be found. Reason:' + 'User has not been logged in'}, 
					status=status.HTTP_400_BAD_REQUEST)


class APIEntryView(views.APIView):
	permissions_classes=(permissions.IsAuthenticated,)
	authentication_classes= (authentication.SessionAuthentication, authentication.BasicAuthentication,)
	serializer_class = EntrySerializer
	
	def get(self,request):
		data = request.query_params
		
		userid=data.get('id')
		### entry, this method is ridiculous
		if userid is not None:
			entry=Entry.objects.get(pk=userid)
			
			return Response({'entry': EntrySerializer(entry).data, 'status':'success'})
			
		#return Response(data)
		
		userid=request.user.id
		balance_id=data.get('balance_id')
		#entries = Entry.getEntries(balance_id)
		entries = Entry.objects.all().filter(balance_id=balance_id).order_by('tag')
		
		totals={'eingang':0, 'ausgang':0,'skonto':0, 'saldo':0}
		for entry in entries:
			totals['eingang']+=entry.eingang
			totals['ausgang']+=entry.ausgang
			totals['skonto']+=entry.skonto
			totals['saldo']=entry.saldo
			
		
		res = EntrySerializer(entries,many=True).data
		return Response({'entries': res, 'totals': totals, 'status':'success'})
		
		
		
	def post(self,request):
	
		return self.updateEntry(postData=request.data)
		
		
	def updateEntry(self,postData):
		
			
		postData['saldo']=0;
		
		balance_id=postData.pop('balance_id')
		
		serializer=self.serializer_class(data=postData)
		is_valid=serializer.is_valid()
		###return Response({'user': UserSerializer(request.user)});
		
		
		if is_valid :
			balance = Balance.objects.get(id=balance_id)
			
			serializer.save(balance=balance)
			res = serializer.data
			res['status']='success'
			
			balance.updateEntries()
			
			return Response(res,status=status.HTTP_201_CREATED)
		
		
		
		return Response({'status': '', 'message':'Balance could not be created', 'data': serializer}, status=status.HTTP_400_BAD_REQUEST)
	
		
		
		
	def put(self,request):
		postData=request.data
		#balancex=postData.pop('balance')
		#postData['balance_id']=balance.get('id')
		entry = Entry.objects.get(pk=postData['id'])
		serializer=self.serializer_class(entry,data=postData, partial=True)
		is_valid=serializer.is_valid()
	
		
		##return Response({'is_valid': is_valid, 'data': request.data, 'error': self.get_serializer_error(serializer.errors)});
		
		
		if is_valid :
			balance=entry.balance
			#balance = Balance.objects.get(id=balancex['id'])
			#balance=BalanceSerializer(data=balancex)
			
			#serializer.save(balance=balance)
			serializer.save()
			res = serializer.data
			res['status']='success'
			balance.updateEntries()
			#balance.updateEntries()
			
			return Response(res,status=status.HTTP_202_ACCEPTED)
		
		
		
		return Response({'status': '', 'message':'Balance could not be updated', 'data': serializer.data , 'error': ResponseRes.get_serializer_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

		"""		
	def get_serializer_error(self,errors):
	
		##errors  = serializer.errors
		error=""
		for k in errors.keys():
			error+=k+":" +',,,'.join(errors[k]) +","
		
		return error	
		
		"""
	
	def delete(self,request):
		id=re.search("(\d+)$",request.path).group()
		
		##return Response({'status': 'success', 'id': id})
		
		entry=Entry.objects.get(pk=id)
		balance=entry.balance;
		entry.delete()
		balance.updateEntries()
		return Response({'status': 'success', 'id': id})
		

class APIDashboarView(views.APIView, AppDebug):
	
	permissions_classes=(permissions.IsAuthenticated,)
	authentication_classes= (authentication.SessionAuthentication, authentication.BasicAuthentication,)
	serializer_class = BalanceSerializer
	
	
	
	def get(self, request):
		
		if request.user.is_authenticated() :
			balances = Balance.objects.filter(user=request.user).order_by('-year','-month')
			balance = None
			
			if balances.exists():
				balance = balances[0]
				
			
			serializer = self.serializer_class(balance)
			
			Response(serializer.data)
		
		return unautorized_response()	
		
	def post(self, request):
		
		if request.user.is_authenticated() :
				
			serializer = self.serializer_class(request.data)
			if serializer.is_valid():
				balance = serializer.save()
				serializer = self.serializer_class(balance)
				Response(serializer.data)
				
			return Response({'status':'error', 
							'message':serializer.error_messages}, 
						status=status.HTTP_400_BAD_REQUEST)	
		
		return unautorized_response()
	
class APIBalanceView(views.APIView,AppDebug):

	permissions_classes=(permissions.IsAuthenticated,)
	authentication_classes= (authentication.SessionAuthentication, authentication.BasicAuthentication,)
	serializer_class = BalanceSerializer

	def get(self, request):
		
		if request.user.is_authenticated() :
	
			data = request.query_params
			
			
			#return Response(data)
			
			#user_id = request.user.id
			balance_id=data.get('balance_id')
			month = data.get('month')
			year = data.get('year')
			
			if balance_id=='undefined':
				balance_id=None
			elif int(balance_id) <= 0:
				balance_id=None
				
			##btype = type(balance_id)
			profiles = Profile.objects.filter(user=request.user)
			profile=None
			if profiles is not None and profiles.count() > 0:
				profile = profiles[0]
			else:
				profile=Profile(user=request.user,address='address')
				profile.save()
				
				
			##return Response({'user_id':user_id, 'btype':btype})
			
			balances = Balance.objects.all()
			balances=balances.filter(user=profile)
			earliestBalance=None
			latestBalance=None
			if(len(balances)>0):
				earliestBalance=balances[0]
				latestBalance=balances.order_by('-created')[0]
				
			
				if balance_id is not None :
					self.debug('balance_id:'+balance_id)
					balances=balances.filter(id=balance_id)
				
				### filter by year, monht
				if len(balances) > 0:
					balances=balances.filter(month=month,year=year)
				
					
				
				
					if len(balances) > 0:
						balances=balances.order_by('created')
						
						return self._resBlance(balances[0],earliestBalance,latestBalance)
						
						"""
						serializer = self.serializer_class(balances[0])
						
						res=serializer.data
						if(earliestBalance is not None):
							res['earliestdate']="1-%s-%s" % (earliestBalance.month,earliestBalance.year,)
							
						if(latestBalance is not None):
							res['latestdate']="1-%s-%s" % (latestBalance.month,latestBalance.year,)	
							
						return Response(res)
						"""
						
					else:
						return self._resBlance(latestBalance,earliestBalance,latestBalance)
						
				else:
					return self._resBlance(latestBalance,earliestBalance,latestBalance)
				
			else:
				return self._resBlance()
			
			
			
		
		return unautorized_response()
		
	def _resBlance(self,balance=None,earliestBalance=None,latestBalance=None):
		res = {'status':'no record'}
		if balance is not None:
			serializer = self.serializer_class(balance)
					
			res=serializer.data
		if(earliestBalance is not None):
			res['earliestdate']="%02d-01-%s" % (earliestBalance.month,earliestBalance.year,)
				
		if(latestBalance is not None):
			res['latestdate']="%02d-01-%s" % (latestBalance.month,latestBalance.year,)	
		return Response(res)
			
			
		
	def put(self,request,format=None):
	
		postData=request.data
		balance=Balance.objects.get(pk=postData['id'])
		
		
		
		
	
		serializer=self.serializer_class(balance,data={'isclosed': True},partial=True)
		return self._updateBalance(serializer,request.user)
	
	def _updateBalance(self,serializer,user):
	
		if serializer.is_valid() :
			profile = Profile.objects.get(user=user)
			
			serializer.save(profile=profile)
			res = serializer.data
			res['status']='success'
			
			return Response(res,status=status.HTTP_201_CREATED)
			
			
			
		return Response({'status': '', 'message':'Balance could not be created', 'data': serializer}, status=status.HTTP_400_BAD_REQUEST)
			
			
			
		
		
	def post(self,request,format=None):
		""" check """
		if request.user.is_authenticated() :
			postData=request.data
			#postData['user_id']=request.user
			#postData['isclosed']=False
			postData['balance_update']=postData['balance']
			##return Response(postData)
			
			serializer=self.serializer_class(data=postData)
			
			return self._updateBalance(serializer,request.user)
			
			
			is_valid=serializer.is_valid()
			###return Response({'user': UserSerializer(request.user)});
			
			
			if is_valid :
				profile = Profile.objects.get(user=request.user)
				
				serializer.save(profile=profile)
				res = serializer.data
				res['status']='success'
				
				return Response(res,status=status.HTTP_201_CREATED)
			
			
			
			return Response({'status': '', 'message':'Balance could not be created', 'data': serializer}, status=status.HTTP_400_BAD_REQUEST)
	
		return Response({'status':'unauthorized', 'message':'Please login'}, status=status.HTTP_403_FORBIDDEN)

class AppViews(View):
	def get(self,request):
		
		id=request.GET.get('id',None)	
		
		
			
		
		if id is not None:
			
			balance  = Balance.objects.get(pk=id)
			if balance is not None:
				
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition']='attachment; filename="entries_of_%s_%s.csv"' % (balance.year,balance.month,)
				
				
				entries = Entry.objects.filter(balance=balance)
				
				
				
				
				writer = csv.writer(response)
				writer.writerow(['Tag','beleg','text','eingang','ausgang','saldo'])
				for row in entries:
				
					writer.writerow([row.tag,row.beleg,row.text,row.eingang,row.ausgang,row.saldo])
					
				return response
			
			
			
		
		return render(request,'app/index.html',{
		'title': 'Good to go'
		})

	
		
		
	

class APIUserView(views.APIView):

	def get_validationcode(self):
		seed="abcdefghijklmnopqstuxyw01234567890"
		val=""
		l=len(seed)
		for c in range(4):
			i = randint(0,l)
			val+= seed[i]
			
				
		return val
		
	def post(self,request,format=None):
		postData=request.data
		postData['is_active']=False
		postData['profile']['validatedcode']= self.get_validationcode()
		
		serializer=UserSerializer(data=postData)
		if serializer.is_valid() :
			serializer.save()
			
			## send email
			pending_message="Hello %s,\n\nThank you for your registration.\n Your account is pendinng. We will review and activate in a due course and send you a notification then.\nRegards,\nSite admin\n\n" % (serializer.data['first_name'],)
			
			send_mail("Pending account",pending_message,"admin@cgito.net",[serializer.data['email']], fail_silently=True)
			
			url="http://%s/accounts/validate" % (request.get_host,)
			pending_message="Hello %s,\n\nA new account as been added. Please reivew and activate it by clicking on the below url:\n%s\n\nSite admin\n\n" % ('Admin',url,)
			mail_admins("Pending account",pending_message, fail_silently=True)
			
			
			return Response(serializer.data)
		
		error =ResponseRes.get_serializer_error(serializer.errors)
		
		return Response({
			'status': 'Failed',
			'message': 'This account could not be created. Reason:' + error})

		
	def get(self,request,format=None):
		pass
		
	
	def put(self,request,format=None):
		postData=request.data
		code=postData['code']
		
		profile=Profile.objects.get(validatedcode=code)
		
		if not code or not profile:
			error = "code could not be found"
			return Response({
			'status': 'Failed',
			'message': 'This account could not be created. Reason:' + error}, status=status.HTTP_401_UNAUTHORIZED)
		
		user = profile.user
		user.is_active=True
		user.save()
		serializedUser=UserSerializer(user)
		return Response(serializedUser.data)
	
class APIAuthView(views.APIView):

	
	def post(self,request,format=None):
		"""
		check if already login
		"""
		data=json.loads(request.body)
		
		if request.user.is_authenticated() :
			serialized=UserSerializer(request.user)
			return Response(serialized.data)
			
			user = data.get('user',data)
			
			if user == request.user:
			
				serialized=UserSerializer(request.user)
				return Response(serialized.data)
			
			else:
				logout(request)
				
				
		
		user = data.get('user',None)
		##return Response(user)
		
		username=user['email']
		password=user['password']
		##return Response({'email':username, 'pw':password})
		
		#username='test@cgito.net'
		#password='test12345'
		##return Response({'email':username, 'pw':password})
		user = authenticate(username = username, password = password)
		##return Response(UserSerializer(user).data)
		if user is not None:
			if user.is_active:
				login(request,user)
				serialized=UserSerializer(user)
				return Response(serialized.data)
			else:
				return Response({
					'status': 'Unauthorized',
					'message': 'This account has been disabled'})
		else:
			return Response({
					'status': 'Unauthorized',
					'message': 'Username/password combination invaid'}, status=status.HTTP_401_UNAUTHORIZED)
		
			
	def get(self,request):
		if request.user.is_authenticated() :
			serialized=UserSerializer(request.user)
			return Response(serialized.data)
			
		return Response({})
		
	def delete(self,request,format=None):
		logout(request)
		return Response({'status':'Logged out'})
		


class ResponseRes():

	@staticmethod
	def get_serializer_error(errors):
	
		##errors  = serializer.errors
		error=""
		for k in errors.keys():
			error+=k+":" +',,,'.join(errors[k]) +","
		
		return error

	@staticmethod
	def get_serializer_res(serializer,message):	

		res=serializer.data
		res['status']='success'
		res['message']=message
		
		return res
		
		
		

		
		
			
