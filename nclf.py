#!/usr/bin/env python

import sys
import json
import re

name_re = re.compile('^([a-zA-Z_][a-zA-Z0-9_]*)=(.*)$')

def decode_s(s):
    try:
        return json.loads(s)
    except:
        try:
            return json.loads('"%s"' % s)
        except:
            return encode_b(s)

def encode_b(s):
    return u''.join([
        unichr(ord(c) if ord(c) >= 128 else ord(c))
        for c in s
    ])

def nclf(argv):
    args_pos = []
    args_named = {}

    literal = False
    for arg in argv:
        m = name_re.match(arg)
        if literal:
            args_pos.append(encode_b(arg))
        elif arg == '=':
            literal = True
        elif m is not None:
            x = m.groups()
            name = x[0]
            value = x[1]
            args_named[name] = decode_s(value)
        else:
            value = decode_s(arg)
            args_pos.append(value)

    return [args_pos, args_named]

if __name__ == '__main__':
    args = nclf(sys.argv[1:])
    print(json.dumps(args))
