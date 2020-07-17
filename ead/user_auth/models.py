from mongoengine import *
import datetime

connect('Farmers')


class consumer(Document):

    email = StringField(max_length=100, unique=True)
    password = StringField(max_length=100)
    f_name = StringField(max_length=50)
    l_name = StringField(max_length=50)
    gender = StringField(max_length=10, default='M')
    address = StringField(max_length=200)
    created_date = DateTimeField()
    email_verified = BooleanField(default=False)
    phone_no = StringField(max_length=10)
    location = PointField(auto_index=True)

class Comment(EmbeddedDocument):
    title = StringField()
    content = StringField()
    rating = IntField()
    name = StringField()
    date = DateTimeField()



class Product(EmbeddedDocument):
    product_id = IntField(max_length=20, unique=True)
    cat_id = IntField()
    name = StringField()
    photo = ImageField(size=(100,100,True))
    description = StringField()
    stock = IntField(max = 99999)
    cost = IntField()
    reviews = ListField(EmbeddedDocumentField(Comment))
    rating = IntField(default=0)


class retailer(Document):

    email = StringField(max_length=100, unique=True)
    password = StringField(max_length=100)
    f_name = StringField(max_length=50)
    l_name = StringField(max_length=50)
    gender = StringField(max_length=10, default='M')
    address = StringField(max_length=200)
    created_date = DateTimeField()
    email_verified = BooleanField(default=False)
    phone_no = StringField(max_length=10)
    products = ListField(EmbeddedDocumentField(Product))
    location = PointField(auto_index=True)


class Message(Document):
    author = ReferenceField(consumer)
    content = StringField(max_length=200)
    timestamp = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.author.f_name

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]



class Inventory(EmbeddedDocument):
	crop = StringField()
	qty = IntField()
	photo = ImageField()



class farmer(Document):
    email = StringField(max_length=100,unique = True)
    password = StringField(max_length=100)
    f_name = StringField(max_length=50)
    l_name = StringField(max_length=50)
    gender= StringField(max_length=10,default='M')
    address=StringField(max_length=200)
    created_date=DateTimeField()
    email_verified=BooleanField(default=False)
    phone_no=StringField(max_length=10)
    stock = ListField(EmbeddedDocumentField(Inventory))
    reviews = ListField(EmbeddedDocumentField(Comment))
    location = PointField(auto_index=True)
    
    
    # items=EmbeddedDocumentListField('crops')
# class crops(Document):
#     vegetable=StringField(max_length=20)
#     quantity=IntField()    





# class Product_post(Document):
#     p_id=IntField(unique=True)
#     Retailer_id=IntField()
#     price=FloatField()
#     description=StringField(max_length=200)
#     name=StringField(max_length=30)
#     review_id=IntField()
#     image=ImageField()
# class vegetable_posts(Document):
#     p_id=IntField(unique=True)
#     consumer=ReferenceField(consumer)
#     address=StringField(max_length=200)
#     vegetable=StringField(max_length=20)
#     quantity=IntField()
#     price=FloatField()
#     text=StringField(max_length=200)
#     status=IntField()

# class collaborative_deal(Document):
#     farmer_id_1=ReferenceField(Farmer)
#     farmer_id_2=ReferenceField(Farmer)
#     text=StringField(max_length=200)
#     image=ImageField()
# class transactions(Document):
#     consumer_id=ReferenceField(consumer)
#     farmer_id=ReferenceField(Farmer)
#     consumer_price=FloatField()
#     farmer_price=FloatField()
#     deal_status=IntField()
            









    
