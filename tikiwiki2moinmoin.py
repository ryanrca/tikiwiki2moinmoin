#!/usr/bin/env python

import os,sys,string
import re
import argparse
from string import capwords

#  These are the simple just find and replace rules
regex_rules = { # 'seek': ' replace'
               '===': r'__',                  # Underline
               '-=': r'{{{#!wiki red/solid',  # title bar
               '=-': r'}}}',      # title bar end
               '\#': r'1. ',      # list numbers
               '\*': ' * ',        # list bullets
               '__': '\'\'\'',    # bold
               '\[': '[[',        # link entry
               '\]': ']]',        # link exit
               '--': r'--{',      # deleted
              }


def init_args():
    parser = argparse.ArgumentParser(description=
      'Pass in a tiki wiki formatted wiki page, output a moin moin formatted wiki page.')

    parser.add_argument('ifile', help='Input file' )
    parser.add_argument('ofile', help='Output file', nargs='?', default=None)
    args = parser.parse_args()
    return args



'''
First, do the simple 'find and replace' regex work
Is one string.

@return modified string
'''
def apply_simple_regex(input):
    output = input
    for seek, replace in regex_rules.items():
        p = re.compile(seek)
        output = p.sub(replace, output)

    return output


'''
Convert:
 "!text" to "= text ="
 "!!text" to "== text =="
Input is one string
'''
def handle_headers(i):
    output = i
    p = re.compile('(!+)(.+)')
    l = p.match(output)
    if l:
        head = l.group(1)
        text = l.group(2)
        output = "{0} {1} {0}\n".format('='*len(head), text)
    return output
            

'''
Convert:
 "((Some Wiki Page))" to "SomeWikiPage"
input is one string
'''
def handle_wiki_links(i):
    output = i
    p = re.compile(r"""
      ([^(]*)       # 1:  everything but '('
      [(]{2}        # Match ((
      (.*)          # 2: everything inbetween 
      [)]{2}        # Match ))
      (.*)          # 3:  all the rest
    """, re.VERBOSE)
    l = p.search(output)
    if l:
        word_list = l.group(2).split()
        if (len(word_list) > 1):
		words = l.group(2).title().split() # title() Converts Words To Upper!
		words = ''.join(words)
        else:
           words = l.group(2)
        output = "{0}{1}{2}\n".format(l.group(1), words, l.group(3))

    return output


'''
input is one string
'''
def handle_tables(i):
    pass

'''
input is one string
'''
def handle_images(i):
    pass

'''
input is one string
'''
def handle_emails(i):
    pass

'''
input is one string
'''
def handle_code(i):
    pass

'''
input is one string
'''
def handle_box(i):
    pass


if __name__ == "__main__":
    args = init_args()
    file_h = open(args.ifile, 'r')
    str = file_h.readline()
    while (str != ''):
        str = apply_simple_regex(str)
        str = handle_headers(str)
        str = handle_wiki_links(str)
        print "{0}".format(str),
        str = file_h.readline()
         

