from django.shortcuts import render,redirect
from .models import User,Product,Cart,Address
from django.conf import settings
from django.core.mail import send_mail
import random
import datetime
import razorpay


a=random.randint(1,9)
b=random.randint(1,9)
c=random.randint(1,9)
d=random.randint(1,9)

a=str(a)
b=str(b)
c=str(c)
d=str(d)

def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def blog(request):
	return render(request,'blog.html')

def blog_single(request):
	return render(request,'blog_single.html')



def contact(request):
	return render(request,'contact.html')

def product_single(request):
	return render(request,'product_single.html')



def shop(request):
	try:
		foruser=User.objects.get(email=request.session['email'])
		prod=Product.objects.all()
		return render(request,'shop.html',{'prod':prod})
	except:
		return redirect('login')

def buyer_prod_single(request,pk):
	prod=Product.objects.get(pk=pk)
	return render(request,'buyer_prod_single.html',{'prod':prod})


def signup(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="User already exist !!!!"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['pswd']==request.POST['cpswd']:
				user=User.objects.create(
					utype=request.POST['utype'],
					name=request.POST['name'],
					email=request.POST['email'],
					pswd=request.POST['pswd'],
					phn=request.POST['phn'],
					)
				return render(request,'login.html')
			else:
				msg="password and confirm password not matched !!!"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],pswd=request.POST['pswd'])
			cart=Cart.objects.filter(user=user)

			x=cart.count()
			request.session['cart_items']=x

			request.session['name']=user.name
			request.session['email']=user.email
			if user.utype=='buyer':
				return render(request,'index.html')
			else:
				return render(request,'seller_index.html')
		except:
			msg="email or password not matched !!!"
			return render(request,'login.html',{'msg':msg})

	else:
		return render(request,'login.html')

def logout(request):
	del request.session['email']
	del request.session['name']
	return redirect('index')

def fp_1(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			email=request.POST['email']

			subject = 'OTP Verification'
			message = f'Hi {user.name}, your OTP for changing the password is '+a+b+c+d
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )

			return render(request,'fp_2.html',{'email':email})
		except:
			msg="No Such User Exists !!!"
			return render(request,'fp_1.html',{'msg':msg})
	else:
		return render(request,'fp_1.html')


def fp_2(request):
	if request.method=='POST':
		user=User.objects.get(email=request.POST['email'])
		email=request.POST['email']
		if a==request.POST['a'] and b==request.POST['b'] and c==request.POST['c'] and d==request.POST['d']:
			return render(request,'fp_3.html',{'email':email})
		else:
			msg="OTP not matched !!!"
			return render(request,'fp_2.html',{'msg':msg})
		return render(request,'fp_2.html')
	else:
		return render(request,'fp_2.html')


def fp_3(request):
	if request.method=="POST":

		if request.POST['npswd']==request.POST['cnpswd']:
			user=User.objects.get(email=request.POST['email'])
			user.pswd=request.POST['npswd']
			user.save()
			return redirect('login')
		else:
			msg='New Password and Confirm New Password not mastched !!!'
			return render(request,'fp_3.html',{'msg':msg})
		return render(request,'fp_3.html')
	else:
		return render(request,'fp_3.html')


def seller_index(request):
	return render(request,"seller_index.html")

def add_prod(request):
	if request.method=='POST':
		try:
			foruser=User.objects.get(email=request.session['email'])
			prod=Product.objects.create(
				foruser=foruser,
				name=request.POST['name'],
				category=request.POST['category'],
				gender=request.POST['gender'],
				price=request.POST['price'],
				size=request.POST['size'],
				image=request.FILES['image'],
				desc=request.POST['desc'],
				date=datetime.datetime.now().strftime("%d-%m-%y"),
				time=datetime.datetime.now().strftime("%H:%M:%S"),
				)
			return render(request,'seller_index.html')
		except:
			msg="Error PLZ try agin later !!!"
			return render(request,'add_prod.html',{'msg':msg})
	else:
		return render(request,'add_prod.html')



def my_prod(request):
	foruser=User.objects.get(email=request.session['email'])
	prod=Product.objects.filter(foruser=foruser)
	return render(request,'my_prod.html',{'prod':prod})


def my_prod_single(request,pk):
	foruser=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk,foruser=foruser)
	return render(request,'my_prod_single.html',{'prod':prod})


