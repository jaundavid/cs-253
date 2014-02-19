import webapp2
import cgi
from google.appengine.api import users

form = """
<form method="get" >
  <label> One
    <input type="radio" name="q" value="one">
  </label>
  <label> Two
    <input type="radio" name="q" value="two">
  </label>
  <label> Three
    <input type="radio" name="q" value="three">
  </label>
  <br>
  <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(form)
        else:
            self.redirect(users.create_login_url(self.request.uri))

class TestForm(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request)
        self.response.write(cgi.escape(form,quote=True))


application = webapp2.WSGIApplication([
    ('/', MainPage),('/testform',TestForm),
], debug=True)
