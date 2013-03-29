# Handlers for logged in pages

import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'policy': '/policy',
        'home_name': 'Home',
        'policy_name': 'Privacy Policy',
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'logout_name': 'Logout',
        } 
      template = jinja_environment.get_template('front.html')
      self.response.out.write(template.render(template_values))
    else:
       self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))
      
app = webapp2.WSGIApplication([('/nus', MainPage)],
                              debug=True)
