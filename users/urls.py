from venv import create
from django.urls import path
from .views import  Allusers, Approve, CustomAuthToken, DeleteDoc,DocsView,DocCreate,PermList, Search, Shop1, Showop1, UpdateDoc,LowerPermList,Showpdf,Deps

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('docslist/',DocsView.as_view()),
    path('docscreate/',DocCreate.as_view()),
    path("permlist/",PermList.as_view()),
    path("updatedoc/<pk>",UpdateDoc.as_view()),
    path("lowerpermlist/",LowerPermList.as_view()),
    path("pdf/<id>",Showpdf.as_view()),
    path("allusers/",Allusers.as_view()),
    path("op1/<id>",Shop1.as_view()),
    path("op2/<id>",Showop1.as_view()),
    path("dep/",Deps.as_view()),
    path("approve/",Approve.as_view()),
    path("search", Search.as_view()),
    path("delete/<pk>", DeleteDoc.as_view()),
    
    #path("search/<str:date>", Search.as_view()),
    #path("search/<str:name>", Search.as_view()),





    

    
]