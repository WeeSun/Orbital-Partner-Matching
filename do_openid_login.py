import webapp2

from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):
  # Redirect users to NUS OpenId for login. 

  def get(self):
    self.redirect(users.create_login_url('http://orbitalpartner.appspot.com/login', None, federated_identity='https://openid.nus.edu.sg/'))

app = webapp2.WSGIApplication([('/_ah/login_required', LoginHandler)],
                              debug=True)
