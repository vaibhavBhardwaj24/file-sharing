import mongoengine as me
import uuid
class File(me.Document):
    uuid=me.UUIDField(default=uuid.uuid4,binary=False,unique=True)
    uploadedBy=me.ReferenceField('User',required=True)
    fileName=me.StringField(required=True)
    filePath=me.StringField(required=True)
    fileType=me.StringField(Choices=['.pptx','.docs','.xlsx'],required=True)
    uploaded_at=me.DateField(required=True,auto_now_add=True)
