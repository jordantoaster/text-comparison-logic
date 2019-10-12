# INPUT VARIATIONS

# 1 Matching Text
doc_a_match = 'this is a matching string, it is a simple example'
doc_b_match = 'this is a matching string, it is a simple example'

# 2 Addition Mid
doc_a_addition = 'this is a matching string -  - it is a simple example'
doc_b_addition = 'this is a matching string - new text inserted here - it is a simple example'


# Data Structure for Changes
class ChChChChanges():

    def __init__(self):     
        self.matching_text = ""
        self.changed_text = ["",""]

    def append_matching_chunk(self, text_chunk :str):
        self.matching_text += text_chunk

    def append_change_chunk(self, text_chunk_a :str, text_chunk_b :str):
        self.changed_text[0] += text_chunk_a
        self.changed_text[1] += text_chunk_b

    def print_collected_data(self):
        print(self.matching_text)
        print('BREAK')
        print(self.changed_text)


# Get shortest input Length
# TODO change to return the leftover text of the longest string as well.
def get_shortest_string_len(doc_a :str, doc_b :str):

    if len(doc_a) < len(doc_b):
        return len(doc_a), doc_b[len(doc_a) : len(doc_b)], True
    else:
        return len(doc_b), doc_a[len(doc_b) : len(doc_a)], False

# Stock Python Implementation
def get_diff(doc_a :str, doc_b :str, view_size :int, retrieval_buffer :int):

    shortest_length, remaining_text, is_a = get_shortest_string_len(doc_a, doc_b)
    comparison_collector = ChChChChanges()
    change_mode = False

    # Help traceback to original loop based on n retreival iterations
    count = 0

    # Iterate each character until shortest string is complete... 
    for idx in range(0, shortest_length, view_size):

        idx+=count
        if idx >= shortest_length: # when we dont want to use range anymore, we are done dude.
            break

        # Grab our text to compare
        text_chunk_a = doc_a[idx:idx + view_size] # Get chunk ... if idx = 0 and view = 1, get 0
        text_chunk_b = doc_b[idx:idx + view_size] # Get chunk = if idx = 2 and view = 2, get 2+3

        if change_mode == True:

            for idx_c in range(idx, shortest_length, view_size):

                text_chunk_b_sub = doc_b[idx_c:idx_c + view_size] 

                # Check for advanced match
                retreival_a = text_chunk_a + doc_a[(idx + view_size) : (idx + view_size + retrieval_buffer)]
                retreival_b = text_chunk_b_sub + doc_b[(idx_c + view_size) : (idx_c + view_size + retrieval_buffer)]

                if retreival_a == retreival_b:
                    comparison_collector.append_matching_chunk(text_chunk_a)
                    change_mode = False
                    break # lets get out of the diff loop
                else:
                    comparison_collector.append_change_chunk("", text_chunk_b_sub) # Assumes changes of any kind can be captured using just B
                    count+=1

        else:
            # Compare standard...        
            if text_chunk_a == text_chunk_b: # look for a view sized match
                comparison_collector.append_matching_chunk(text_chunk_a)
            else:
                comparison_collector.append_change_chunk(text_chunk_a, text_chunk_b)
                change_mode = True


    # Get the diff between both strings len - add remaining text as a 'change'
    if is_a:
        comparison_collector.append_change_chunk("", remaining_text)
    else:
        comparison_collector.append_change_chunk(remaining_text, "")

    # Show results
    comparison_collector.print_collected_data()


# Run
get_diff(doc_a_addition, doc_b_addition, 1, 3)