from dataclasses import field
from statistics import mode
from rest_framework import serializers

from users.models import Doc,UserDetail,Dep


class DocSerializer(serializers.ModelSerializer):
    branchname = serializers.SerializerMethodField(read_only=True)
    department = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doc
        fields = ('id','name',"users","department","coming","descr","created_by","branchname","date","sec_id","approved","op1","op2")
    def get_branchname(self,doc):
        return doc.branch.name
    def get_department(self,doc):
        return doc.dep.name
    

class CreateDocSerializer(serializers.ModelSerializer):
    branchname = serializers.SerializerMethodField(read_only=True)
    department = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doc
        fields  = ("name","descr",'users',"branch","coming","created_by","date","branchname","doc","op1","op2","department","dep","id","pdf")
        read_only_fields = ['users',"branch","coming","created_by","branchname","pdf"]
    def get_branchname(self,doc):
        return doc.branch.name
    def get_department(self,doc):
        return doc.dep.name

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

class DepsSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Dep 
        fields= "__all__"