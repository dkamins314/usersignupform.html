from flask import Flask, request, redirect
import jinja2
import os
import re
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
app = Flask(__name__)
app.config['DEBUG'] = True
def is_empty(field):
    if field == "":
        return True
    else:
        return False
def is_invalid_char(field):
    for char in field:
        if char.isspace():
            return True
    return False
def is_invalid_length(field):
    if len(field) > 3 and len(field) < 20:
        return False
    else:
        return True
def is_invalid_verify_pass(field1, field2):
    if field1 == field2:
        return False
    else:
        return True
def is_invalid_email(field):
    if field == "":
        return False
    elif re.match(r"(^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$)", field):
        return is_invalid_length(field)
    else:
        return True
@app.route("/")
def index():
    template = jinja_env.get_template("signup_form.html")
    return template.render()
@app.route("/", methods=["POST"])
def validate_signup_form():
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify_password"]
    email = request.form["email"]
    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""
    empty_input_msg = "Please submit a valid input."
    invalid_name_pass_msg = "Must be between 3 and 20 characters, no spaces."
    invalid_verify_pass_msg = " Must match the previous password."
    invalid_email_msg = "Please submit a valid email."
    if is_empty(username):
        username_error = empty_input_msg
    else:
        if is_invalid_char(username) or is_invalid_length(username):
            username_error = invalid_name_pass_msg
    if is_empty(password):
        password_error = empty_input_msg
    else:
        if is_invalid_char(password) or is_invalid_length(password):
            password_error = invalid_name_pass_msg
    if is_empty(verify_password):
        verify_password_error = empty_input_msg
    else:
        if is_invalid_verify_pass(password, verify_password):
            verify_password_error = invalid_verify_pass_msg
    if is_invalid_email(email):
        email_error = invalid_email_msg
    if not username_error and not password_error and not verify_password_error and not email_error:
        return redirect("/welcome?username={0}".format(username))
    else:
        template = jinja_env.get_template("signup_form.html")
        return template.render(username_error=username_error, password_error=password_error,
                               verify_password_error=verify_password_error, email_error=email_error)
@app.route("/welcome")
def welcome():
    username = request.args.get("username")
    template = jinja_env.get_template("signup_welcome.html")
    return template.render(name=username)
app.run()