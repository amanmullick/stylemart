from django.db import models

# Create your models here.

class User(models.Model):
	utype=models.CharField(max_length=100,default="buyer")
	name=models.CharField(max_length=100)
	email=models.EmailField()
	pswd=models.CharField(max_length=100)
	phn=models.IntegerField()

	def __str__(self):
		return self.email+" - "+self.utype

class Product(models.Model):
	foruser=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=100)
	category=models.CharField(max_length=100)
	gender=models.CharField(max_length=50)
	size=models.CharField(max_length=100)
	price=models.IntegerField()
	image=models.ImageField(upload_to='images/')
	desc=models.CharField(max_length=500)
	date=models.CharField(max_length=100)
	time=models.CharField(max_length=100)

	def __str__(self):
		return self.foruser.name+'-'+self.name+'-'+str(self.price)


class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	prod=models.ForeignKey(Product,on_delete=models.CASCADE)
	payment_status=models.CharField(max_length=50,default=False)
	razorpay_payment_id=models.CharField(max_length=100, null=True, blank=True)
	razorpay_order_id=models.CharField(max_length=100, null=True, blank=True)
	razorpay_signature=models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.user.name+"-"+self.prod.name+'-'+str(self.prod.price)

class Address(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	state=models.CharField(max_length=100)
	ship_address=models.CharField(max_length=100)
	city=models.CharField(max_length=50)
	postal_code=models.CharField(max_length=50)

	def __str__(self):
		return self.user.name+'-'+self.ship_address
