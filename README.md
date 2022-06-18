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

### View documents in the Inbox
Now that we've created a document and sent it to a superior we can see documents in our inbox by going to this url docslist/

you will send a GET request with the Token in headers

you will recive a list of all documents in this user inbox like this

```
[
    {
        "id": 52,
        "name": "doc1",
        "users": 14,
        "department": "Accounting",
        "coming": 12,
        "descr": "aucsc",
        "created_by": 12,
        "branchname": "Haram",
        "date": "2022-06-17",
        "sec_id": null,
        "approved": false,
        "op1": null,
        "op2": null
    },
    {
        "id": 53,
        "name": "doc1",
        "users": 14,
        "department": "Accounting",
        "coming": 12,
        "descr": "aucsc",
        "created_by": 12,
        "branchname": "Haram",
        "date": "2022-06-17",
        "sec_id": null,
        "approved": false,
        "op1": null,
        "op2": null
    }
]
```

 the new elements here are sec_id which we added to allow the archive manager to add a second ID to manage the documents
 and approved which is to determine if the document is approved and has been automatically signed
 
 ### Send a document to another user or any kind of update document
 to update document you send a PATCH request to updatedoc/<PK of document>
 with request like this
 
```
 {
    "users" :15
 }
```
 Here we specified the user to send this document to 
 the response will come like this
 ```
 {
    "id": 52,
    "name": "doc1",
    "doc": "http://127.0.0.1:8000/files/Untitled_1_L0tOT1u.docx",
    "pdf": "http://127.0.0.1:8000/home/mohamed/Documents/mk/Untitled_1.pdf",
    "op1": null,
    "op2": null,
    "approved": false,
    "descr": "aucsc",
    "date": "2022-06-17",
    "sec_id": null,
    "coming": 14,
    "users": 15,
    "branch": 6,
    "created_by": 12,
    "dep": 3
}
```
 we see that users changed from 14 to 15 indicating that we sent the document to user 15
 
 ### Get list of superior users to send documents to
 If you want to create document or send a document(update) you will need a list of all superior users in the same branch
 to do that send a GET request to permlist/
 you will recive a response like this
 ```
 [
    {
        "id": 15,
        "uname": "mahmoudManager",
        "rank": "Manager",
        "branch": 6
    }
]
```
 Note that the list will contain all users directly above the request sender who are in the same branch as he is
 
 ### Get list of all subordinates
 
 to get a list of users directly below the request sender you will send a GET request to this url lowerpermlist/
 
 you will recive a response like this
 ```
 [
    {
        "id": 12,
        "uname": "AhmedEmployee",
        "rank": "Employee",
        "branch": 6
    },
    {
        "id": 13,
        "uname": "Ahmed2Empolyee",
        "rank": "Employee",
        "branch": 6
    }
]
```
 ### preview a pdf
 to preview a pdf send a a GET request to this url pdf/<id of the document>
 you will recive the pdf file as response
 
 ### preview optional
 to preview optional document 1 send GET request to op1/<id> for optional document 1 and op2/<id> for optional document 2
 you will recive the optional document file as a response
 
 ### List of users
 to get a list of all users send a GET request to this allusers/
 you will recive a Document like this
 ```
 [
    {
        "id": 12,
        "rank": "Employee",
        "branch": 6,
        "uname": "AhmedEmployee"
    },
    {
        "id": 13,
        "rank": "Employee",
        "branch": 6,
        "uname": "Ahmed2Empolyee"
    },
    {
        "id": 14,
        "rank": "Supervisor",
        "branch": 6,
        "uname": "AymanSupervisor"
    },
    {
        "id": 15,
        "rank": "Manager",
        "branch": 6,
        "uname": "mahmoudManager"
    },
    {
        "id": 16,
        "rank": "CTO",
        "branch": 7,
        "uname": "EzzCTO"
    },
    {
        "id": 17,
        "rank": "CEO",
        "branch": 7,
        "uname": "YaraCEO"
    },
    {
        "id": 18,
        "rank": "archive",
        "branch": 8,
        "uname": "Anasarchive"
    }
]
```
 ### List all Departments
 To list all departments send a GET request to this dep/
 
 you will recive a response like this
 ```
 [
    {
        "id": 3,
        "name": "Accounting"
    },
    {
        "id": 4,
        "name": "Sales"
    },
    {
        "id": 5,
        "name": "IT"
    }
]
```
 Note that you Can do all CRUD operations on Department via the admin panel
 
 ### Approve the document
 First you ned to add a signature a a picture to the UserDetail table via the admin panel to the CEO and CTO
 I also added a permission that allows only the CEO and CTO of approving Documents
 to approve a Document send POST request to this url approve/
 like this
```
{
    "docid": 52
}
 ```
 you will recive a response like this
 ```
{"approved":"True"}
 
 ### Search
 to search for a document you can send a GET request to search?name=actual name that will search by name
 or search?date=date that will filter by date
 or search?id= id  that will filter by ID
 or search?sec_id= Secondary Id that will filter by secondary ID
 
 and you will recive a response like this
 ```
 [
    {
        "id": 52,
        "name": "doc1",
        "users": 18,
        "department": "Accounting",
        "coming": 15,
        "descr": "aucsc",
        "created_by": 12,
        "branchname": "Haram",
        "date": "2022-06-17",
        "sec_id": null,
        "approved": true,
        "op1": null,
        "op2": null
    }
]
 ```
 ### Delete a document
 To delete a document send a DELETE request to this url delete/<pk>
 but you have to be the document owner as in {users: ID of the request sender
 
