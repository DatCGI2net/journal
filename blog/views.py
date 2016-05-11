from django.shortcuts import get_object_or_404, render,redirect

#from django.http import HttpResponse
#from django.template import loader
from .models import Post,Comment,Profile
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib.auth.decorators import login_required
from django.utils import timezone



def index(request):
	#return HttpResponse("Hello, world. You're at the polls index.")
	latest_post_list=Post.objects.order_by('-pub_date')[:5]
	##template=loader.get_template('blog/index.html')
	context={
		'latest_post_list': latest_post_list,
	}
	return render(request,'blog/index.html',context)
	
def detail(request,post_id):
	post=get_object_or_404(Post, pk=post_id)
	comments = post.get_comments()
	count = len(comments)
	return render(request,'blog/post_detail.html',{'post': post, 'comment_count': count, 'comments': comments})
	
def comments(request,post_id):
	pass

@login_required(login_url = '/blog/login/')
def comment(request,post_id):
	post=get_object_or_404(Post,pk=post_id)

	if len(request.POST):
		comment = Comment()
		profile = Profile.objects.get(pk=request.user.id)
		comment.commenter=profile
		comment.comments=request.POST['comments']
		comment.post=post
		comment.comment_date=timezone.now()
		comment.save()
	
	return redirect(post)
	
def login_user(request):
	if(len(request.POST)):
	
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				## redirect_to
				url=request.POST['url']
				if url:
					if "login" in url:
						url="/blog/"
						
				if not url:
					url="/blog/"
					
						
				return redirect(url)
				
			else:
				return render(request,'blog/login.html',{error: 'disabled'})
		else:
			return render(request,'blog/login.html',{error: 'invalid account'})
	
	url = request.GET['next']
	if not url:
		url='/'
		
	return render(request,'blog/login.html', {'url': url})
	
def logout_user(request):
	logout(request)
	return render(request,'blog/login.html')
	
def about(request):

	pass
	
def contact(request):

	pass
	
	
	
	
	
	
	
