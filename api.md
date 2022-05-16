This is a human-readable summary of the api defined in mysite/address/urls.py
For example, the following would be appended to localhost:8000/address
 
#Navigable Pages

/  
The sign-in/sign-up page for users.

/home  
The default page for a user to view all contacts.
This also contains a search bar for filtering the contacts.

/add  
A page for the user to create a new contact.

/<contact_id>  
A page for a user to view the details of a particular contact.
Here they can also edit or delete the basic info.
They can also add and remove phone numbers for the contact from this page.



#API Endpoints
/do_add  
Adds a new contact to a user

/<contact_id>/do_edit  
Edits the details of a particular contact.

/<contact_id>/do_delete  
Deletes a particular contact.

/<contact_id>/phone/do_add  
Adds a new phone number to a particular contact.

/<contact_id>/phone/<phonenumber_id>/do_delete  
Deletes the specified phone number from a particular contact.

/sign_out  
Signs out the currently signed-in user. Returns them to sign-in/sign-up page.
