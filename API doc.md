# Signup

## URL

**/signup**

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
## URL
**/login**
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
* **GET**
#### $~~~~~~~~~~$ URL $~~$ : **$~$ user/id**
### $~~~~~~~~~$ Responses<br>
 **$~~~~~~~~~~~~~~~$**   **Success Response**<br>
 **$~~~~~~~~~~~~~~~$**   **$~~~~~~~$**  `{"status" : "success",`<br>
 **$~~~~~~~~~~~~~~~$**   **$~~~~~~~$**  `"data" : []}`