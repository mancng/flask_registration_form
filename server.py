from flask import Flask, render_template, redirect, request, session, flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$')

app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def submit():
    errors = False
    #Validate Blank Fields
    if len(request.form['name_first']) < 1 or len(request.form['name_last']) < 1 or len(request.form['email']) < 1 or len(request.form['password']) < 1 or len(request.form['password_con']) < 1:
        flash("***All fields are mandatory and cannot be blank.", "all_err")
        errors = True

    #Validate Email
    if not EMAIL_REGEX.match(request.form['email']):
        flash("***Invalid Email Address!", "email_err")
        errors = True
    
    #Validate First and Last Names
    if not NAME_REGEX.match(request.form['name_first']) or not NAME_REGEX.match(request.form['name_last']):
        flash("***First Name or Last Name cannot contain any numbers", "name_err")
        errors = True

    #alternative way to limit input to be letters only
    # if not request.form['name_first'].isalpha() or not request.form['name_last'].isalpha():

    #Validate Password character count
    if len(request.form['password']) < 9:
        flash("***Password must be more than 8 characters.", "pass_err")
        errors = True
    elif not PASS_REGEX.match(request.form['password']):
        flash("***Password must contain at least 1 uppercase letter and 1 numeric value.")

    #Validate Confirm Password
    if request.form['password_con'] != request.form['password']:
        flash("***Confirm password doesn't match!")
        errors = True

    name_first = request.form['name_first']
    name_last = request.form['name_last']
    email = request.form['email']

    if errors:
        return redirect('/')
    else:
        return redirect('/success')

@app.route('/success')
def success():
    return render_template('result.html')

app.run(debug=True)