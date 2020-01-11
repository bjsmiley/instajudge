from secret import secret_username #, secret_public_username, secret_public_password
import subprocess, os, shutil

# =============================================== [START] Helper Functions ===============================================

def log( string, logger):
    if logger:
        logger.info( string )

def move_dir(source, destination, logger=None):
        shutil.move(src=source, dst=os.path.join("static",destination))

def delete_dir(folder_name):
        shutil.rmtree( os.path.join("static", "users", folder_name) )

# =============================================== [ END ] Helper Functions ===============================================






# ============================================= [START] Logging In Functions =============================================
def verify_login( username, password, logger=None ):
    log( "logging in...", logger )
    cmd = "instagram-scraper {0} -u {1} -p {2}".format( secret_username, username, password ).split()
    #log( cmd, logger )

    output = subprocess.check_output( cmd )
    #log( output, logger )

    return confirm_login_with_log(logger)

def confirm_login_with_log(logger=None):
    #parent_dir = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
    #path_to_file = os.path.join( parent_dir , "instagram-scraper.log" )
    #parent_dir = os.path.dirname( os.getcwd() )


    # os.getcwd() == /mnt/c/Users/bryan/Desktop/Programs/python/machine_learning/instajudge/flaskinstajudge
    current_dir = os.getcwd()
    path_to_file = os.path.join( current_dir , "instagram-scraper.log")

    log_file = open( path_to_file, 'r' )
    #lineOne = log.readline()
    
    
    for line in log_file:
            response = line.split(" - ")[3].rstrip()
            if response == "Error getting user details for {0}. Please verify that the user exists.".format(secret_username):
                    log( "login attempt: SUCCESSFUL", logger)
                    return True
            else:
                    log( "login attempt: FAILED", logger)
                    #log( response, logger)
    return False    

    #correctResponse = lineOne.split(" - ")[3].rstrip()
    #log( correctResponse , logger )
    #return correctResponse == "Error getting user details for {0}. Please verify that the user exists.".format(secret_username)

# ============================================= [ END ] Logging In Functions =============================================




# ============================================== [START] Searching Functions ==============================================

def confirm_search_with_log(username, logger=None):
        current_dir = os.getcwd()
        path_to_file = os.path.join( current_dir , "instagram-scraper.log")

        log_file = open( path_to_file, 'r' )

        for line in log_file:
                response = line.split(" - ")[3].rstrip()
                if response == "Error getting user details for {0}. Please verify that the user exists.".format(username):
                        return {"code": 404, "message": "Could not find the user {0}".format(username)} #False
                if response == "User {0} is private".format(username):
                        return {"code": 409, "message": response}
                else:
                        log( response, logger )
        return {"code": 200, "message": "user found"} #True
        #log( correctResponse , logger )
        #return errorResponse != "Error getting user details for {0}. Please verify that the user exists.".format(username)



def get_all_photos( username, cur_user, cur_password, folder="users",logger=None):
                #log("( {0} , {1} )".format(cur_user, cur_password), logger)
                #see if the folder already exists in @folder
        #directory = os.path.join( os.getcwd() , "static", folder )

                # WARNING: POTENTIAL SECURITY RISK, a user not following can still find a directory if it exists and look it up
        # if os.path.isdir( os.path.join( directory, username) ):
        #         log("{0} exists as a directory in {1}".format(username, directory), logger)
        #         return {"code": 201, "message": "user has already been found"} # True
        # else:
        #         log("{0} DOES NOT exists as a directory in {1}".format(username, directory), logger)
        #         return exec_search( username=username, current_user=cur_user, current_password=cur_password, logger=logger )
        return exec_search( username=username, current_user=cur_user, current_password=cur_password, logger=logger )

def exec_search( username, current_user, current_password, logger=None ):

        cmd = "instagram-scraper {0} -u {1} -p {2} -d {3}".format( username, current_user, current_password, os.path.join("static","users", username) ).split()
        log( "Executing Search...", logger )
        output = subprocess.check_output( cmd )
        log( "Done!", logger )
        #log( output, logger )
        log( "NOW CONFIRMING IF THE SEARCH WORKED...", logger )
        return confirm_search_with_log(username, logger)

# ============================================== [ END ] Searching Functions ==============================================


