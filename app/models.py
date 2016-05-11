from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	phone=models.TextField(max_length=20,null=True,blank=True)
	address=models.TextField(max_length=200,null=True,blank=True)
	city=models.TextField(max_length=20,null=True,blank=True)
	country=models.TextField(max_length=20,null=True,blank=True)
	zipcode=models.TextField(max_length=20,null=True,blank=True)
	validatedcode=models.CharField(max_length=20,null=True,blank=True)
	created=models.DateTimeField(auto_now_add=True)
	
	REQUIRED_FIELDS = ['phone']
	
	def __str__(self):
		return self.user.email
	def __unicode__(self):
		return self.user.email	
	
class Balance(models.Model):
	""" Balance model """
	user = models.ForeignKey("Profile",on_delete=models.CASCADE,)
	balance = models.FloatField()
	balance_update = models.FloatField()
	year = models.PositiveSmallIntegerField()
	month = models.PositiveSmallIntegerField()
	isclosed = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def list(self,uid):
	
		return self.objects.all().filter(user_id=uid).order_by('created')
		
	def updateEntries(self):
	
		entries = Entry.objects.filter(balance_id=self.id)
		
		start_balance=self.balance
		for e in entries:
			e.saldo=start_balance+e.eingang-e.ausgang
			e.save()
			start_balance=e.saldo
			
		
		self.update_balance=start_balance
		
		self.save()
		
	
class Entry(models.Model):
	""" Entry of a blance """
	balance=models.ForeignKey("Balance",on_delete=models.CASCADE,)
	tag	= models.DateField()
	beleg= models.TextField()
	op_beleg=models.TextField(null=True,blank=True )
	konto=models.TextField(null=True,blank=True )
	ust_code=models.PositiveSmallIntegerField()
	uid_lieferant_kunde=models.TextField(null=True,blank=True )
	text=models.TextField()
	kostenstelle=models.TextField(null=True,blank=True )
	steuersatz=models.PositiveSmallIntegerField()
	eingang = models.FloatField()
	ausgang = models.FloatField()
	skonto = models.FloatField()
	saldo = models.FloatField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	"""
	def getEntries(self,balance_id):
	
		entries=self.balance_id=balance_id
		return entries.order_by('tag')
	"""	
