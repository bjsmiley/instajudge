import pickle, os, json


# ===================
#       pickle
# ===================

def save_object_pkl( obj , filename ):
    path_to_file = os.path.join( os.getcwd(), "pickles", filename)    
    #with open(path_to_file, 'wb') as file:
    #    pickle.dump(obj, file)
    file = open(path_to_file, 'wb')
    pickle.dump(obj, file)
    file.close()

def load_object_pkl( filename ):
    path_to_file = os.path.join( os.getcwd(), "pickles", filename)    
    #with open(path_to_file, 'rb') as file:
    #    return pickle.load(file)
    file = open(path_to_file, 'rb')
    obj = pickle.load(file)
    file.close
    return obj

def check_for_object_pkl( username ):
        file_path = os.path.join( os.getcwd(), "pickles", "{0}.pkl".format(username) )
        return os.path.isfile(file_path)


# ===================
#       json
# ===================

def save_object_json( obj , filename ):

        path_to_file = os.path.join( os.getcwd(), "json", filename)

        with open(path_to_file, 'w') as file:
                json.dump(obj, file, indent=4)


def load_object_json( filename ):

        path_to_file = os.path.join( os.getcwd(), "json", filename)

        with open(path_to_file, 'r') as file:
                obj = json.load(file)

        return obj

def check_for_object_json( username ):
        file_path = os.path.join( os.getcwd(), "json", "{0}.json".format(username) )
        return os.path.isfile(file_path)
        # does_exist = os.path.isfile(file_path)
        # if does_exist:
        #         json_length = len(load_object_json( "{0}.json".format(username) ))

        # else:
        #         return False

def delete_object_json( filename ):
        file_path = os.path.join( "json", filename )
        if os.path.isfile(file_path):
                os.remove( file_path )