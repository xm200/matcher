def foo(data):
    if len(data) == 13:
        data += '1337'
    elif len(data) < 13:
        buf = data[:]
        data = 132
    else:
        data = "third path"
