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

# Data Structure for Changes
class ChChChChanges():

    def __init__(self):     
        self.matching_text = ""
        self.changed_text = []

    def append_matching_chunk(self, text_chunk :str):
        self.matching_text += text_chunk

    def append_change_chunk(self, text_chunk :str):
        self.changed_text.append(text_chunk)

    def print_collected_data(self):
        print(self.matching_text)
        print('----BREAK----')
        print(self.changed_text)


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

    if is_before_longest:
        long_doc = doc_before
        short_doc = doc_after
    else:
        long_doc = doc_after
        short_doc = doc_before 

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
                    comparison_collector.append_change_chunk(text_chunk_long)
                    idx_long+=view_size
                    text_chunk_long = long_doc[idx_long:idx_long + view_size] # update our 'B' text chunk

    # Show results
    comparison_collector.print_collected_data()

# Run
get_diff(doc_before_both, doc_after_both, 1, 3)