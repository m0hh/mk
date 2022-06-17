# Heirarchial Correspendece and signature stystem
 This a system where employees can send correspendeces to emplyee directly above them and can return the correspence to employees directly beneath them. The correspendence stays in the system until it finally reaches the CEO or CTO who can approve it and it will automatically add their signature to the document and be sent to the archive
 
 Here is a breakdown of the ranks in the system
 
![Pyramid Heriarchy](files/1.jpg)

## Authentication
I used Token authentication to Verify users and pull up their rank

## Database
Here is an ERD of the data base

![ERD](files/2.jpg)

## Project setup

Install required packages:

    pip3 install -r requirements.txt

Initialize database:

    python3 manage.py makemigrations
    python3 manage.py migrate
  
  ## Documentation
  
  ### Authentication
  To get Token to use for authentication send a POST request to this url api-token-auth/
  with this request 

    {
      "username" : "AhmedEmployee",
      "password" : "test4321"
     }
     
 You will get a response like this
 ```
     {
       "token": "ccc22e350d09de6453d349db4be202a148314bc3",
       "user_id": 13,
       "email": "AhmedEmployee",
       "rank": "Employee",
       "branch": "Haram"
     }
 ```
 
 You will use this token every time you send a request 
 
 ### Create a Doc
 
 Send a POST request to this url docscreate/
 
 with this request as form data
 
 ```
 name : name of the document
 doc : document file
 descr: doc description
 user: ID of the user to send this to
 dep : ID of the department of the document
 op1: optional file
 op2: optional file
```

you will recive response like this

```
{
    "name": "doc1",
    "descr": "aucsc",
    "users": 14,
    "branch": 6,
    "coming": 12,
    "created_by": 12,
    "date": "2022-06-17",
    "branchname": "Haram",
    "doc": "http://127.0.0.1:8000/files/Untitled_1_L0tOT1u.docx",
    "op1": null,
    "op2": null,
    "department": "Accounting",
    "dep": 3,
    "id": 52,
    "pdf": "http://127.0.0.1:8000/home/mohamed/Documents/mk/Untitled_1.pdf"
}
```
users is the id of the user that the document was sent to
branch is the id of the branch of the user
coming is the id of user that the document came from
created_by is the id of the user who created the document
pdf is the document after it was converted to pdf
 
