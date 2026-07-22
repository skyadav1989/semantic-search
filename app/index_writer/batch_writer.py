
def chunk(items,size=100):
    for i in range(0,len(items),size):
        yield items[i:i+size]
