from secret import apikey
from image import Image

from clarifai.rest import ClarifaiApp



app = ClarifaiApp(api_key=apikey)

model = app.public_models.general_model
response =  model.predict_by_url('https://samples.clarifai.com/metro-north.jpg') 

#if response['status']['code'] is '10000':
#print( type(response['status']['code']))
#print( response['outputs'][0]['data']['concepts'] )
#print( response['outputs'][0]['id'] )

im = Image( response )

im.printTags()




