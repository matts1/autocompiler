class Position(object):
    """
    :type line_start: int
    :type char_start: int
    :type line_finish: int
    :type char_finish: int
    """
    def __init__(self, line_start: int, char_start: int, text: str=''):
        self.line_start = self.line_finish = line_start
        self.char_start = self.char_finish = char_start
        for letter in text:
            if letter == '\n':
                self.line_finish += 1
                self.char_finish = 0
            self.char_finish += 1

    @staticmethod
    def join(start: 'Position', finish: 'Position'):
        return Position(start.line_start, start.char_start, finish.line_finish, finish.char_finish)

    def __repr__(self):
        return '%d(%d)...%d(%d)' % (self.line_start, self.char_start, self.line_finish, self.char_finish)


class Token(object):
    def __init__(self, position: Position, spelling: str, kind: str):
        self.position = position
        self.spelling = spelling
        self.kind = kind

    def __repr__(self):
        return '%s (%s)' % (self.spelling, self.kind)

DUMMY_POS = Position(-1, -1)