# Handlers for pages that do not require log in

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
  """ Handler for the front page."""
  def get(self):
    user = users.get_current_user()
    if user:   # if logged in
      template_values = {
        'home': self.request.host_url,
        'policy': '/policy',
        'home_name': 'Home',
        'policy_name': 'Privacy Policy',
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.uri),
        'logout_name': 'Logout',
        }      
    else: # not logged in
      login_string = 'Login'
      template_values = {
        'home': self.request.host_url,
        'policy': '/policy',
        'login': '/nus',
        'home_name': 'Home',
        'policy_name': 'Privacy Policy',
        'login_name': 'Login',
        }
    template = jinja_environment.get_template('front.html')
    self.response.out.write(template.render(template_values))

class Privacy(webapp2.RequestHandler):
  """ Handler for privacy policy page."""
  def get(self):
    user = users.get_current_user()
    if user: # if logged in 
      template_values = {
        'home': self.request.host_url,
        'policy': '/policy',
        'home_name': 'Home',
        'policy_name': 'Privacy Policy',
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.uri),
        'logout_name': 'Logout',
        }
    else: # not logged in 
      login_string = 'Login'
      template_values = {
        'home': self.request.host_url,
        'policy': '/policy',
        'login': '/nus',
        'home_name': 'Home',
        'policy_name': 'Privacy Policy',
        'login_name': 'Login',
        }
    template = jinja_environment.get_template('privacy.html')
    self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage), ('/policy', Privacy)],
                              debug=True)
