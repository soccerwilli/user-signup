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
import webapp2
import cgi
import re

form = """
<form action="/signup" method="post">
    <h1>User Signup</h1>
        <label>Username </label>
            <input type="text" name="username" value=%(username)s>
                <div style="color: red">%(error)s</div><br>
        <label>Password </label>
            <input type="password" name="password">
                <div style="color: red">%(error)s</div><br>
        <label>Verify Password </label>
            <input type="password" name="verify">
                <div style="color: red">%(error)s</div><br>
        <label>Email (optional) </label>
            <input type="text" name="email" value=%(email)s>
                <div style='color: red'>%(error)s</div><br><br>
            <input type="submit"/><br>
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self, error=""):
        self.response.out.write(form % {"error": error})


USERNAME_REG = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USERNAME_REG.match(username)

PASSWORD_REG = re.compile(r"^.{3-20}$")
def valid_password(password):
    return password and PASSWORD_REG.match(password)

EMAIL_REG = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_REG.match(email)

class Signup(MainHandler):
    def get(self, error=""):
            self.response.out.write(form % {"error": error})

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            error = "That's not a valid username."
            self.response.out.write(error)
            have_error = True
        if not valid_password(password):
            error = "That's not a valid password."
            self.response.out.write(error)
            have_error = True
        elif password != verify:
            error = "The passwords didn't match."
            self.response.out.write(error)
            have_error = True
        if not valid_email(email):
            error = "That's not a valid email."
            self.response.out.write(error)
            have_error = True
        if have_error:
            self.redirect('/signup')
        else:
            self.redirect('/welcome')

class Welcome(MainHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write("Welcome, " + username)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
