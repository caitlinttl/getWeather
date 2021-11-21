# -*- coding: UTF-8 -*-
# Created by Caitlin, Hsinchu, Taiwan, 2021.
# Test the Flask web framework.
# ----------------------------------------------------------

from flask import Flask

# print a nice greeting.
def say_hello(username = ""):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> 
    <title>Caitlin Flask Test</title> 
    <link rel="icon" href="/static/img/icon_cat.ico">
    <link rel="apple-touch-icon" href="/static/img/icon_cat.ico">
    </head>\n<body>'''
instructions = '''
    <p>Welcome to Penguin Cabin.</p>\n
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/yourName</code>) to say hello to
    someone specific.</p>\n
    <img src="/static/img/penguin_map_name.jpg" width="1500">
    '''
home_link = '<p><a href="/">Back to Main Page</a></p>\n'
footer_text = '</body><br>Just for test.\n</html>'
# the end of the page

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)