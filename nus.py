# Handlers for logged in pages

import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

# Datastore definition
class Profile(db.Model):
  """Models an individual with an name, sex, email, fb_link, linkedin_link, \
  orbital_level, orbital_country, preference, and date. The email, which \
  should be unique is used as key. """
  name = db.StringProperty()
  sex = db.StringProperty()
  email = db.StringProperty()
  fb_link = db.StringProperty()
  linkedin_link = db.StringProperty()
  orbital_level = db.StringProperty()
  orbital_country = db.StringProperty()
  preference = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

# These classes generates pages from templates
class MainPage(webapp2.RequestHandler):
  """ Front page for those logged in """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('front.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class NUSPolicy(webapp2.RequestHandler):
  """ Handler for privacy policy page."""
  def get(self):
    user = users.get_current_user()
    if user: # if logged in 
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('privacy.html')
      self.response.out.write(template.render(template_values))    
    else: # not logged in 
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class Login(webapp2.RequestHandler):
  """ Checks whether profile already exists, if not create profile """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      # Check whether profile exists
      db_key =  db.Key.from_path('Profile',users.get_current_user().email())
      profile = db.get(db_key)

      if profile == None:
        template = jinja_environment.get_template('getprofile.html')
      else:
        template = jinja_environment.get_template('front.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))
class EditProfile(webapp2.RequestHandler):
  """ Retrieves profile and prefill the form for editing """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieves profile
      db_key =  db.Key.from_path('Profile',users.get_current_user().email())
      profile = db.get(db_key)

      if profile != None:
        male_checked = female_checked = Boctok_checked = Gemini_checked = Appollo11_checked = "";
        
        # For filling in radio button for sex
        if profile.sex == 'Male':
          male_checked = 'checked'
        else:
          female_checked = 'checked'
          
        # For filling in radio button for Orbital level
        if profile.orbital_level == 'Boctok':
          Boctok_checked = 'checked'
        elif profile.orbital_level == 'Gemini':
          Gemini_checked = 'checked'
        else:
          Appollo11_checked = 'checked'
      
        template_values = {
          'profile': profile,
          'male_checked': male_checked,
          'female_checked': female_checked,
          'Boctok_checked': Boctok_checked,
          'Gemini_checked': Gemini_checked,
          'Appollo11_checked': Appollo11_checked,
          'preference': cgi.escape(profile.preference),  # html escaping
          'home': self.request.host_url,
          'user_mail': users.get_current_user().email(),
          'logout': users.create_logout_url(self.request.host_url),
          } 
        template = jinja_environment.get_template('editprofile.html')
        self.response.out.write(template.render(template_values))
      else:
        self.redirect('/login')
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class Search(webapp2.RequestHandler):
  """ Creates search form """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('search.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class Display(webapp2.RequestHandler):
  """Display the result of search query """
  def post(self):

    sex = self.request.get('sex')
    level = self.request.get('orbital_level')
    country = self.request.get('orbital_country')

    if country == "Anywhere":
      profiles = db.GqlQuery("SELECT *"
                             "FROM Profile "
                             "WHERE sex = :1 "
                             "AND orbital_level = :2 "
                             "ORDER BY date DESC",
                             sex, level)
    else:
      profiles = db.GqlQuery("SELECT *"
                             "FROM Profile "
                             "WHERE sex = :1 "
                             "AND orbital_level = :2 "
                             "AND orbital_country = :3 "
                             "ORDER BY date DESC",
                             sex, level, country)

    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'profiles': profiles,
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('display.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class AdminDisplay(webapp2.RequestHandler):
  """ Creates page to get info for admin """
  def get(self):
    profiles = db.GqlQuery("SELECT *"
                           "FROM Profile "
                           "ORDER BY date DESC")
    
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'profiles': profiles,
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('admin.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

# These classes process requests

class CreateProfile(webapp2.RequestHandler):
  """ Process data from user and creates a new profile """
  def post(self):
    if users.get_current_user():
      profile = Profile(key_name=users.get_current_user().email())
      profile.name = self.request.get('user_name')
      profile.email = users.get_current_user().email()
      profile.sex = self.request.get('sex')
      profile.fb_link = self.request.get('fb_link')
      profile.linkedin_link = self.request.get('linkedin_link')
      profile.orbital_level = self.request.get('orbital_level')
      profile.orbital_country = self.request.get('orbital_country')
      profile.preference = self.request.get('preference')   
      profile.put()
      self.redirect('/nus')
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

class Edit(webapp2.RequestHandler):
  """ Edit the profile then stores it """
  def post(self):
    if users.get_current_user():
      # Get key from database
      db_key =  db.Key.from_path('Profile',users.get_current_user().email())
      profile = db.get(db_key) # Retrieve profile
      
      if self.request.get('delete')=='Yes': # Delete profile
        db.delete(profile)
        self.redirect(users.create_logout_url(self.request.host_url))
      else: # Edit profile
        profile.name = self.request.get('user_name')
        profile.sex = self.request.get('sex')
        profile.fb_link = self.request.get('fb_link')
        profile.linkedin_link = self.request.get('linkedin_link')
        profile.orbital_level = self.request.get('orbital_level')
        profile.orbital_country = self.request.get('orbital_country')
        profile.preference = self.request.get('preference')   
        profile.put()
        self.redirect('/nus')
        
      
class Admin(webapp2.RequestHandler):
  """ Process admin request """
  def post(self):
    all = self.request.get('select_all')
    if all:
      profiles = db.GqlQuery("SELECT *"
                             "FROM Profile ")
    else:
      selected = self.request.get_all('selected')
      profiles = db.GqlQuery("SELECT *"
                             "FROM Profile "
                             "WHERE email in :1",
                             selected)
    db.delete(profiles)
    self.redirect('/nus')


app = webapp2.WSGIApplication([('/nus', MainPage),
                               ('/nuspolicy', NUSPolicy),
                               ('/login', Login),
                               ('/profile', CreateProfile),
                               ('/editprofile', EditProfile),
                               ('/edit', Edit),
                               ('/search', Search),
                               ('/display', Display),
                               ('/admindisplay', AdminDisplay),
                               ('/admin', Admin)],
                              debug=True)
