# Securing Passwords
Method of securing user passwords using Static and Dynamic Salts

A proposed method of securing user passwords using hashing, static and dynamic salts. When an user account is created, the password is ususally stored in a Database, we have a number of options on how to store the password

Plain Text : Password is stored as plain text in a DB column. This is the worst way of storing a password as accounts can be hijacked merely by getting access to the DB 

Hashed Password : Password is hashed using a hashing function, like bcrypt and stored in the DB column. This is secure to an extent but still at risk as the only layer of security is the hashing function.

Static Salted Password : A Static string, called Salt, is added to the password and then hashed. This is more secure than plain Hashing as the Static Salt is necessary to crack the password, but is still as risk as all the passwords are hashed the same way. So, if one password is cracked, the same method can be used to crack all the passwords.

Dynamic Salted Password : This extends the Static Salted Password method, but instead of a Static Salt, a Dynamic Salt is added to each password. This increases the security as each password will be hashed with a different salt and even if one password is cracked, the same method cannot be used to crack all the passwords. 


In this example, we use a combination of Static + Dynamic Salt and Hashing to secure the password. 

Flow : 

1) Code contains a Static Salt 
2) User creates an account 
3) A timestamp is generated to be used as a Dynamic Salt 
4) Password String is created by adding the Static Salt + User Password + Dynamic Salt
5) Password String is Hashed
6) Hashed Password is stored in the DB 

When generating the timestamp in pt3, the logic can be done as per your lking. You can generate a complex timestamp with microseconds, AM/PM, Dates etc
When creating the Password String in pt4, the logic can be done as per your liking. You could go with any combination you want. 

# Implementation : 
This is a Python Flask based App, the main code is in main.py, HTML templates are in templates and a DB, SQLite, is in the DB Folder. 

To test the logic : 

1) Edit all the paths to the DB in the main.py to reference your system's path
2) Run the App in PyCharm and open the webpage
3) Create 2 users with the same password
4) Login to the DB, via the Shell, and notice that the password hashes for both the users are different
5) Change the password for one user and use the same password
6) Login to the DB, via the Shell, and notice that the password hash for the changed used is different now, even though we resued the same passwor
7) DB, Table, Row Names are all available in the main.py file inside the code
