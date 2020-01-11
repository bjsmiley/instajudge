from secret import apikey
#from serializer import save_object
from models.image import Image
from models.profile import Profile

from clarifai.rest import ClarifaiApp

import os

class ClarifaiApi:
    
    def __init__(self):
        #
        #   set up model for image visualization
        #
        
        self.app = ClarifaiApp(api_key=apikey)   
        self.model = self.app.public_models.general_model

    def log(self, string, logger):
        if logger:
            logger.info( string )

    def cut_url(self, string ):
        index = string.find("/static/")
        if index == -1: return ""
        return string[index:]


    def analyze_image_url(self,url):
        #
        #   analyze_image_url - get an Image that is readable
        #   url: the image url
        #   returns an Image model
        #
        response =  self.model.predict_by_url(url)
        return Image(res=response)

    def analyze_image_file(self, absolute_file_path, relative_file_path):
        #
        #   analyze_image_file - get an Image that is readable
        #   url: the image filename (path included)
        #   returns an Image model
        #
        response = self.model.predict_by_filename(absolute_file_path)
        #rel_path = self.cut_url(file)
        rel_path = relative_file_path
        return Image(res=response, url=rel_path)

    def create_profile_from_dir(self, username, folder, limit=50, logger=None):
        profile = Profile(username)

        profile_dir = os.path.join(os.getcwd(), "static", folder, username)
        self.log("creating profile object...", logger)
        self.log("looking at {0}".format(profile_dir), logger)
        count = 0
        for filename in os.listdir( profile_dir ):
            count += 1
            if count > limit:
                break
            self.log("file {0} analysis.".format(count), logger)
            
            if not filename.endswith(('.png', '.jpg', '.jpeg')):
                self.log("{0} does not end with .jpg or .png or .jpeg".format(filename), logger)
                continue
            abs_path_to_image = os.path.join( profile_dir, filename )
            relative_url_to_image = os.path.join( "static", folder, username, filename )
            self.log("file location: {}".format(relative_url_to_image), logger)
            image = self.analyze_image_file( abs_path_to_image, relative_url_to_image )
            profile.add_image( image )
            self.log("image saved.", logger)

        profile.finish_averages()
       
        
        return profile



