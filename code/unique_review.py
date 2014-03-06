from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

WORD_RE = re.compile(r"[\w']+")


class UniqueReview(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_words(self, _, record):
        """Take in a record, yield <word, review_id>"""
            # TODO: for each word in the review, yield the correct key,value
            # pair:
        if record['type'] == 'review':
            review_id = record['review_id']
            for word in WORD_RE.findall(record['text']):
                yield [word.lower() , review_id ]

    def count_reviews(self, word, review_ids):
        """Count the number of reviews a word has appeared in.  If it is a
        unique word (ie it has only been used in 1 review), output that review
        and 1 (the number of words that were unique)."""

        unique_reviews = set(review_ids)  # set() uniques an iterator
        # TODO: yield the correct pair when the desired condition is met:
        ##want set count to be 1; means the word only appeared once
        if len(unique_reviews) == 1:
            myreviews = list(unique_reviews) 
            yield [ myreviews[0], 1 ]

    def count_unique_words(self, review_id, unique_word_counts):
        """Output the number of unique words for a given review_id"""
        yield [review_id, sum(unique_word_counts)]
        ###
        # TODO: summarize unique_word_counts and output the result
        #
        ##/
    

    def aggregate_max(self, review_id, unique_word_count):
        """Group reviews/counts together by the MAX statistic."""
        ###
        # TODO: By yielding using the same keyword, all records will appear in
        # the same reducer:
        yield ["MAX",[unique_word_count, review_id] ]
        ##/

    def select_max(self, stat, count_review_ids):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
       # yield max(count_review_ids)
        ###
        # TODO: find the review with the highest count, yield the review_id and
        # the count. HINT: the max() function will compare pairs by the first
        # number
        yield[stat, max(count_review_ids)]
        #/

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
            Step 1: extract_words
                Mapper Input: <line number, text>
                Mapper Output: <word, review_id>
                Reducer Input: <word, [review_ids]>
                Reducer Output: <review_id, 1> since the word is unique
            Step 2:
                count_reviews:
                Mapper Input: <review_id, 1>
                Mapper Output: <review_id, 1>
                count_unique_words:
                Reducer Input: <review_id, [1, 1, ...]>
                Reducer Output: <review_id, sum>
            Step 3: 
                aggregate_max:
                Mapper Input: <review_id, sum>
                Mapper Output: <"MAX", [sum, review_id]>
                select_max:
                Reducer Input: <"MAX", [[sum, review_id],...]>
                Reducer Output: <review_id, sum> of the max(sum)
        """
        return [
            self.mr(self.extract_words, self.count_reviews),
            self.mr(reducer=self.count_unique_words),
            self.mr(self.aggregate_max, self.select_max),
        ]


if __name__ == '__main__':
    UniqueReview.run()
