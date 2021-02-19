def write(c):
    f = open("state.txt", "w")
    f.write(c)
    f.close()

def read():
    f = open("state.txt", "r")
    return f.read()
