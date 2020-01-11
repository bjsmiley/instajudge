class Image:

    '''
    id: string
                              id tag  percent
    tags: array of tuples - [(str,str,int)]
    status: str
    code: int

    
    '''

    def __init__(self, res, url):
        '''
            extract the request id, status, code, and tags (id, name, value) for an image

        '''
        self.id = res['outputs'][0]['id']
        self.status = res['status']['description']
        self.code = res['status']['code']
        self.tags = []
        for output_tag in res['outputs'][0]['data']['concepts']:
            self.tags.append( (output_tag['id'] , output_tag['name'] , output_tag['value']) )
        self.url = url
    
    def stringTags(self):
        '''
            stringTags - return a formatted string of all the tags for this image
        '''

        rt = "" # initalize return object

        # get all tags
        for t in self.tags:
            rt += "[ {0}: {1} ({2}) ]".format(t[0],t[1],t[2])

        return rt

    def getTagNames(self):
        '''
            getTagNames - get a list of the actual tags for an image
            return: array of strings
        '''

        rt = []
        for t in self.tags:
            rt.append( t[1] )
        return rt

    def getTagsAndPercentage(self):
        rt = []
        for t in self.tags:
            rt.append( (t[1],t[2]) )
        return rt