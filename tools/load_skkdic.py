import skk

dic = skk.load_dic()
if dic != None:
    while True:
        s = input("よみ=")
        try:
            print(dic[s])
        except KeyError as e:
            pass
else:
    print("Fine not found")
