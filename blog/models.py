from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.utils.safestring import SafeUnicode
from app.models import Profile


"""
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	website = models.CharField(max_length=255)
	def __str__(self):
		return self.user.username
"""		
	
class Post(models.Model):
	poster = models.ForeignKey('app.Profile', on_delete = models.CASCADE,)
	title = models.CharField(max_length =100, null = False)
	text  = models.TextField()
	pub_date=models.DateTimeField('date publish')
	
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	def __str__(self):
		return self.title
		
	def get_comments(self):
		##comments=Comment.objects.filter(post_id=self.id)
		comments=Comment.objects.filter(post=self.id, status=Comment.APPROVED)
		return comments
		
	def get_absolute_url(self):
		return "/blog/%i/" % self.id 
		
	
	
class Comment(models.Model):
	APPROVED='approved'
	UNAPPROVED='unapproved'
	SPAMMED='spammed'
	DELETED='deleted'
	COMMENT_CHOICES =((APPROVED,'Approved'),(UNAPPROVED,'Unapproved'),(SPAMMED,'Spammed'), (DELETED,'Deleted'))
	commenter=models.ForeignKey('app.Profile', on_delete=models.CASCADE,)
	#post_id=models.ForeignKey('Post',on_delete=models.CASCADE,)
	post=models.ForeignKey('Post',on_delete=models.CASCADE,)
	comments=models.TextField('Comments', null = False)
	comment_date=models.DateTimeField('date comment')
	status=models.CharField(max_length=10, choices=COMMENT_CHOICES,default=UNAPPROVED)
	
	def get_recent_comments(self):
		return self.comment_date <= timezone.now() - datetime.timedelta(days=5)
		
	def __str__(self):
		return SafeUnicode(self.comments)[:20]
		
	
	
	
	
