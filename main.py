def answer(*a):
    if type(a[0][0]) != int:
        return "ERROR"
    if a[0][0] % 2 == 0:
        return "HI"
    else:
        return "BYE"