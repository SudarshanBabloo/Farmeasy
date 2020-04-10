# from mongoengine import *
# connect('Farmers')

# class Comment(EmbeddedDocument):
# 	content = StringField()
# 	rating = IntField()
# 	name = StringField()

# class Inventory(EmbeddedDocument):
# 	crop = StringField()
# 	qty = IntField()


# class Farmer(Document):
# 	farmer_id = IntField(max_length = 20,unique = True)
# 	name = StringField(max_length = 30)
# 	email = EmailField(max_length=200,unique = True)
# 	password = StringField(max_length=1000)
# 	created_date=DateTimeField(default=None)
# 	stock = ListField(EmbeddedDocumentField(Inventory))
# 	reviews = ListField(EmbeddedDocumentField(Comment))


# farmer = Farmer.objects(farmer_id=100).get()
# crop = 'tomato'
# qty = 30

# for i in farmer.stock:
#     if i.crop == 'tomato':
#         i.qty = qty + i.qty
#         farmer.save()
    
    

# a = (farmer.stock[0])
# print(a.qty) 





