def decode(code):
    value=0
    for step in range(1,41):
        value=(value+(code*step+step*step)%65521)%4093
    return value
