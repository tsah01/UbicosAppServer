import random

usernames_array = ["giraffe", "raccoon", "ant", "tiger", "sheep", "deer", "panda", "liger", "fox", "hippo", "alligator",
                   "dog", "dolphin", "eagle", "zebra", "rabbit", "bear", "monkey", "leopard", "frog", "squirrel",
                   "elephant", "bee", "duck", "kangaroo", "penguin"]


username_groupID = ['1', '1', '2', '2', '2', '3', '3', '3', '4', '4', '4', '5', '5', '5', '6', '6', '6', '7', '7',
                    '7', '8', '8', '8', '9', '9', '9']

dictionary = dict(zip(usernames_array, username_groupID))
# print(dictionary)

group1 = {}
group2 = {}
group3 = {}
group4 = {}
group5 = {}
group6 = {}

length = len(username_groupID)
#print(length)

def swapelement(group, id_rep, name_rep):
    for ID in group:
        if ID not in group6:
            group6[ID] = group[ID]
            del group[ID]
            break
    group[id_rep] = name_rep;

print("Total number of animals: "+str(len(dictionary.keys())))
random.shuffle(usernames_array)

class randomGroupGenerator():
    def creategroup(self):
        group_list = []
        length = len(username_groupID)
        while length > 0:
            name = usernames_array.pop()
            ID = dictionary[name]
            if len(list(group1.keys()))< 6 and ID not in group1.keys():
                group1[ID] = name

            elif len(list(group2.keys()))< 4 and ID not in group2.keys():
                group2[ID] = name

            elif len(list(group3.keys()))<4 and ID not in group3.keys():
                group3[ID] = name

            elif len(list(group4.keys()))<4 and ID not in group4.keys():
                group4[ID] = name

            elif len(list(group5.keys()))<4 and ID not in group5.keys():
                group5[ID] = name

            elif len(list(group6.keys())) < 4 and ID not in group6.keys():
                group6[ID] = name

            else:
                if ID not in group1.keys():
                    swapelement(group1, ID, name)
                elif ID not in group2.keys():
                    swapelement(group2, ID, name)
                elif ID not in group3.keys():
                    swapelement(group2, ID, name)
                elif ID not in group4.keys():
                    swapelement(group2, ID, name)
                elif ID not in group5.keys():
                    swapelement(group2, ID, name)
            length -= 1


        #convert dictionaries into list
        group_list.append([x for x in group1.values()])
        group_list.append([x for x in group2.values()])
        group_list.append([x for x in group3.values()])
        group_list.append([x for x in group4.values()])
        group_list.append([x for x in group5.values()])
        group_list.append([x for x in group6.values()])

        return group_list;

# creategroup()
# print(group1)
# print(group2)
# print(group3)
# print(group4)
# print(group5)
# print(group6)


