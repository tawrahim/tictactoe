import webapp2
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

jinja_environment = jinja2.Environment(autoescape=True,
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


# When the user starts the app this is what they are
# going to see at first
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        url_login = users.create_login_url(self.request.uri)

        template_values = dict (
                greet = "It works! Hello from localhost",
                logout = url,
                logout_linktext = "Logout",
                login = url_login
        )
        if user:
            obj = user.nickname()

            template = jinja_environment.get_template('gamepage.html')
            self.response.out.write(template.render(template_values))
            self.response.out.write('Hello, ' + user.nickname())
        else:
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))

# This is the gameboard, all the models for the user needs
# to be placed here so that we can query for information
class GameBoard(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        template_values = dict (
                greet = "It works! Hello from localhost",
                logout = url,
                logout_linktext = "Logout"
        )

        template = jinja_environment.get_template('gamepage.html')
        self.response.out.write(template.render(template_values))
    
    # Post method to post stuffs to the db
    def post(self):
        pass

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/gamepage', GameBoard)],
                             debug=True) 

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
