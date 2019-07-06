with open("file2","r") as f:
    with open("file3",'w') as g:
        res = ""
        for e in f.readlines():
            new = int(e.split(" ")[0])-50
            res = str(new)+" "+" ".join(e.split(" ")[1:])
            g.write(res)
