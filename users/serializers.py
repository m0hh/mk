from dataclasses import field
from statistics import mode
from rest_framework import serializers

from users.models import Doc,UserDetail


class DocSerializer(serializers.ModelSerializer):
    #def __init__(self, *args, **kwargs):
    #    many = kwargs.pop('many',True)
    #    super(DocSerializer,self).__init__(many=many,*args, **kwargs)
    branchname = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Doc
        fields = ('id','name',"users","branch","coming","descr","created_by","branchname")
    def get_branchname(self,doc):
        return doc.branch.name
    

class CreateDocSerializer(serializers.ModelSerializer):
    branchname = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Doc
        fields  = ("name","descr",'users',"branch","coming","created_by","date","branchname" )
        read_only_fields = ['users',"branch","coming","created_by","branchname"]
    def get_branchname(self,doc):
        return doc.branch.name

class UpdateDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        fields  = "__all__"
        read_only_fields = ("coming","created_by")
class PermListSerializer(serializers.ModelSerializer):
    uname = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserDetail
        fields = ("id","uname","rank","branch") 
    def get_uname(self,userdetail):
        return userdetail.user.username


class AllusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = "__all__"