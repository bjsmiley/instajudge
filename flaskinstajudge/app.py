from flask import Flask, render_template, request, flash, redirect, url_for, session, logging, jsonify

from services.api import ClarifaiApi
from services.instagramScraper import verify_login, get_all_photos, move_dir, delete_dir
from services.serializer import load_object_json, save_object_json, check_for_object_json, delete_object_json

#from models.progress import Execution
import services.secret as ss

import functools

from random import randint


app = Flask(__name__)
api = ClarifaiApi()

look_up = {
    "user": None
}


# Check if user logged in
def is_logged_in(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap


# Index
@app.route('/')
def index():
    return render_template('home.html')


# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        #get form fields
        username = request.form['username']
        password = request.form['password']

        if verify_login(username, password, app.logger):

            # create session
            session['logged_in'] = True
            session['username'] = username
            session['password'] = password
            ss.password.set(password)

            flash('You are now logged in','success')
            return redirect(url_for('search'))
        else:
            error = 'Login failed for {0}'.format(username)
            return render_template('login.html', error=error )

    return render_template('login.html')

# Make a view for when the user tries to do something that also requires a password but it is already gone


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    ss.password.reset()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


# Public Search
@app.route('/public')
def public():
    return render_template('public.html')










def instagram(username): #202,404,203,201
    look_up['user'] = None

    #see if there is already a json object of its tags
    # if check_for_object_json( username ):
    #     tag_dict = load_object_json( "{0}.json".format(username) )
    #     response = jsonify(
    #         code = 202,
    #         message = "json object already exists",
    #         tags = tag_dict
    #     )
    #     return response
    
    #collect the photos and get a response
    res = get_all_photos( username=username, cur_user=session['username'], cur_password=session['password'], folder="users", logger=app.logger )
    if res['code'] == 404:
        # couldn't find the user
        response = jsonify(
            code = 404,
            message = "Could not find the user {}".format(username)
        )
    elif res["code"] == 409:
        # The user is private
        response = jsonify(
            code = 409,
            message = res["message"],
        )
        delete_object_json( "{0}.json".format(username) )
        delete_dir( folder_name=username )
    elif res["code"] == 200:
        response = jsonify(
            code = 201,
            message = "Found user and created directory",
            url = "/ajax/search?u={}&m=clarifai".format(username)
        )
        look_up['user'] = username
    else:
        response = jsonify(
            code = 6969,
            message = "Shit wtf",
        )

    return response

def clarifai(username):
    # confirm username
    if username != look_up['user']:
        response = jsonify(
            code = 405,
            message = "{} is the incorrect username, looking for {} instead".format(username, look_up['user'])
        )
        return response

    if check_for_object_json( username ):
        tag_dict = load_object_json( "{0}.json".format(username) )
        response = jsonify(
            code = 202,
            message = "json object already exists",
            tags = tag_dict
        )
        return response

    profile = api.create_profile_from_dir(username=username, folder="users", limit=10, logger=app.logger )
    tag_dict = profile.tag_info
    sorted_tags = sorted(tag_dict, key=lambda k: k['count'])
    save_object_json(obj=sorted_tags[::-1], filename="{0}.json".format(username))
    delete_dir( folder_name=username )

    look_up['user'] = None

    response = jsonify(
        code = 200,
        message = "All Complete!",
        tags = sorted_tags[::-1]
    )
    return response






# Private Search
'''
response = {
    code: 200 (completely done), 201 (first part is done), 202 (json object already exists), 203 (directory of photos already exists), 404 (username not found), 405 (incorrect username for second part)
}
'''
@app.route('/search', methods=['GET','POST'])
@is_logged_in
def search():
    look_up['user'] = None
    return render_template('search.html')


    

@app.route('/ajax/search', methods=['POST'])
@is_logged_in
def ajax_search():
    # get the query strings
    username = request.args["u"]
    method = request.args["m"]

    if method == "instagram-scraper":
        return instagram(username)
    if method == "clarifai":
        return clarifai(username)


# TODO:
# 1) stop storing password in session
# 4) give _bsmiley admin privaliges(?) to look over and delete directories
# 6) nsfw option
# 7) include nosql database for large json of user profiles
# 8) make a shell script to make development easier?
# 9) gunna have to use amazon s3 storage for user profile images perhaps? perhaps not..
# 10) FIX THIS FUCKING BUG

# DONE:
# 2) move profile directories into user/ once they are created
# 3) THEN continue with machine learning for each photo and create profile object and give to the view
# 5) figure out how to save an object locally maybe to a file? so I can save my api calls
# 5) make UI responsive when collecting images, then analyzing each image, then Done!
# 6) add links to tag dictionary
# 7) make tags clickable to display what photos corrispond to them
# 5) make preview photo's scrollable
# 2) handle when searching for a profile but they are private to you

if __name__ == '__main__':
    app.secret_key= ss.secret_key
    app.run(debug=True)