def edit_my_prod(request,pk):
	foruser=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk,foruser=foruser)
	if request.method=='POST':
		prod.foruser=foruser

		if request.POST['name']=='':
			pass
		else:
			prod.name=request.POST['name']

		if request.POST['desc']=='':
			pass
		else:
			prod.desc=request.POST['desc']
			
		prod.price=request.POST['price']
		prod.date=datetime.datetime.now().strftime("%d-%m-%y")
		prod.time=datetime.datetime.now().strftime("%H:%M:%S")
		try:
			prod.size=request.POST['size']
			prod.image=request.FILES['image']
		except:
			pass
		prod.save()
		return render(request,'seller_index.html',{'prod':prod})
	else:
		return render(request,'edit_my_prod.html',{'prod':prod})


def delete_prod(request,pk):
	foruser=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk,foruser=foruser)
	prod.delete()
	return redirect('seller_index')


def add_to_cart(request,pk):
	
	user=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk)
	cart=Cart.objects.filter(user=user)

	Cart.objects.create(
		user=user,
		prod=prod
		)

	#adding total number of items in cart and displaying them in the header of cart
	c=0
	for i in cart:
		c+=1
	request.session['cart_items']=c
	return redirect('shop')

def cart(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)

	#calculating the total price
	price=0
	for j in cart:
		temp=j.prod.price
		temp=int(temp)
		price+=temp

	return render(request,'cart.html',{'cart':cart,'price':price})

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(pk=pk,user=user)
	cart.delete()

	#subtracting total number of items in cart and displaying them in the header of cart
	cc=Cart.objects.filter(user=user)
	x=cc.count()
	request.session['cart_items']=x

	return redirect('cart')


def checkout(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)

	x=cart.count()
	print(x)

	amount=0
	for i in cart:
		amount+=i.prod.price

	try:
		address=Address.objects.get(user=user)
		return redirect('payment')
	except:
		return render(request,'checkout.html',{'user':user,'amount':amount})



def billing_info(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		address=Address.objects.create(
			user=user,
			state=request.POST['state'],
			ship_address=request.POST['ship_address'],
			city=request.POST['city'],
			postal_code=request.POST['postal_code']
			)
		return redirect('payment')
	else:
		return render(request,'checkout.html')



def payment(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)

	x=cart.count()
	print("loooo",x)
	amount=0
	for i in cart:
		amount+=i.prod.price

	print("called")

	client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
	data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
	payment = client.order.create(data=data)

	for j in cart:
		print(j.prod.price)
		j.razorpay_order_id=payment['id']
		j.save()

	print("----------------",payment)

	return render(request,'payment.html',{'user':user,'amount':amount*100})



def t_shirts(request):
	try:
		prod=Product.objects.filter(category='t_shirts')
		count=0
		for i in prod:
			count+=1
		request.session['count']=count
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})

def casual_shirts(request):
	try:
		prod=Product.objects.filter(category='casual_shirts')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})

def formal_shirts(request):
	try:
		prod=Product.objects.filter(category='formal_shirts')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def sweatshirts(request):
	try:
		prod=Product.objects.filter(category='sweatshirts')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def sweaters(request):
	try:
		prod=Product.objects.filter(category='sweaters')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def jackets(request):
	try:
		prod=Product.objects.filter(category='jackets')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def blazers_coats(request):
	try:
		prod=Product.objects.filter(category='blazers_coats')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def winter_coats(request):
	try:
		prod=Product.objects.filter(category='winter_coats')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def jumpsuits(request):
	try:
		prod=Product.objects.filter(category='jumpsuits')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def jeans(request):
	try:
		prod=Product.objects.filter(category='jeans')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def casual_trousers(request):
	try:
		prod=Product.objects.filter(category='casual_trousers')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def formal_trousers(request):
	try:
		prod=Product.objects.filter(category='formal_trousers')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def shorts(request):
	try:
		prod=Product.objects.filter(category='shorts')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def track_pants_joggers(request):
	try:
		prod=Product.objects.filter(category='track_pants_joggers')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def wallets(request):
	try:
		prod=Product.objects.filter(category='wallets')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def belts(request):
	try:
		prod=Product.objects.filter(category='belts')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def perfumes_body_mists(request):
	try:
		prod=Product.objects.filter(category='perfumes_body_mists')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def trimmers(request):
	try:
		prod=Product.objects.filter(category='trimmers')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def deodorants(request):
	try:
		prod=Product.objects.filter(category='deodorants')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def phone_cases(request):
	try:
		prod=Product.objects.filter(category='phone_cases')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def helmets(request):
	try:
		prod=Product.objects.filter(category='helmets')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})


def rings_wristwear(request):
	try:
		prod=Product.objects.filter(category='rings_wristwear')
		return render(request,'shop.html',{'prod':prod})
	except:
		print("except block")
		msg="No such products available !!"
		return render(request,'shop.html',{'msg':msg})









