import os
import sys
import csv

import re

from error_reporter import ErrorReporter
from tokeniser.token import Position, Token

directory = sys.argv[1]
token_file = open(os.path.join(directory, 'tokens.csv'), 'r')

reporter = ErrorReporter('Compiling your tokeniser')
token_types = []

for line in csv.DictReader(token_file):
    ident = line['Identifier']
    pattern = line['Pattern']
    regex = line['Regex'].lower()
    ignore = line['Ignore'].lower()
    # TODO: disallow duplicate idents

    if ident == 'EOF': reporter.report('EOF is a reserved identifier')

    if regex in 'yn':
        regex = regex == 'y'
    else: reporter.report('Regex must be y/n')

    if ignore in 'yn':
        ignore = ignore == 'y'
    else: reporter.report('Ignore must be y/n')

    if not pattern: reporter.report('Token %s cannot be empty' % ident)

    if regex:
        try:
            pattern = re.compile(pattern, re.MULTILINE)
            if pattern.match(''): reporter.report('Token %s cannot be nullable' % ident)
        except Exception:
            reporter.report('Ident %s has an invalid regex' % ident)

    token_types.append((ident, pattern, regex, ignore))

reporter.stop_on_err()
reporter = ErrorReporter('Tokenising your input file')

input_file = open(sys.argv[2], 'r').read()
last_pos = Position(1, 1, '')
tokens = []

while input_file:
    longest_match = ''
    ignore_match = False
    kind = None

    for ident, pattern, regex, ignore in token_types:
        match = ''
        if not regex and input_file.startswith(pattern):
            match = pattern
        if regex and re.match(pattern, input_file) is not None:
            match = re.match(pattern, input_file).group(0)
        if len(match) > len(longest_match):
            longest_match = match
            kind = ident
            ignore_match = ignore

    last_pos = Position(last_pos.line_finish, last_pos.char_finish, longest_match)
    if longest_match == '':
        reporter.report('Invalid token at %s (%s)' % (last_pos, input_file[:10]), fatal=True)
    if not ignore_match: tokens.append(Token(last_pos, longest_match, kind))
    input_file = input_file[len(longest_match):]

last_pos = Position(last_pos.line_finish, last_pos.char_finish, '')
tokens.append(Token(last_pos, '', 'EOF'))
print(tokens)
reporter.stop_on_err()