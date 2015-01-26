from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from .models import Article, Content, Issue , Subscriber, ShopItem# '.' signifies the current directory
from .models import Article, Content, Issue # '.' signifies the current directory
from collections import OrderedDict
import json
import stripe
from django.conf import settings
from django.core import serializers
# Create your views here.
def index(request):
	issue = Issue.objects.first()

# for each article with this issue id
	articles_in_issue = Article.objects.filter(issue=issue)
	data = {
		'fiction': [],
		'features': [],
		'poetry': [],
		'art': []
	}
	# for article in articles_in_issue:
	# 	data[article.section].append(article)

	#template_name = 'index_v1.html',
	template_name = 'current_issues.html'
	return render_to_response(template_name, data, context_instance=RequestContext(request))



def article(request, slug):
	article = get_object_or_404(Article, slug=slug)
	data = {
		'article': article
	}
	template_name = 'article.html'
	return render_to_response(template_name, data, context_instance=RequestContext(request))

def issues(request):
	all_issues = Issue.objects.all()
	season = {'Winter': 0, 'Spring': 1, 'Commencement': 2, 'Fall': 3}
	all_issues_sorted = reversed(sorted(all_issues, key=lambda i: i.year))
	#all_issues_sorted = reversed(sorted(all_issues, key=lambda i: i.year * 10 + season[i.issue]))
	data = {
		'issues': all_issues_sorted
	}
	template_name = 'issues.html'
	return render_to_response(template_name, data, context_instance=RequestContext(request))

def masthead(request):
	template_name = 'about_us.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def singleissue(request, season, year):
	template_name = 'singleissue.html'
	issue = get_object_or_404(Issue, issue__iexact=season, year=year)

	issue_content = Content.objects.filter(issue=issue)
	section = ('Art','Features','Fiction','Poetry')
	content = OrderedDict()
	for s in section:
		content[s] = issue_content.filter(section__name=s)
	print content
	data = {
		'issue' : issue,
		'content_list' : content
		}

	return render_to_response(template_name, data, context_instance=RequestContext(request))

def subscribe(request):
	template_name = 'subscribe.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def stripeSubmit(request):
	# Get the credit card details submitted by the form
	token = request.POST['stripeToken']
	stripe.api_key = settings.STRIPE_SECRET_KEY
	# Create the charge on Stripe's servers - this will charge the user's card
	try:
	  	charge = stripe.Charge.create(
		    amount=123, # amount in cents, again
		    currency="usd",
		    card=token,
		    description="payinguser@example.com",
	  	)


		subscriber = Subscriber.objects.create(
			name=request.POST['name'], 
			email=request.POST['email'],
			streetAddress1=request.POST['streetAddress1'],
			streetAddress2=request.POST['streetAddress2'],
			city=request.POST['city'],
			state=request.POST['state'],
			country=request.POST['country'],
			zipCode=request.POST['zipCode'],
			renew=request.POST['renew'],
			subscriptionType=request.POST['subscriptionType'],
		)
		return subscribe(request)
	except stripe.CardError, e:
	  # The card has been declined
	  pass

def submit(request):
	template_name = 'submit.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def donate(request):
	template_name = 'donate.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def contact(request):
	template_name = 'contact_us.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def alumni(request):
	template_name = 'alumni.html'
	return render_to_response(template_name, context_instance=RequestContext(request))

def advertise(request):
	template_name = 'advertise.html'

	return render_to_response(template_name, context_instance=RequestContext(request))

def shop(request):
	#shopItems =  serializers.serialize('json',ShopItem.objects.all())
	shopItems = ShopItem.objects.all()
	template_name = 'shop.html'
	return render_to_response(template_name,dictionary = {"items":shopItems},  context_instance=RequestContext(request))

def comp(request):
	template_name = 'comp.html'
	return render_to_response(template_name, context_instance=RequestContext(request))