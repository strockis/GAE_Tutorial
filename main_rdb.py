import os
import logging

from google.appengine.api import rdbms
from google.appengine.ext import webapp

import jinja2

template_path = os.path.join(os.path.dirname(__file__))

jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path)
)

CLOUDSQL_INSTANCE = ''
DATABASE_NAME = 'guestbook'
USER_NAME = '<var>username</var>'
PASSWORD = '<var>password</var>'

def get_connection():
    return rdbms.connect(instance=CLOUDSQL_INSTANCE, database=DATABASE_NAME,
                         user=USER_NAME, password=PASSWORD, charset='utf8')

class MainHandler(webapp.RequestHandler):
    def get(self):
        # Viewing guestbook
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT guest_name, content, created_at FROM entries '
                       'ORDER BY created_at DESC limit 20')
        rows = cursor.fetchall()
        conn.close()
        template_values = {"rows": rows}
        template = jinja2_env.get_template('index.html')
        self.response.out.write(template.render(template_values))


class GuestBook(webapp.RequestHandler):
    def post(self):
        # Posting a new guestbook entry
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (guest_name, content) '
                       'VALUES (%s, %s)',
                       (self.request.get('guest_name'),
                        self.request.get("content")))
        conn.commit()
        conn.close()
        self.redirect("/")


app = webapp.WSGIApplication(
    [
        ("/", MainHandler),
        ("/sign", GuestBook),
    ],
    debug=True
)





