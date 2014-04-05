# netstring(x)
def netstring(x):
    """
    Encodes a Python object as a netstring.
    
    >>> netstring(456)
    '3:456,'
    >>> netstring(['abc', 'defg'])
    '3:abc,4:defg,'
    """
    if hasattr(x, '__iter__'):
        return ''.join( netstring(y) for y in x )
    else:
        x = str(x)   
        return '%d:%s,' % (len(x), x)


##  NetstringParser
##
class NetstringParser(object):

    """
    Decodes a netstring to a list of Python strings.

    >>> parser = NetstringParser()
    >>> parser.feed('3:456,')
    >>> parser.results
    ['456']
    >>> NetstringParser.parse('3:abc,4:defg,')
    ['abc', 'defg']
    """
    
    def __init__(self):
        self.results = []
        self.reset()
        return

    def reset(self):
        self._data = ''
        self._length = 0
        self._parse = self._parse_len
        return
        
    def feed(self, s):
        i = 0
        while i < len(s):
            i = self._parse(s, i)
        return
        
    def _parse_len(self, s, i):
        while i < len(s):
            c = s[i]
            if c < '0' or '9' < c:
                self._parse = self._parse_sep
                break
            self._length *= 10
            self._length += ord(c)-48
            i += 1
        return i
        
    def _parse_sep(self, s, i):
        if s[i] != ':': raise SyntaxError(i)
        self._parse = self._parse_data
        return i+1
        
    def _parse_data(self, s, i):
        n = min(self._length, len(s)-i)
        self._data += s[i:i+n]
        self._length -= n
        if self._length == 0:
            self._parse = self._parse_end
        return i+n
        
    def _parse_end(self, s, i):
        if s[i] != ',': raise SyntaxError(i)
        self.add_data(self._data)
        self.reset()
        return i+1

    def add_data(self, data):
        self.results.append(data)
        return

    @classmethod
    def parse(klass, s):
        self = klass()
        self.feed(s)
        return self.results
