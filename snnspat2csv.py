#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:56:38 2021
Convert snns pattern files to csv 
@author: cacoch

output pattern format:
in_0,in_1,in_2, ...,in_79,in_y,out_0,out_1,out_x # first pattern
in_0,in_1,in_2, ...,in_79,in_y,out_0,out_1,out_x # second pattern

"""

import pyparsing as pp
from pyparsing import (Regex,
        Literal,
        Group,
        LineStart,
        LineEnd,
        Word,
        OneOrMore,
        restOfLine,
        alphanums,
        Combine)

import argparse
import sys
from itertools import zip_longest
import itertools


# Grammar definition
def grammar():

    #pp.ParserElement.setDefaultWhitespaceChars('')

    VERSION_HEADER  = Literal("SNNS pattern definition file").suppress()
    INT = Word(pp.nums)
    DOT = Literal(".")
    V_NUMBER         = (Word("Vv") +INT +  DOT + INT).suppress()
    EOL = LineEnd().suppress()
    COLON = Literal(":")
    GENERATED_AT     = ("generated at" + pp.SkipTo(EOL)).suppress()

    NO_OF_PATTERN = (Literal("No. of patterns") + COLON).suppress()
    NO_OF_INPUT   = (Literal("No. of input units") + COLON).suppress()
    NO_OF_OUTPUT  = (Literal("No. of output units") + COLON).suppress() 
    NUMBER = (INT |  Combine('+'+ INT ) | Combine('-' + INT)| 
            Combine(INT+ '.' + INT) | Combine('.' + INT ))

    n_patt          = (NO_OF_PATTERN + NUMBER)("no_patts")
    i_head          = (NO_OF_INPUT + NUMBER)("no_inputs")
    o_head          = (NO_OF_OUTPUT + NUMBER)("no_outputs")


    header = (VERSION_HEADER + V_NUMBER + GENERATED_AT + n_patt
              + i_head + o_head)
    pattern_list = (OneOrMore(NUMBER))('pattern')



    gramm = header + pattern_list 
    gramm.ignore(Literal('#') + pp.restOfLine)

    return gramm

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def save_csv(filename, data):
    #print(data)
    print("===")
    no_inputs = int(data['no_inputs'][0])
    no_outputs = int(data['no_outputs'][0])
    no_patts = int(data['no_patts'][0])
    patts = data['pattern']
    print(no_inputs, no_outputs, no_patts)
    #print(patts)
    chunk_size = no_inputs + no_outputs 

    chunked_list = [list(item) for item in list(zip_longest(*[iter(patts)]*chunk_size, fillvalue=''))]
    #print(chunked_list)
    result = ""

    for el in chunked_list:
        csv_line = ','.join(map(str, el))
        result += csv_line + "\n"
    print(result)
    file1 = open("myfile.txt","w")
    file1.write(result)






def parse_args(args):
    prser = argparse.ArgumentParser(description='Convert SNNS pattern file to csv')
    prser.add_argument("input", help="input pat pattern file")
    prser.add_argument("output", help="output json pattern file", nargs='?')
    return  prser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    print("\n\n###################")
    parser = grammar()

    

    result = parser.parseFile(args.input)
    #print(result.dump())
    save_csv("output.csv", result.as_dict())
    
    #parser.add_argument("y", type=int, help="the exponent")
    #parser.add_argument("-v", "--verbosity", action="count", default=0)
    #answer = args.x**args.y
    #if args.verbosity >= 2:
    #    print("Running '{}'".format(__file__))
    #if args.verbosity >= 1:
    #    print("{}^{} == ".format(args.x, args.y), end="")
    #print(answer)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
