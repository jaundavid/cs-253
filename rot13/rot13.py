import webapp2
import cgi
import string
import re
from google.appengine.api import users

form = """
<form method=post>
  <label> <h1> Enter some text to ROT13 </h1>
    <br>
    <input type="textarea" style="height: 100px; width: 400px;"
                name="text" value="%(ROT13)s">
  </label>
  <br>
  <input type="submit">
</form>
"""
singinform = """
<h1> Signup </h1>
<form method=post>
 <table>
 <tr>
 <td>
  <label> Username:
    <input name="username">
  </label>
  </td>
  <td> %(usernamerror)s  </td>
  </tr>
  <tr>
 <td>
  <label> Password:
    <input name="password">
  </label>
  </td>
  <td>  %(passerror)s  </td>
  </tr>
  <tr>
 <td>
  <label> Verify (password):
    <input name="verify">
   </label>
  </td>
  <td>  %(verifyerror)s  </td>
  </tr>
  <tr>
 <td>
  <label> Email:
    <input name="email">
  </label>
  </td>
  <td>  %(emailerror)s  </td>
  </tr>
  </table>
  <input type="submit">
</form>
"""
class MainPage(webapp2.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.write("Hello, Udacity!")

class Rot13(webapp2.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      text = self.request.get("text")
      self.response.write(writeform())
    def post(self):
      self.response.headers['Content-Type'] = 'text/html'
      text = self.request.get("text")
      self.response.write(writeform(text))

class SignUp(webapp2.RequestHandler):
    def get(self):
      errors = {'emailerror':"",'usernamerror':"",'passerror':"",'verifyerror':""}
      self.response.headers['Content-Type'] = 'text/html'
      self.response.write(singinform % errors)
    def post(self):
      errors = {'emailerror':"",'usernamerror':"",'passerror':"",'verifyerror':""}
      username = self.request.get("username")
      password = self.request.get("password")
      verify = self.request.get("verify")
      email = self.request.get("email")
      validemail = validEmail(email)
      validusername = validUsername(username)
      validpass = validPassword(password)
      validverify = password == verify
      if not validemail:
        errors['emailerror'] = "That's not a valid email."
      if not validusername:
        errors['usernamerror'] = "That's not a valid username."
      if not validpass:
        errors['passerror'] = "That wasn't a valid password."
      if not validverify:
        errors['verifyerror'] = "Your passwords didn't match."
        self.response.headers['Content-Type'] = 'text/html'
      if validpass and validverify and validusername and validemail:
        self.redirect("/welcome?username="+username)
      else:
        self.response.write(singinform % errors)

class Welcome(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.write("Welcome, " + self.request.get("username"))

application = webapp2.WSGIApplication([
    ('/', MainPage),('/rot13',Rot13), ('/signup',SignUp),('/welcome',Welcome),
], debug=True)

def writeform(text=""):
  text = rot13(text)
  return form % {"ROT13":text}

def rot13(text):
  rot13 = ""
  for c in text:
    ord_c = ord(c)
    if 65 <= ord_c <= 90:
      ord_c = (ord_c - 65 + 13) % 26 + 65
    elif 97 <= ord_c <= 122:
      ord_c = (ord_c - 97 + 13) % 26 + 97
    rot13+= unichr(ord_c)
  return rot13

def validPassword(password):
  pass_re = re.compile(r"^.{3,20}$")
  return pass_re.match(password)

def validEmail(email):
  email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
  return email_re.match(email) or email == ""

def  validUsername(username):
  user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
  return user_re.match(username)
