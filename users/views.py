from pyexpat import model
from re import U
from unicodedata import name
from urllib import request
from django import views
from rest_framework import viewsets
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
from django.contrib.auth.models import User
from PyPDF2 import PdfFileMerger, PdfFileReader,PdfFileWriter
from datetime import datetime
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.db.models import Q
from .permissions import UpdatePermission, ModeerPermission
from rest_framework import status
from django.views.generic import DetailView
from django.http import FileResponse
from reportlab.pdfgen import canvas
import os
from django.core.files import File
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from docx2pdf import convert

import docx
from docx.shared import Cm
import subprocess

#libreoffice

def sign(fname, img,user,docu):
    doc = docx.Document(fname)
    

    doc.add_picture(img,width= Cm(5), height = Cm(2))
    
    doc.save(fname)
    docu.save()

    
    

    convert("files\"+fname)
    pdfname = fname.replace("docx", "pdf")
    #pdfname = pdfname.replace("files/", "")
    docu.pdf = pdfname
    arch = UserDetail.objects.filter(branch = Branches.objects.filter(name= "archive")[0])[0]
    docu.users = arch
    docu.approved = True
    docu.save()
    






"""
def sign(f1,u,d,nm,madany):
        c = canvas.Canvas("ww")
    c.drawImage(f2, 450, 1, width=100,height=30)
    c.save()

    file1 = PdfFileReader(open(f1, "rb"))
    file2 = PdfFileReader(open("ww", "rb"))

    output = PdfFileWriter()

    page = file1.getPage(-1)
    page.mergePage(file2.getPage(0))

    output.addPage(page)

    outputStream = open(f"document{num}.pdf", "wb")
    output.write(outputStream)

    outputStream.close()
    

    c = canvas.Canvas('watermark.pdf')
    im = UserDetail.objects.get(id = u)
    # Draw the image at x, y. I positioned the x,y to be where i like here
    if madany:
        c.drawImage(im.imgmadany.path, 30, 1, width=150,height=80)
    else:
        c.drawImage(im.img.path, 30, 1, width=150,height=80)

    c.save()
    #print(c)




    file1 = PdfFileReader(open(f1, "rb"))
    file2 = PdfFileReader(open("watermark.pdf", "rb"))

    output = PdfFileWriter()
    for i in range(file1.getNumPages()):
        if i == file1.getNumPages() -1:
            page = file1.getPage(i)
            page.mergePage(file2.getPage(0))
            output.addPage(page)
        else:
            page = file1.getPage(i)
            output.addPage(page)

    arch = UserDetail.objects.filter(branch = Branches.objects.filter(name= "archive")[0])[0]
    outputStream = open(nm, "wb")
    output.write(outputStream)
    outputStream.close()
    dd = Doc.objects.get(id = d)
    l = open(nm,"rb")
    ll = File(l)
    dd.doc = ll
    dd.approved = True
    dd.users = arch
    dd.save()
    l.close()
    os.remove(f1)
    os.remove("watermark.pdf")

"""

class DocsView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
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
        serializer.save(users = UserDetail.objects.get(id =self.request.data["user"]), branch = self.request.user.info.branch,coming = self.request.user.info,
        created_by = self.request.user.info)
        output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,str(serializer.instance.doc.path)])
        fname = str(serializer.instance.doc.path).replace("docx", "pdf")
        fname = fname.replace("files/", "")

        serializer.save(pdf = fname)


"""class DocDetail(generics.RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #queryset = Doc.objects.all()
    #serializer_class = DocSerializer
    
    def put(self, request, format=None):
    
        
        d =request.data['id']
        obj = Doc.objects.get(id = d)
        #obj  = self.get_object()
        fil = open(obj.doc.path, 'rb')
        response = HttpResponse(FileWrapper(fil), content_type='application/pdf')
        return response"""

class PermList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = UserDetail.objects.get(user= request.user)
        if user.rank == "saf":
            susers = UserDetail.objects.filter(Q(rank = "zabet") | Q(rank = "superzabet"),branch = user.branch)
        elif user.rank == "zabet":
            susers = UserDetail.objects.filter(Q(rank = "superzabet")|Q(rank='zabet'),~Q(user = request.user),branch = user.branch)
        elif user.rank == "superzabet":
            susers = UserDetail.objects.filter(Q(rank = "raeesarkan")|Q(rank="modeer")|Q(rank= "superzabet", branch = user.branch), ~Q(user = request.user))
        elif user.rank == "modeer":
            susers = UserDetail.objects.filter(rank = "raeesarkan")

        elif user.rank == "raeesarkan":
            susers = UserDetail.objects.filter(rank = "modeer")
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

        if user.rank == "zabet":
            susers = UserDetail.objects.filter(rank = "saf",branch = user.branch)
        elif user.rank == "superzabet":
            susers = UserDetail.objects.filter(Q(rank = "zabet")|Q(rank="saf"),branch = user.branch)
        #elif user.rank == "modeer":
            #susers = UserDetail.objects.filter(rank = "raeesarkan")

        #elif user.rank == "raeesarkan":
            #susers = UserDetail.objects.filter(Q(rank = "zabet") |Q(rank="superzabet"),branch = Branches.objects.get(name=branchh))
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
        #a =  request.data.get("",request.user.info.id)
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def perform_update(self, serializer):
        if self.request.data.get("users",-1) != -1:
            serializer.save(coming = self.request.user.info)

class Showpdf(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        return FileResponse(open(dcc.pdf.path, 'rb'), as_attachment=True, content_type='application/pdf')
class Shop1(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        return FileResponse(open(dcc.op1.path, 'rb'), as_attachment=True, content_type='application/pdf')
class Showop1(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
      # Create a file-like buffer to receive PDF data.
    def get(self, request,id, format=None):
        dcc = Doc.objects.get(id = id)
        return FileResponse(open(dcc.op2.path, 'rb'), as_attachment=True, content_type='application/pdf')

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
        if "docid" in request.data and request.user.info.img != None and  request.user.info.imgmadany != None and "madany" in request.data:
            d = request.data["docid"]
            dc = Doc.objects.get(id = d)
            fname = dc.doc.path
            u = request.user.info
            if request.data["madany"]:
                sign(fname,u.imgmadany.path,u,dc)
            else:
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
        if self.request.user.info.branch.name == "archive" or self.request.user.info.rank  == "modeer" or self.request.user.info.rank == "raeesarkan":
            return Doc.objects.filter(approved = True).order_by("-date")
        else:
            return Doc.objects.filter(approved = True, branch = self.request.user.info.branch).order_by("-date")
