from pyexpat import model
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser

from users.serializers import AllusersSerializer, DocSerializer, CreateDocSerializer,PermListSerializer, UpdateDocSerializer
from .models import UserDetail, Doc,Branches
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from PyPDF2 import PdfFileMerger, PdfFileReader,PdfFileWriter
from datetime import datetime
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.db.models import Q
from .permissions import UpdatePermission
from rest_framework import status
from django.views.generic import DetailView
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas




def sign(f1,f2,num):
    file1 = PdfFileReader(open(f1, "rb"))
    file2 = PdfFileReader(open(f2, "rb"))

    output = PdfFileWriter()

    page = file1.getPage(0)
    page.mergePage(file2.getPage(0))

    output.addPage(page)

    outputStream = open(f"document{num}.pdf", "wb")
    output.write(outputStream)

    outputStream.close()


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

class DocDetail(generics.RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #queryset = Doc.objects.all()
    #serializer_class = DocSerializer
    
    def put(self, request, format=None):
        """
        Return a list of all users.
        """
        d =request.data['id']
        obj = Doc.objects.get(id = d)
        #obj  = self.get_object()
        fil = open(obj.doc.path, 'rb')
        response = HttpResponse(FileWrapper(fil), content_type='application/pdf')
        return response

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

    def get(self, request,branchh, format=None):
        """
        Return a list of all users.
        """
        user = UserDetail.objects.get(user= request.user)

        if user.rank == "zabet":
            susers = UserDetail.objects.filter(rank = "saf",branch = user.branch)
        elif user.rank == "superzabet":
            susers = UserDetail.objects.filter(Q(rank = "zabet")|Q(rank="saf"),branch = user.branch)
        elif user.rank == "modeer":
            susers = UserDetail.objects.filter(rank = "raeesarkan")

        elif user.rank == "raeesarkan":
            susers = UserDetail.objects.filter(Q(rank = "zabet") |Q(rank="superzabet"),branch = Branches.objects.get(name=branchh))
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
        return FileResponse(open(dcc.doc.path, 'rb'), as_attachment=True, content_type='application/pdf')
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


    

    