
# https://stackoverflow.com/questions/43067373/split-by-comma-and-how-to-exclude-comma-from-quotes-in-split-python/70594403

def tokenize( string, separator = ',', quote = '"' ):
    """
    Split a comma separated string into a List of strings.

    Comma's inside double quotes are ignored.

    :param string: A string to be split into chunks
    :return: A list of strings, one element for every chunk
    """
    comma_separated_list = []

    chunk = ''
    in_quotes = False

    for character in string:
        if character == separator and not in_quotes:
            comma_separated_list.append(chunk)
            chunk = ''

        else:
            chunk += character
            if character == quote:
                in_quotes = False if in_quotes else True

    comma_separated_list.append( chunk )

    return comma_separated_list

def test_1():
    string = '"aaaa","bbbb","ccc,ddd"' 

    expected = ['"aaaa"', '"bbbb"', '"ccc,ddd"']
    actual = tokenize( string )

    assert expected == actual

def test_2():

    s = 'one "hello world;" line; another statement;'

    res = tokenize( s, ';' )

    for x in res:
        print( "result: {}".format( x ) )



def test():

    test_1()
    test_2()

if __name__ == "__main__":
    test()
