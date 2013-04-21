Orbital Partner Matching is a little app I built to learn how to use 
Google App Engine with Python. It is hosted at 
http://orbitalpartner.appspot.com/ and used by NUS School of Computing
students to find partners for the Orbital Programme.

The code uses Jinja2 for templates, Twitter Bootstrap for CSS styles and 
a bit of jQuery.

Templates are placed in the 'templates' directory. The two main base 
templates are 
 - base0.html which contains the navigation elements for
   pages that are used both for logged-in users and non-logged-in users.
 - base1.html which contains navigation elements for logged-in users.
The files front.html and privacy.html inherits from base0.html and the
other files inherit from base1.html

The Python functions are placed in orbitalpartner.py for pages that do 
not require login and nus.py for pages that require login. NUS OpenId is
used for login - this is handled in do_openid_login.py.

Lee Wee Sun
