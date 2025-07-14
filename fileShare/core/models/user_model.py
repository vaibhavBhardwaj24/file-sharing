import mongoengine as me
import uuid
class User(me.Document):
    uuid=me.UUIDField(default=uuid.uuid4,binary=False,unique=True)
    username = me.StringField(unique=True,required=True,max_length=50)
    password_hashed = me.StringField(required=True,max_length=100)
    is_admin = me.BooleanField(default=False)
    created_at = me.DateTimeField(auto_now_add=True)
    email=me.EmailField(required=True,max_length=50,unique=True)
    is_active=me.BooleanField(default=False,required=True)