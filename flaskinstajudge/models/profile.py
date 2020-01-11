class Profile:

    images = []
    tag_info = [] # [
                  #     {"name" : str, "prob": float, "count", int, "urls": list}
                  # ]

    avg_prob_taken  = False

    def __init__(self, profile_name):
        self.name = profile_name

    def finish_averages(self):
        avg_prob_taken = True
        for tag in self.tag_info:
            tag["prob"] /= tag["count"]

    def add_image(self, image):
        if image.code != 10000:
            return
        self.images.append( image )

        self.collect_all_tags( image )

    def collect_all_tags(self, image):

        # get all tags for thiis profile
        current_tags = self.getTagNames()

        # for each tag in this photo
        for id,tag,prob in image.tags:

            # check if the tag already exists
            #if isinstance(tag, current_tags):
            if tag in current_tags:
                # find the index of such a tag
                index = current_tags.index(tag)
                # update the count and prob
                self.tag_info[ index ]["count"] += 1
                self.tag_info[ index ]["prob"] += prob
                self.tag_info[ index ]["urls"].append(image.url)
            else:
                new_tag = {"name": tag, "prob": prob, "count": 1, "urls": [image.url]}
                self.tag_info.append( new_tag )


    def getTagNames(self):
        '''
            getTagNames - get a list of the actual tags for a profile
            return: array of strings
        '''

        rt = []
        for t in self.tag_info:
            rt.append( t["name"] )
        return rt



    def count(self):
        return len(images)