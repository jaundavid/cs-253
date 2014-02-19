import webapp2
import cgi
import string
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


application = webapp2.WSGIApplication([
    ('/', MainPage),('/rot13',Rot13),
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
