from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Profile,Balance,Entry
from django.contrib.auth.hashers import make_password





class ProfileSerializer(serializers.ModelSerializer):
	
	validatedcode=serializers.CharField(required=False,write_only=True,allow_blank=True)
	address=serializers.CharField(required=False,allow_blank=True)
	phone=serializers.CharField(required=False,allow_blank=True)
	city=serializers.CharField(required=False,allow_blank=True)
	country=serializers.CharField(required=False,allow_blank=True)
	class Meta:
		model = Profile
		fields =('address','phone','city','country','validatedcode')
		

class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()
	password=serializers.CharField(write_only=True,required=False)
	is_active=serializers.BooleanField(write_only=True,required=False)
	
	class Meta:
		model = User
		fields=('id','username','password','email','first_name','last_name','is_active','profile')
	

	
	def create(self,validated_data):
		
		profile = validated_data.pop('profile')
		
		validated_data['password']=make_password(validated_data.get('password',None))
		user = User.objects.create(**validated_data)
		profileRec=Profile.objects.create(user=user,**profile)
		
		
		return user
		
	
	def update(self,instance,validated_data):
		
		profile_data = validated_data.pop('profile')
		
		profile=instance.profile
		
		instance.first_name=validated_data.get('first_name',instance.first_name)
		instance.last_name=validated_data.get('last_name',instance.last_name)
		instance.email=validated_data.get('email',instance.email)
		#instance.is_active=validated_data.get('is_active',instance.is_active)
		
		instance.save()
		
		profile.phone=profile_data.get('phone',profile.phone)
		profile.address=profile_data.get('address',profile.address)
		profile.city=profile_data.get('city',profile.city)
		profile.country=profile_data.get('country',profile.country)
		
		profile.save()
		
		return instance
		


class BalanceSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(required=False,read_only=True)
	isclosed=serializers.BooleanField(required=False)
	
	class Meta:
		model=Balance
		fields=('id','profile','year','month','balance','balance_update','isclosed',)
		read_only_fields=('created','updated')
		
		
			
	
	def get_validation_exclusions(self,*args, **kwargs):
		excls=super(BalanceSerializer,self).get_validation_exclusions()
		
		return excls+['profile']
	
	def create(self,validated_data):
	
		profile = validated_data.pop('profile')
		newinstance=Balance(user=profile,isclosed=False,**validated_data)
		newinstance.save()
		return newinstance
	
	def update(self,instance,validated_data):
		
		instance.isclosed=validated_data.get('isclosed',instance.isclosed)
		instance.balance=validated_data.get('balance',instance.balance)
		instance.balance_update=validated_data.get('balance_update',instance.balance_update)
		instance.month=validated_data.get('month',instance.month)
		instance.year=validated_data.get('year',instance.year)
		
		instance.save()
		
		##return instance
		
		
		if instance.isclosed == True:
			
			b=instance.balance_update
			m = instance.month
			m=m+1
			y = instance.year
			if m > 12:
				m=1
				y=y+1
				
			
			
			profile=validated_data.pop('profile')
			
			newinstance=Balance(year=y,month=m,balance_update=b,balance=b,isclosed=False,user=profile)
			newinstance.save()
			
		
		return instance
		

class EntrySerializer(serializers.ModelSerializer):
	balance=BalanceSerializer(required=False,read_only=True)
	
	op_beleg=serializers.CharField(allow_blank=True,required=False,allow_null=True)
	konto=serializers.CharField(allow_blank=True,required=False,allow_null=True)
	uid_lieferant_kunde=serializers.CharField(allow_blank=True,required=False,allow_null=True)
	kostenstelle=serializers.CharField(allow_blank=True,required=False,allow_null=True)
	#id=serializers.IntegerField(required=False)
	
	class Meta:
		model=Entry
		fields=('id','balance','tag','beleg','op_beleg','konto','uid_lieferant_kunde','text','kostenstelle','konto','ust_code','steuersatz','eingang','ausgang','skonto','saldo')
		read_only_fields=('created','updated')
		
	

	def get_validation_exclusions(self,*args, **kwargs):
		excls=super(EntrySerializer,self).get_validation_exclusions()
		
		return excls+['balance']
		
		
	def create(self,validated_data):
		entry=Entry(**validated_data)
		entry.save()
		balance=entry.balance
		balance.balance_update=balance.balance_update+entry.eingang-entry.ausgang
		balance.save()
		
		return entry