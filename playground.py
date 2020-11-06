ings_pairs = [('z', 2), ('z', 1), ('p', 13)]
ings_list = [['z',2], ['z', 1], ['p', 13]]

b = {}
for pair in ings_list:
    name = str(pair[0])
    val  = int(pair[1])
    if name not in b:
        b[name]=val
    else:
        b[name]+=val

# print(d_list)
print(b)