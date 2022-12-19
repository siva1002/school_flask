## profile
* **/url**
profile/

**/methods:**
 "GET"
**/URL Params:**
**Requried:**
`id =id`
**/Success Response:**
* **code:** 200<br>
* **condent:** `{"id':user_id, firstname:profile.firstname,lastname:profile.lastname,fullname:profile.fullname,address:profile.address"}`<br>
* **Error Resopnse:** 400<br>
* **condent:** `{"error: profile Does't exits}`


## student-profile
* **/url**
student-profile
**/methods:**
"GET"
**URL Params:**
**Requried:**
 * firstname =[String]
 * lastname = [String]
 * fullname = [String]
 * address =  [String]

**/Success Response:**
* **code:** 200<br>
* **condent:** ``{"id':user_id, firstname:profile.firstname,lastname:profile.lastname,fullname:profile.fullname,address:profile.address"}`<br>
* **Error Response:** 400<br>
* **condent:** `{"error:studentprofile Does't exits}`

## student-profile
* **/url**
student-profile
**/methods:**
"PATCH"
**URL Params:**
**Requried:**
 * firstname =[String]
 * lastname = [String]
 * fullname = [String]
 * address =  [String]

**/Success Response:**
* **code:** 200<br>
* **condent:** ``{"id':user_id, firstname:profile.firstname,lastname:profile.lastname,fullname:profile.fullname,address:profile.address"}`<br>
* **Error Response:** 400<br>
* **condent:** `{"error:studentprofile Does't exits}`

## gread-get
* **/url**
grade
**/methods:**
"GET"
**Requried:**
 *grade =[Integer]
 *section =[List]
 **/Success Response:**
 * **code:** 200<br>
 * **condent:** `{id:user_id,grade:Grade.grade,section=Grade.section}`<br>
 * **Error Response:** 400<br>
 * **condent:**`{"error:grade Does't exits"}`
## gread-post
* **/url**
grade
**/methods:**
"GET"
**Requried:**
 *grade =[Integer]
 *section =[List]
 **/Success Response:**
 * **code:** 200<br>
 * **condent:** `{id:user_id,grade:Grade.grade,section=Grade.section}`<br>
 * **Error Response:** 400<br>
 * **condent:**`{"error:grade Does't exits"}`

 ## gread-patch
* **/url**
grade/<int:id>
**/methods:**
"PATCH"
**Requried:**
 *grade =[Integer]<br>
 *section =[List]<br>
 **/Success Response:**
 * **code:** 200<br>
 * **condent:** `{id:user_id,grade:Grade.grade,section=Grade.section}`<br>
 * **Error Response:** 400<br>
 * **condent:**`{"error:grade Does't exits"}`


## gread-delete
* **/url**
grade/<int:id>
**/methods:**
"DELETE"
**Requried:**
 *grade =[Integer]
 *section =[List]
 **/Success Response:**
 * **code:** 200<br>
 * **condent:** `{id:user_id,grade:Grade.grade,section=Grade.section}`<br>
 * **Error Response:** 400<br>
 * **condent:**`{"error:grade Does't exits"}`

 ## subject
 * **/url**
 **/methods:**
 "POST"
 **Requried:**
  *name =[String]
  *code = [Integer]
  *grade_id =[Integer]
  *created_at = [Datefield]
  **/Sucess Response:**
  * **code:** 200<br>
  * **condent:** `{name:Subject.name,code:Subject,grade_at:Subject.grade_id,created_at:Subject.created_at}`<br>
  * **Error Response:** 400<br>
  * **condent:**`{"error:subject Does't exits}`


## subject
 * **/url**
 **/methods:**
 "GET"
 **Requried:**
  *name =[String]
  *code = [Integer]
  *grade_id =[Integer]
  *created_at = [Datefield]
  **/Sucess Response:**
  * **code:** 200<br>
  * **condent:** `{name:Subject.name,code:Subject,grade_at:Subject.grade_id,created_at:Subject.created_at}`<br>
  * **Error Response:** 400<br>
  * **condent:**`{"error:subject Does't exits}`



  
 





