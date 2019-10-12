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
        # print('----BREAK----')
        # print(self.changes)


# Stock Python Implementation
def get_diff(doc_before :str, doc_after :str, view_size :int, retrieval_buffer :int):

    comparison_collector = ChChChChanges()

    idx_before=0
    idx_after=0

    # implement 'view' based sliding window.
    while (idx_before < len(doc_before) and idx_after < len(doc_after)):

        # if the same - append
        if doc_before[idx_before] == doc_after[idx_after]:
            comparison_collector.append_matching_chunk(doc_before[idx_before])
            idx_before+=1
            idx_after+=1
        else:
            # first, lets try to find out position from before -> after                
            count = 0
            found = False
            idx_after_seek = idx_after
            while(idx_after_seek < len(doc_after)):

                # get retrieval text
                retreival_before = doc_before[idx_before:idx_before+retrieval_buffer]
                retreival_after = doc_after[idx_after_seek:idx_after_seek+retrieval_buffer]

                # if you dont find it, keep scanning the after document for match
                if retreival_before != retreival_after:
                    idx_after_seek+=1
                    count+=1
                else:
                    #if you find it, save the text between idx_after - count
                    comparison_collector.append_change_text(doc_after[idx_after_seek-count: idx_after_seek])
                    idx_after = idx_after_seek #found it, so we can move this the after text along.
                    found = True
                    break

            # We cant find it! lets try to go from after->before - typical for deletions
            # crucial as it accounts for docs being different lens and addition / del happening in any order for any length doc
            # see running 4 vs 5
            if found == False:
                count = 0
                idx_before_seek = idx_before
                while(idx_before_seek < len(doc_before)):   

                    # get retrieval text
                    retreival_after = doc_after[idx_after:idx_after+retrieval_buffer]
                    retreival_before = doc_before[idx_before_seek:idx_before_seek+retrieval_buffer]

                    if retreival_after != retreival_before:
                        idx_before_seek+=1
                        count+=1
                    else:
                        #if you find it, save the text between idx_after - count
                        comparison_collector.append_change_text(doc_before[idx_before_seek-count: idx_before_seek])
                        idx_before = idx_before_seek #found it, so we can move this the after text along. 
                        break   
            
            # I cant find the word, so just add letter as a change, increment and break?
            # break

    
    # If we run out bounds, just append the remainder as a change - it cant match.
    if idx_before < len(doc_before):
        comparison_collector.append_change_text(doc_before[idx_before:len(doc_before)])
    if idx_after < len(doc_after):
        comparison_collector.append_change_text(doc_after[idx_after:len(doc_after)])

    # Show results
    comparison_collector.print_collected_data()

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

# 4.5 Deletion & Addition - longer after
doc_before_both_b = 'this is a *delete* piece of sample text'
doc_after_both_b = 'this is a piece of sample text *addddddddd*'

# 5 Addition & Deletion
doc_before_both_swap = 'this is a piece of sample text *delete*'
doc_after_both_swap = 'this is a *add* piece of sample text'

# 6 very changed mix up
doc_before_mix = 'how now brown cow I run afoul'
doc_after_mix = 'how new now add cow update run afoul'


# Run
get_diff(doc_before_both_b, doc_after_both_b, 1, 3)

# before_set = [doc_before_match, doc_before_addition, doc_before_deletion, doc_before_both, doc_before_both_swap, doc_before_mix]
# after_set = [doc_after_match, doc_after_addition, doc_after_deletion, doc_after_both, doc_after_both_swap, doc_after_mix]

# for i, var in enumerate(before_set):
#     get_diff(before_set[i], after_set[i], 1, 3)
#     print(' ')
