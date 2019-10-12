# INPUT VARIATIONS

# 1 Matching Text
doc_before_match = 'this is a matching string, it is a simple example'
doc_after_match = 'this is a matching string, it is a simple example'

# 2 Addition Mid
doc_before_addition = 'this is a matching string -  - it is a simple example'
doc_after_addition = 'this is a matching string - new text inserted here - it is a simple example'

# 3 Deletion Mid
doc_before_deletion = 'this is a matching string - old text deleted here - it is a simple example'
doc_after_deletion = 'this is a matching string -  - it is a simple example'

# 4 Deletion & Addition
doc_before_both = 'this is a *delete* piece of sample text'
doc_after_both = 'this is a piece of sample text *add*'

# 5 Addition & Deletion - DOES NOT WORK FOR THIS ONE
doc_before_both = 'this is a piece of sample text *delete*'
doc_after_both = 'this is a *add* piece of sample text'

# 6 Longer B, more text, random add and deletes - Get stuck in loop
doc_before_big = 'this is a piece of sample text, this is a piece of sample text, this is a piece of sample text, this is a piece of sample text, this is a piece of sample text, this is a piece of sample text'
doc_after_big = 'this is a  of sample text, this is a piece Hello sample text, this is a piece of sample test, this is a piece of sample text, this is a piece of  text, this is a piece of sample text, this is a piece of sample text, this is a piece of sample text'

# Data Structure for Changes
class ChChChChanges():

    def __init__(self):     
        self.matching_text = ""
        self.changes = []
        self.changed_text = ""

    def append_matching_chunk(self, text_chunk :str):
        self.matching_text += text_chunk

    def append_change_chunk(self, change_information :dict):
        self.changes.append(change_information)

    def append_change_text(self, text_chunk :str):
        self.changed_text += text_chunk

    def print_collected_data(self):
        print(self.matching_text)
        print('----BREAK----')
        print(self.changed_text)
        print('----BREAK----')
        print(self.changes)


# Get shortest input Length
# TODO change to return the leftover text of the longest string as well.
def get_shortest_string_len(doc_before :str, doc_after :str):

    if len(doc_before) >= len(doc_after):
        return len(doc_before), True
    else:
        return len(doc_after), False

# Stock Python Implementation
def get_diff(doc_before :str, doc_after :str, view_size :int, retrieval_buffer :int):

    longest_length, is_before_longest = get_shortest_string_len(doc_before, doc_after)
    comparison_collector = ChChChChanges()

    idx_short = 0
    idx_long = 0
    focused_doc = ''

    if is_before_longest:
        long_doc = doc_before
        short_doc = doc_after
        focused_doc = 'before'
    else:
        long_doc = doc_after
        short_doc = doc_before 
        focused_doc = 'after'

    while(idx_short < longest_length or idx_long < longest_length):

        # idea to check and flip 'short' and 'long' based on however how the most string left?
        # Important given logic after this assumes we keep chipping into the longest
        if (len(long_doc) - idx_long) < (len(short_doc) - idx_short):

            # get temp data for switch
            switch_data = long_doc
            switch_idx = idx_long
            
            # switch the data, switch the indexes
            long_doc = short_doc
            idx_long = idx_short
            short_doc = switch_data
            idx_short = switch_idx
            
            if focused_doc == 'after':
                focused_doc = 'before'
            else:
                focused_doc = 'after'

        # Grab our text to compare
        text_chunk_short = short_doc[idx_short:idx_short + view_size] # Get chunk ... if idx = 0 and view = 1, get 0
        text_chunk_long = long_doc[idx_long:idx_long + view_size] # Get chunk = if idx = 2 and view = 2, get 2+3

        if text_chunk_short == text_chunk_long: # look for a view sized match
            comparison_collector.append_matching_chunk(text_chunk_short)
            idx_short+=view_size
            idx_long+=view_size
        else:
            found = False
            while(found == False):

                # get retrieval text
                retreival_short = text_chunk_short + short_doc[(idx_short + view_size) : (idx_short + view_size + retrieval_buffer)]
                retreival_long = text_chunk_long + long_doc[(idx_long + view_size) : (idx_long + view_size + retrieval_buffer)]

                # Are we synced?
                if retreival_short == retreival_long:
                    found = True
                    comparison_collector.append_matching_chunk(text_chunk_short)
                    idx_short+=view_size
                    idx_long+=view_size
                else:
                    comparison_collector.append_change_chunk({'text':text_chunk_long, 'source':focused_doc})
                    comparison_collector.append_change_text(text_chunk_long)
                    idx_long+=view_size
                    text_chunk_long = long_doc[idx_long:idx_long + view_size] # update our 'After' text chunk

    # Show results
    comparison_collector.print_collected_data()

# Run
get_diff(doc_before_big, doc_after_big, 1, 3)