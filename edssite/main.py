#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, jinja2, os, re
from google.appengine.api import mail

template_dir = (os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)

class Handler(webapp2.RequestHandler):
    """Helper class with all the useful methods that my request handlers will need"""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

"""
Handlers for the front page, and "/" that redirects to "/home"
"""

class MainHandler(Handler):
    def get(self):
        self.redirect('/home')

class FrontpageHandler(Handler):
    def get(self):
        self.render('index.html')

    def post(self):
        name   = self.request.get("name")
        email  = self.request.get("email")
        number = self.request.get("number")
        body   = self.request.get("body")

        mail.send_mail(sender = "bradycpeters@gmail.com",
                        to = "<fitnessstl@gmail.com>",
                        subject = "business inquiry",
                        body = "Name: {} \n Email: {} \n Contact number: {} \n Message: {}".format(name,email,number,body))

        self.redirect("/home")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', FrontpageHandler),
], debug=True)
