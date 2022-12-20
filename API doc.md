

# Signup
#### $~~~~~~~~~~$ URL $~~$ : **$~$ /signup**

* **Method:**
  `POST`
### Data Params
       {
         {"user":
            {
            "email":"user735@gmail.com",
            "phone":"9248786695",
            "usertype":"is-admin",
            "registernumber":"user7529"
            },
        "profile":{
                    "firstname":"user73",
                    "lastname":"new",
                    "fullname":"harry",
                    "address":"new",
                    "standard":["1-A"]}
                    }
        }
 ## Responses
** **
### Success Response

`User created successfully`
### Failure Response
` returns the Exception while the process `
<br><br> 

# Login 
#### $~~~~~~~~~~$ URL $~~$ : **$~$ /login**
### Data Params
        {
        "email:<email>
        "phone":<phone>
        }
## Responses
** **
### Success Response

`{status : "successfully logged in"`<br>
`data   : <logged in users data>`<br>
`token  : <token>}`
### Failure Response
` User Does Not Exist`
<br><br> 

# User Details
## **$~~~$** Methods<br>
**$~~~~~$** `GET,PATCH,DELETE`
#### $~~~~~$ URL $~~$ : **$~$ user/id**
* **GET**
### $~~~~~~~~~$ Responses<br>
 **$~~~~~~~~~~~~~~~$**   **Success Response**<br>
 **$~~~~~~~~~~~~~~~$**   **$~~~~~~~$**  `{"status" : "success",`<br>
 **$~~~~~~~~~~~~~~~$**   **$~~~~~~~$**  `"data" : <data(Array)>}`<br>
 **$~~~~~~~~~~~~~~~$**  **Failure Response**<br>
 **$~~~~~~~~~~~~~~~~~~~~~~$**  ` User Does Not Exist`
<br><br> 

* **DELETE**

### $~~~~~~~~~$    Responses<br>
 $~~~~~~~~~~~$     **Success Response**<br>
  $~~~~~~~~~~~$  `{"status" : "User Deleted Successfully",`<br>

$~~~~~~~~~~~$    **Failure Response**<br>
  $~~~~~~~~~~~$  `User Dosen't exist`
<br><br> 

* **PATCH**
### Data Params
      {
         {"user":
            {
            "email":"user735@gmail.com",
            "phone":"9248786695",
            "usertype":"is-admin",
            "registernumber":"user7529"
            },
        "profile":{
                    "firstname":"user73",
                    "lastname":"new",
                    "fullname":"harry",
                    "address":"new",
                    "standard":["1-A"]}
                    }
        }
###  Responses<br>
 *   **Success Response**<br>
  `{"status" : "Updated Successfully",`<br>

 * **Failure Response**<br>
  ` Exception while updating`
<br><br> 

# Profile
#### $~~~~~~~~~~$ URL $~~$ : **$~$ /profile**
###  Responses<br>
 *   **Success Response $~$ (if user logged in)**<br>
 $~~$  `{"status" : "success" , "data":<[logged in user data]>}`
 * **Failure Response**<br>
 $~~$ ` User Does not logged in `
# Grade
  #### URL $~~$ : **$~$ /grade**
   ##  Methods<br>
  **$~~~~~$** `GET,'POST',PATCH,DELETE`
  * **POST**
      ### Data Params
          {
              "grade":<int>,"section":<array of sections>
          }
    ### Responses<br>
    *   **Success Response $~$ (if user logged in)**<br>
    `{"status" : "success" , "message":"Grade Created"}`
    * **Failure Response**<br>
  ` Grade already exists `
  * **GET**
    ### Responses<br>
  *   **Success Response**<br>
      * ### if student user logged in
        `{"status" : "success" , "data:[grade of student]"}`
      * ### if staff user logged in
        `{"status" : "success" , "data:[<grades which allocated to the logged in staff>]"}`

      * ### if admin user logged in
          `{"status" : "success" , "data:[<all grades>]"}`
  * **Failure Response**<br>
  $~~~$`{"status": "failure", 'data': 'Your not have access to view this page'}`
  ** **
   * **PATCH**
     #### URL $~~$ : **$~$ /grade/id**
     ### Data Params
          {
              "grade":<int>,"section":<array of sections>
          }
      ### Responses<br>
      *   **Success Response**<br>
     ` {"message": "Grade  Updated "}`
     * **Failure Response**<br>
     ** **
  `{"status": "failure", 'data': '<Exception error while updating>'}`
  * **DELETE**
     #### URL $~~$ : **$~$ /grade/id**
      ### Responses<br>
      *   **Success Response**<br>
     ` {"message": "Grade  Deleted "}`
     * **Failure Response**<br>
  `{"status": "failure", 'data': '<Exception error while updating>'}`
  ** ** 
  ** **