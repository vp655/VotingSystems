mega_list = []
def gen_recurse(listing, num_cand, a_done, b_done):
    if(a_done == 0 and b_done == 0):
        mega_list.append(listing)
    if(a_done != 0):
        list1 = listing[:]
        list2 = listing[:]
        list3 = listing[:]
        list1.append(['C','A','B'])
        list2.append(['A','C','B'])
        list3.append(['A','B','C'])
        a_done -= 1
        gen_recurse(list1, num_cand, a_done, b_done)
        gen_recurse(list2, num_cand, a_done, b_done)
        gen_recurse(list3, num_cand, a_done, b_done)
    elif(a_done ==0 and b_done != 0):
        list1 = listing[:]
        list2 = listing[:]
        list3 = listing[:]
        list1.append(['C','B','A'])
        list2.append(['B','C','A'])
        list3.append(['B','A','C'])
        b_done -= 1
        gen_recurse(list1,num_cand, a_done, b_done)
        gen_recurse(list2, num_cand, a_done, b_done)
        gen_recurse(list3, num_cand, a_done, b_done)

gen_recurse([],0,10,2)
print(len(mega_list))

# if we do every single case, then the number of possible preferences scales by 3 to the power of num_voters
# we can try the new algorithm given in the text
