from re import U
from django_filters import rest_framework as filters
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser

from users.serializers import AllusersSerializer, DepsSeralizer, DocSerializer, CreateDocSerializer,PermListSerializer, UpdateDocSerializer
from .models import Dep, UserDetail, Doc,Branches
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import authentication, permissions

from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.db.models import Q
from .permissions import UpdatePermission, ModeerPermission
from rest_framework import status

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from docx2pdf import convert

import docx
from docx.shared import Cm
import subprocess

def sign(fname, img,user,docu):
    doc = docx.Document(fname)
    

    doc.add_picture(img,width= Cm(5), height = Cm(2))
    
    doc.save(fname)
    docu.save()

    output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,fname])
    pdfname = fname.replace("docx", "pdf")
    pdfname = pdfname.replace("files/", "")
    docu.pdf = pdfname
    arch = UserDetail.objects.filter(branch = Branches.objects.filter(name= "archive")[0])[0]
    docu.users = arch
    docu.approved = True
    docu.save()
    







class DocsView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        queryset = request.user.info.docs.all()
        serializer = DocSerializer(queryset,many=True)
        return Response(serializer.data)



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            info = UserDetail.objects.get(user = user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.username,
                "rank" : info.rank,
                "branch": info.branch.name
            })
        else:
            return Response({
                "8alat pass" : "pass 8alat"
            },status=status.HTTP_400_BAD_REQUEST)



class DocCreate(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Doc.objects.all()
    serializer_class  = CreateDocSerializer
    parser_classes = (MultiPartParser, FormParser,)
    def perform_create(self, serializer):
        try:
            serializer.save(users = UserDetail.objects.get(id =self.request.data["user"]), branch = self.request.user.info.branch,coming = self.request.user.info,
            created_by = self.request.user.info)
            output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,serializer.instance.doc.path])
            fname = str(serializer.instance.doc.path).replace("docx", "pdf")
            fname = fname.replace("files/", "")

            serializer.save(pdf = fname)
        except:
            serializer.instance.delete()
            raise ValueError



class PermList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = UserDetail.objects.get(user= request.user)
        if user.rank == "Employee":
            susers = UserDetail.objects.filter(Q(rank = "Supervisor") | Q(rank = "Manager"),branch = user.branch)
        elif user.rank == "Supervisor":
            susers = UserDetail.objects.filter(Q(rank = "Manager")|Q(rank='Supervisor'),~Q(user = request.user),branch = user.branch)
        elif user.rank == "Manager":
            susers = UserDetail.objects.filter(Q(rank = "CEO")|Q(rank="CTO")|Q(rank= "Manager", branch = user.branch), ~Q(user = request.user))
        elif user.rank == "CEO":
            susers = UserDetail.objects.filter(rank = "CTO")

        elif user.rank == "CTO":
            susers = UserDetail.objects.filter(rank = "CEO")
        else:
            return Response({"No objects With that ID": "Try a dffrent ID"})

        serializer = PermListSerializer(susers,many = True)
        return Response(serializer.data)
        
class LowerPermList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = UserDetail.objects.get(user= request.user)

        if user.rank == "Supervisor":
            susers = UserDetail.objects.filter(rank = "Emplyee",branch = user.branch)
        elif user.rank == "Manager":
            susers = UserDetail.objects.filter(Q(rank = "Supervisor")|Q(rank="Employee"),branch = user.branch)
        else:
            return Response({"No objects With that ID": "Try a dffrent ID"})

        serializer = PermListSerializer(susers,many = True)
        return Response(serializer.data)
        


        
        
class UpdateDoc(generics.UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [UpdatePermission]
    queryset = Doc.objects.all()
    serializer_class  = UpdateDocSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def perform_update(self, serializer):
        if self.request.data.get("users",-1) != -1:
            serializer.save(coming = self.request.user.info)

class Showpdf(APIView):

      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        fil = open(dcc.pdf.path, 'rb')
        response = HttpResponse(FileWrapper(fil), content_type='application/pdf')
        return response
class Shop1(APIView):

      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        fil = open(dcc.op1.path, 'rb')
        response = HttpResponse(FileWrapper(fil), content_type='application/pdf')
        return response
class Showop1(APIView):

      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        fil = open(dcc.op2.path, 'rb')
        response = HttpResponse(FileWrapper(fil), content_type='application/pdf')
        return response

class Allusers(generics.ListAPIView):
    queryset = UserDetail.objects.all()
    serializer_class  = AllusersSerializer


class Deps(generics.ListAPIView):
    queryset = Dep.objects.all()
    serializer_class = DepsSeralizer

class Approve(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [ModeerPermission]
    def post(self, request, format=None):
        if "docid" in request.data and request.user.info.img != None and  request.user.info.imgmadany != None :
            d = request.data["docid"]
            dc = Doc.objects.get(id = d)
            fname = dc.doc.path
            u = request.user.info
            sign(fname,u.img.path,u,dc)
            return Response({"cool":"all right"})
        else:
            return Response({"Forbidden": "you need to add pic or send docid in body"}, status= status.HTTP_400_BAD_REQUEST)


class Search(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocSerializer
    model = Doc
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ["date","id","sec_id"]

    def get_queryset(self):
        if self.request.user.info.branch.name == "archive" or self.request.user.info.rank  == "CEO" or self.request.user.info.rank == "CTO":
            return Doc.objects.filter(approved = True).order_by("-date")
        else:
            return Doc.objects.filter(approved = True, branch = self.request.user.info.branch).order_by("-date")

class DeleteDoc(generics.DestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [UpdatePermission]
    serializer_class = DocSerializer
    queryset = Doc.objects.all()