from venv import create
from django.urls import path
from .views import  Allusers, CustomAuthToken,DocsView,DocCreate,DocDetail,PermList, UpdateDoc,LowerPermList,Showpdf

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('docslist/',DocsView.as_view()),
    path('docscreate/',DocCreate.as_view()),
    path("docsdetail/",DocDetail.as_view()),
    path("permlist/",PermList.as_view()),
    path("updatedoc/<pk>",UpdateDoc.as_view()),
    path("lowerpermlist/<str:branchh>",LowerPermList.as_view()),
    path("pdf/<id>",Showpdf.as_view()),
    path("allusers/",Allusers.as_view()),

    

    
]