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

USER_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")    #Regular Expressions (Regex)
def valid_username(username):
    return username and USER_REGEX.match(username)

PASSWORD_REGEX = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_REGEX.match(password)

EMAIL_REGEX = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_REGEX.match(email)

params = dict(username = "",
              error_username = "",
              error_password = "",
              error_verify = "",
              error_email = "",
              email = "")

form = """
<title>Signup</title>
<form name="form" method="post">
<h1>Signup</h1>
    <table>
        <tbody>
            <tr>
                <td>
                    <label>Username </label>
                </td>
                <td>
                    <input name="username" type="text" value=%(username)s>
                </td>
                <td>
                    <span class="error" style="color: red">%(error_username)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label>Password </label>
                </td>
                <td>
                    <input name="password" type="password">
                </td>
                <td>
                    <span class="error" style="color: red">%(error_password)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label>Verify Password </label>
                </td>
                <td>
                    <input name="verify" type="password">
                </td>
                <td>
                    <span class="error" style="color: red">%(error_verify)s</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label>Email (optional) </label>
                </td>
                <td>
                    <input name="email" type="text" value=%(email)s>
                </td>
                <td>
                    <span class="error" style="color: red">%(error_email)s</span>
                </td>
            </tr>
        </tbody>
    </table>
    <input type="submit">
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form % params)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        params = dict(username = username,
                      error_username = error_username,
                      error_password = error_password,
                      error_verify = error_verify,
                      error_email = error_email,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "The passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.response.out.write(form % params)
        else:
            self.redirect("/welcome?username=" + cgi.escape(username, quote=True))

class Welcome(MainHandler):
    def get(self):
        username = self.request.get('username')
        users = dict(username = username)
        welcome = """
        <title>Welcome</title>
        <h1>Welcome, %(username)s</h1>
        """
        if valid_username(username):
            self.response.out.write(welcome % users)
        else:
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
