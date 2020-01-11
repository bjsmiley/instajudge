class Image:

    '''
    id: string
                              id tag  percent
    tags: array of tuples - [(str,str,int)]
    status: str
    code: int

    
    '''

    def __init__(self, response):
        self.id = response['outputs'][0]['id']
        self.status = response['status']['description']
        self.code = response['status']['code']
        self.tags = []
        for output_tag in response['outputs'][0]['data']['concepts']:
            self.tags.append( (output_tag['id'] , output_tag['name'] , output_tag['value']) )
    
    def printTags(self):
        for t in self.tags:
            print("[ {0}: {1} ({2})".format(t[0],t[1],t[2]))