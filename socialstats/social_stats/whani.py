
# [15,18,29,67,2,34]
# tple = ("a","b","c")
# lst.append(3)
# print(lst)
# dict_ = {"a":1, "b":2 , "c":3}
# print(dict_["b"])
# dict_["d"] = 4
# print(dict_)
# dict_[4] = "d"
# print(dict_)

# if "a" in dict_ :
#     print(dict_["a"])
# else:
#     print("No such key")
# def sort_lst(lst):
#     for i in range(0, len(lst)):
#         for j in range(i+1, len(lst)):
#             if lst[i] >=lst[j]:
#                 s = lst[i]
#                 lst[i] = lst[j]
#                 lst[j] = s
#                 print(lst)
#     # print(lst)

# # sort_lst(lst)
# lst.sort()
# print(lst[-2])
lst = [18,29,67,15,2,34,2]
def lowest_in_lst(lst):
    lowest = lst[0]
    for i in range(len(lst)):
        if lst[i]<=lowest:
            lowest=lst[i]
    print(lowest)

def largest_in_lst(lst):
    largest = lst[0]
    for i in range(len(lst)):
        if lst[i]>=largest:
            largest=lst[i]
    print(largest)

def second_lowest_in_lst(lst):
    lowest = lst[0] 
    second_lowest = lst[0]
    for i in range(len(lst)):
        if lst[i] < lowest:
            second_lowest = lowest
            lowest = lst[i]
        elif lst[i] < second_lowest and lst[i] != lowest:
            second_lowest = lst[i]
    print(second_lowest)

def second_largest_in_lst(lst):
    largest = lst[0] 
    second_largest = lst[0]
    for i in range(len(lst)):
        if lst[i] > largest:
            second_largest = largest
            largest = lst[i]
        elif lst[i] > second_largest and lst[i] != largest:
            second_largest = lst[i]
    print(second_largest)

        


client id
M0FhMElSNno1ekJxemxsVU8wZGw6MTpjaQ

client secret 

LcJqnlFjocjUDIPEcMfxEsDc39WjtfS9c6iSL3h8I2QBYaaZhU

