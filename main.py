import webapp2
import os
import jinja2
from google.appengine.api import users

jinja_environment = jinja2.Environment(autoescape=True,
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = dict (
                greet = "It works! Hello from localhost"
        )

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
            debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
