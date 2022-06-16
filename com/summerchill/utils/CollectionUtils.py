"""
https://www.oreilly.com/library/view/python-cookbook/0596001673/ch01s15.html
 iterate on both lists in parallel ,handle same index element
"""


def loopTwoList(lista, listb):
    # metod1: built-in function map
    for x, y in map(None, lista, listb):
        print(x, y)
    # metod2: built-in function zip
    for x, y in zip(lista, listb):
        print(x, y)
    # metod3: A list comprehension affords a very different iteration:
    for x, y in [(x, y) for x in lista for y in listb]:
        print(x, y)



if __name__ == "__main__":
    loopTwoList()
