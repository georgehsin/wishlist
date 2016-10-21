from django.shortcuts import render, redirect
from .models import Users, Wishes #IMPORT OTHER MODELS HERE
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'wish/index.html')

def register(request):
	result = Users.loginmgr.register(request.POST['name'], request.POST['user'], request.POST['passw'], request.POST['confirm'])
	if result[0]:
		request.session['name'] = result[1].name
		request.session['id'] = result[1].id
		print request.session['id']
		return redirect('/dashboard')
	else:
		for error in result[1]:
			messages.error(request, error)
	return redirect('/')

def login(request):
	result = Users.loginmgr.login(request.POST['username'], request.POST['password'])
	if result[0]:
		request.session['name'] = result[1].name
		request.session['id'] = result[1].id
		print request.session['id']
		return redirect('/dashboard')
	else:
		for error in result[1]:
			messages.error(request, error)
	return redirect('/')

def home(request):
	return redirect('/dashboard')

def dashboard(request):
	users = Users.loginmgr.all()
	wishes = Wishes.objects.all()
	context = {'users':users, 'wishes':wishes}
	return render(request, 'wish/dashboard.html', context)

def create(request):
	return render(request, 'wish/create.html')

def adding(request):
	item = request.POST['item']
	if len(item)<3:
		messages.error(request, 'error')
		return redirect('wish_items/create')
	userinfo = Users.loginmgr.get(id = request.session['id'])
	wishlist = Wishes(item = request.POST['item'])
	wishlist.save()
	wishlist.user_id.add(userinfo)
	return redirect('/dashboard')

def selfadd(request, id):
	userinfo = Users.loginmgr.get(id = request.session['id'])
	product = Wishes.objects.get(id = id)
	item = product.item
	wishlist = Wishes(item = item)
	wishlist.save()
	wishlist.user_id.add(userinfo)
	return redirect('/dashboard')

def product(request, id):
	products = Wishes.objects.all()
	productid = Wishes.objects.get(id = id)
	print products
	print productid.user_id
	users = Users.loginmgr.all()
	context = {'products':products, 'users':users, 'productid':productid}
	return render(request, 'wish/product.html', context)

def delete(request, id):
	Wishes.objects.filter(id = id).delete()
	return redirect('/dashboard')

def logout(request):
	request.session.flush()
	return redirect ('/')