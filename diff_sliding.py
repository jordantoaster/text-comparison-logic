# Data Structure for Changes
class ChChChChanges():

    def __init__(self):     
        self.matching_text = ""
        self.changed_text = ""

    def append_matching_chunk(self, text_chunk :str):
        self.matching_text += text_chunk

    def append_change_text(self, text_chunk :str):
        self.changed_text += text_chunk

    def print_collected_data(self):
        print(self.matching_text)
        print('----BREAK----')
        print(self.changed_text)


# Stock Python Implementation
'''
The retreival works by essentially, when a mismatch occurs - try to find yourself in B- if so, save chars prior to your match index and your start position
else try to find the opposing change but in A, if you do, save the n characters before your match
If you cant find it either way, force move onto the next character and save the char
'''
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
            found = False
            count = 0
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
                    text = ' ' + doc_after[idx_after_seek-count: idx_after_seek]
                    comparison_collector.append_change_text(text)
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
                        text = ' ' + doc_before[idx_before_seek-count: idx_before_seek]
                        comparison_collector.append_change_text(text)
                        idx_before = idx_before_seek #found it, so we can move this the after text along. 
                        found = True
                        break   
            
            # If I cant find a reference word in either search direction.
            if found == False:

                single_character_exceptions = ['A', 'I']
                
                # check if the word is a single char like A or I
                if doc_before[idx_before] in single_character_exceptions:
                    text = ' ' + doc_before[idx_before]
                else:
                    text = doc_before[idx_before]

                comparison_collector.append_change_text(text)
                idx_before+=1 # move on

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
doc_before_mix = 'how now brown cow A run afoul'
doc_after_mix = 'how added now add cow update run afoul'

# 7 Lorem ipsum
doc_before_l = 'Lorem DELETION ipsum dolor sit amet consectetur adipiscing elit, pharetra penatibus dictumst iaculis taciti DELETION imperdiet, auctor tempor maecenas fermentum tellus rutrum. Sociis ullamcorper dui mollis hac condimentum aliquam quam suscipit ante, blandit eros vehicula diam molestie pretium primis DELETION erat purus, cum nulla tristique nec ultricies euismod pellentesque elementum. Sem ac natoque volutpat felis interdum consequat parturient eget ridiculus, gravida nam inceptos accumsan magna feugiat per lacinia, curae sociosqu nunc mi placerat vitae aptent nascetur. Phasellus faucibus mauris netus lacus litora proin a, praesent sapien potenti sagittis vel dis, magnis facilisis tempus semper pulvinar cursus. Scelerisque cras et commodo justo venenatis conubia aliquet aenean, DELETION ligula mattis ultrices augue fusce posuere torquent quis, suspendisse massa est sodales risus integer mus. Convallis senectus luctus morbi varius fames non himenaeos habitant at laoreet arcu, curabitur vivamus odio congue ut quisque dapibus rhoncus donec montes viverra, ad orci in malesuada nullam tincidunt hendrerit eu tortor urna. Class velit cubilia sollicitudin facilisi id dictum nibh enim metus, porttitor sed leo habitasse neque duis ornare vestibulum, vulputate dignissim libero fringilla nostra platea bibendum eleifend. Egestas etiam nisl turpis nisi lobortis porta, lectus volutpat morbi phasellus ornare varius faucibus, dictum lectus donec magnis bibendum. Facilisis pulvinar nulla euismod integer nisl interdum orci luctus etiam, natoque aliquet erat sem inceptos enim vitae turpis cum accumsan, sollicitudin fermentum curae quam senectus tristique netus suspendisse. Eros taciti semper dictumst arcu purus vel potenti nunc proin sagittis, cras felis himenaeos montes a blandit ridiculus nascetur. Nisi feugiat sociis sed in dis lacus tempor duis risus massa ullamcorper, ad est iaculis odio at non pretium sodales neque. Mi rutrum libero fusce viverra commodo parturient gravida vulputate sapien, mollis lacinia ultricies justo rhoncus porttitor nibh auctor, eget class conubia porta litora hac aptent torquent. Leo vehicula scelerisque dapibus facilisi tortor sociosqu, quisque mauris maecenas posuere.'
doc_after_l = 'Lorem ipsum dolor sit amet consectetur adipiscing elit, pharetra penatibus dictumst iaculis taciti imperdiet, auctor tempor maecenas fermentum tellus rutrum. Sociis ullamcorper dui mollis hac condimentum aliquam quam suscipit ante, blandit eros vehicula diam molestie pretium primis erat purus, cum nulla tristique nec ultricies euismod pellentesque elementum. Sem ac natoque volutpat felis interdum consequat parturient eget ridiculus, gravida nam inceptos accumsan magna ADDITION feugiat per lacinia, curae sociosqu nunc mi placerat vitae aptent nascetur. Phasellus faucibus mauris netus lacus litora proin a, praesent sapien potenti sagittis vel dis, magnis facilisis tempus semper pulvinar cursus. Scelerisque cras et commodo justo venenatis conubia aliquet aenean, ligula mattis ultrices ADDITION augue fusce posuere torquent quis, suspendisse massa est sodales risus integer mus. Convallis senectus luctus morbi varius fames non himenaeos habitant at laoreet arcu, curabitur vivamus odio congue ut quisque dapibus rhoncus donec montes viverra, ad orci in malesuada nullam tincidunt hendrerit eu tortor urna. Class velit cubilia sollicitudin facilisi id dictum nibh enim metus, porttitor sed leo habitasse neque duis ornare vestibulum, vulputate dignissim libero fringilla nostra platea bibendum eleifend. Egestas etiam nisl turpis nisi lobortis porta, lectus volutpat morbi phasellus ornare varius faucibus, dictum lectus donec magnis bibendum. Facilisis pulvinar nulla euismod integer nisl interdum orci luctus etiam, natoque aliquet erat sem inceptos enim vitae turpis cum accumsan, sollicitudin fermentum curae quam senectus tristique netus suspendisse. Eros taciti semper dictumst arcu purus vel potenti nunc proin sagittis, cras felis himenaeos montes a blandit ridiculus nascetur. Nisi feugiat sociis sed in dis lacus tempor duis risus massa ullamcorper, ad est iaculis odio at non pretium sodales neque. Mi rutrum libero fusce viverra commodo parturient gravida vulputate sapien, mollis lacinia ultricies justo rhoncus porttitor nibh auctor, eget class conubia porta litora hac aptent torquent. Leo vehicula scelerisque dapibus facilisi tortor sociosqu, quisque mauris maecenas posuere.'

# Run
before_set = [doc_before_match, doc_before_addition, doc_before_deletion, doc_before_both, doc_before_both_swap, doc_before_mix, doc_before_l]
after_set = [doc_after_match, doc_after_addition, doc_after_deletion, doc_after_both, doc_after_both_swap, doc_after_mix, doc_after_l]

for i, var in enumerate(before_set):
    get_diff(before_set[i], after_set[i], 1, 3)
    print(' ')
