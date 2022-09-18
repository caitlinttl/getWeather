# -*- coding: UTF-8 -*-
# Created by Caitlin, Hsinchu, Taiwan, 2021.
# Test the Flask web framework.
# ----------------------------------------------------------

from flask import Flask
from flask import jsonify
from flask import request
import urllib.request
import json
# from ip2geotools.databases.noncommercial import DbIpCity

# print a nice greeting.
def say_hello(username = ""):
    return '<p>Hello %s! How are you?</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> 
    <title>Caitlin Flask Test</title> 
    <link rel="icon" href="/static/img/icon_cat.ico">
    <link rel="apple-touch-icon" href="/static/img/icon_cat.ico">
    </head>\n<body>'''
instructions = '''
    <p>Welcome to Caitlin test web.</p>\n
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/yourName</code>) to say hello to
    someone specific.</p>\n
    <p><a href="/ip/json">click to get your ip</a></p>\n
    <!-- <img src="/static/img/penguin_map_name.jpg" width="1500"> -->
    '''
home_link = '<p><a href="/">Back to Main Page</a></p>\n'
footer_text = '</body><br>Just for test.\n</html>'
# the end of the page

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config['JSON_SORT_KEYS'] = False

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))


@application.route("/ip/json", methods=["GET"])
def get_user_ip():

    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.get("X-Forwarded-For").split(',')[0]
    else:
        user_ip = request.remote_addr    

    ip_api_url = "http://ip-api.com/json/"
    req = urllib.request.Request(ip_api_url + user_ip)
    response = urllib.request.urlopen(req).read()
    json_response = json.loads(response.decode('utf-8'))

    status = json_response['status']
    if status == "fail":
        return jsonify({'ip': user_ip}), 200
    else:
        return jsonify({
            'ip': user_ip,
            'country': json_response['country'],
            'countryCode': json_response['countryCode'],
            'region': json_response['region'],
            'regionName': json_response['regionName'],
            'city': json_response['city'],
            'zip': json_response['zip'],
            'latitude': json_response['lat'],
            'longitude': json_response['lon'],
            'timezone': json_response['timezone'],
            'isp': json_response['isp'],
            'org': json_response['org'],
            'as': json_response['as'],
            'status': json_response['status']
            }), 200


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8000)