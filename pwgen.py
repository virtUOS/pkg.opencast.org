# -*- coding: utf-8 -*-
'''
Database specification for the Opencast package repository user interface.
:license: FreeBSD, see license file for more details.
'''

import sys
from passlib.hash import pbkdf2_sha512


def main(password):
    print(password)
    passwordhash = pbkdf2_sha512.hash(password)
    print(passwordhash)
    assert pbkdf2_sha512.verify(password, passwordhash)

if __name__ == '__main__':
    main(sys.argv[1])
