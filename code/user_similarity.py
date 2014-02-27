from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    def jaccard(users_in_common, total_users1, total_users2):
        '''
    The Jaccard Similarity between 2 two vectors
    |Intersection(A, B)| / |Union(A, B)|
    '''
        union = total_users1 + total_users2 - users_in_common
        return (users_in_common / (float(union))) if union else 0.0
    ###
    # TODO: write the functions needed to
    # 1) find potential matches,
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/
    ##get the biz ids and user ids from a file
    def extract_biz(self, _, record):
        '''just need x, y --> x,y'''
       # This map method simply takes in a key/value pair and returns them unchange
            # TODO: for each word in the review, yield the correct key,value
            # pair:
        if record['type'] == 'review':
            userid = record['user_id']
            bizid =  record['business_id']
            yield [ userid, bizid]

    def count_biz(self, userid, values):
        """This reduce method takes a key and the set of all corresponding values, and computes the cardinality of the set of values, C, and returns the input key with each input value; we'll use c later..."""
        '''take x, {y} and turn into x,(y,c) where c is the number of biz ids'''
        final = []
        item_count = 0
        for bizid in values:
            item_count += 1
            final.append(bizid)
        yield [userid, (final, item_count)]
    
    def items_pair (self, userid, values):
        for i in range(1, len(userid)): 
            #print(userid[i])
           #for v in values:
            #bizids = v[0]
            #count = v[1]
            #print bizids
            #print count
            #print "#######user 1"
            mylen = len(userid) +1
            for j in range(1, len(userid)):
                print j
                print j+1
                #print userid[j]
                #for v in values:
                   # bizids = v[0]
                    #count = v[1]
                    #print "#######user 2"
                    #print bizids 
                    #print count
                
        
        #yield [bizid,(userid, item_count)]
    
    
    #def next_step_sim (self, bizids, values):
        
        ##@param vlist The list of (x,count) pairs associated with each y
        ##@param output OutputCollector that collects a String representing a list of (x,count) pairs
        ###I am totally stuck on this next step. ---> I have no idea what to do...I tried a bunch of stuff but I couldn't figure out how to group 
        ## the users together. :( I will ask Shreyas for help on solving this this in the next couple of days...)
        
    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <key, value>
        reducer1: <key, [values]>
        mapper2: ...
        """
        return [  self.mr(self.extract_biz, self.count_biz), ##]
               self.mr(reducer=self. items_pair) ]
            ##self.mr(mapper=self.mapper1, reducer=self.reducer1),
            ##elf.mr(mapper=...),
        


if __name__ == '__main__':
    UserSimilarity.run()
