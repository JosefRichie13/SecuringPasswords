from flask import Flask, render_template, request
import sqlite3
import hashlib
import datetime


# Function to hash the password
def saltpass(upass):
    salt = "$3*&4&12KL"

    currentdatetime = datetime.datetime.now()
    modifieddatetime = str(currentdatetime) + currentdatetime.strftime("%p") + currentdatetime.strftime("%A")
    modifieddatetime = modifieddatetime.replace(" ", "")

    saltedpassword = salt + upass + modifieddatetime
    hashedpassword = hashlib.md5(saltedpassword.encode())
    hashedpassword = hashedpassword.hexdigest()
    return [hashedpassword, modifieddatetime]


# Function to hash the password
def passretreive(upass, timestamp):
    salt = "$3*&4&12KL"
    saltedpassword = salt + str(upass) + str(timestamp)
    hashedpassword = hashlib.md5(saltedpassword.encode())
    hashedpassword = hashedpassword.hexdigest()
    return hashedpassword


# Function to login the user
def checkpage(name, pwd):
    connection = sqlite3.connect("C:\\Users\\Joseph Richie\\PycharmProjects\\SecureSnake\\DB\\UserLogin.db")
    cur = connection.cursor()
    cur.execute("SELECT rowid FROM USER where USERNAME = '" + name + "';")
    usercheck = cur.fetchone()
    cur.execute("SELECT PASSWORD FROM USER where rowid = '" + str(usercheck[0]) + "';")
    pwdcheck = cur.fetchone()
    cur.execute("SELECT TIMESTAMP FROM USER where rowid = '" + str(usercheck[0]) + "';")
    timestampcheck = cur.fetchone()

    upass = passretreive(pwd, timestampcheck[0])

    # Build the app here, in the Temp.html page
    if upass == str(pwdcheck[0]):
        return render_template("Temp.html")
    else:
        return render_template("Unauthorized.html")


app = Flask(__name__)


# Renders the Main Page
@app.route('/')
def mainPage():
    return render_template('Index.html')


# Renders the page to create the new user
@app.route('/NewUser', methods=['POST'])
def NewUser():
    return render_template("NewUser.html")


# Page to create the new user
@app.route('/usercreate', methods=['POST'])
def usercreate():
    uname = request.form['newuser']
    upass = request.form['newpwd']
    upass = saltpass(upass)
    unamepass = "('" + uname + "', '" + upass[0] + "', '" + upass[1] + "')"
    connection = sqlite3.connect("C:\\Users\\Joseph Richie\\PycharmProjects\\SecureSnake\\DB\\UserLogin.db")
    cur = connection.cursor()

    cur.execute("SELECT rowid FROM USER where USERNAME = '" + uname + "';")
    usercheck = cur.fetchone()

    if usercheck is None:
        cur.execute("INSERT INTO USER (USERNAME, PASSWORD, TIMESTAMP) VALUES " + unamepass + ";")
        connection.commit()
        return render_template("Index.html")
    else:
        return render_template("UserExist.html")


# Page to Login
@app.route('/loginpage', methods=['POST'])
def loginpage():
    uname = request.form['user']
    upass = request.form['password']
    connection = sqlite3.connect("C:\\Users\\Joseph Richie\\PycharmProjects\\SecureSnake\\DB\\UserLogin.db")
    cur = connection.cursor()
    cur.execute("SELECT rowid FROM USER where USERNAME = '" + uname + "';")
    usercheck = cur.fetchone()

    if usercheck == None:
        return render_template("NewUser.html")
    else:
        return checkpage(uname, upass)


# Page to change the password
@app.route('/userchange', methods=['POST'])
def userchange():
    return render_template("PasswordChange.html")


# Logic to change the password
@app.route('/passchange', methods=['POST'])
def passchange():
    changeuser = request.form['newuser']
    changepass = request.form['newpwd']

    connection = sqlite3.connect("C:\\Users\\Joseph Richie\\PycharmProjects\\SecureSnake\\DB\\UserLogin.db")
    cur = connection.cursor()
    cur.execute("SELECT rowid FROM USER where USERNAME = '" + changeuser + "';")
    usercheck = cur.fetchone()

    if usercheck is None:
        return render_template("Unauthorized.html")
    else:
        newpass = saltpass(changepass)
        cur.execute("UPDATE USER SET PASSWORD = '" + newpass[0] + "',TIMESTAMP = '" + newpass[1] + "' where rowid = " + str(usercheck[0]) + ";")
        connection.commit()
        return render_template("Index.html")


# Runs the App
if __name__ == '__main__':
    app.run()
