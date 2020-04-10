from mongoengine import *

connect('Farmers')

class Comment(EmbeddedDocument):
	content = StringField()
	rating = IntField()
	name = StringField()
	date = DateTimeField()

class Inventory(EmbeddedDocument):
	crop = StringField()
	qty = IntField()
	photo = ImageField(size=(100, 100, True))


class Farmer(Document):
	farmer_id = IntField(max_length = 20,unique = True)
	name = StringField(max_length = 30)
	email = EmailField(max_length=200,unique = True)
	password = StringField(max_length=1000)
	created_date=DateTimeField(default=None)
	stock = ListField(EmbeddedDocumentField(Inventory))
	reviews = ListField(EmbeddedDocumentField(Comment))
	#email_verified=BooleanField(default=False)
	#profile_created=BooleanField(default=False)
	#image = ImageField(size=(800, 600, True))
	#address = StringField(max_length=50)
	#phone_no = IntField(null=True)
	#lon = models.FloatField(null=True)
	#lat = models.FloatField(null=True)
	#description = models.CharField(max_length=300)


class Customer(Document):
	customer_id = IntField(max_length = 20,unique = True)
	name = StringField(max_length = 30)
	email = EmailField(max_length=200,unique = True)
	password = StringField(max_length=1000)
	created_date=DateTimeField()


class Inv(DynamicDocument):
	stock = ListField()


class Review(Document):
	farmer = ReferenceField(Farmer)
	customer = ReferenceField(Customer)
	content = StringField(max_length=1000)
	rating = IntField(null=True)
	date = DateTimeField(required=False)

	def json(self):
		dict={
			"farmer":farmer,
			"customer":customer,
			"content":content,
			"rating":rating,
			"date":date
		}
		return json.dumps(dict)
	

class History(Document):
	farmer = ReferenceField(Farmer)
	customer = ReferenceField(Customer)
	crop = StringField(max_length=20)
	qty = IntField()


# customer = Customer(customer_id = 100,name='many',email='many@gmail.com',password='harsha')
# customer.save()