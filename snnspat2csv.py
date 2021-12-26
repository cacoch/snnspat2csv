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

import sys
import os
import argparse
from itertools import zip_longest
import pyparsing as pp
from pyparsing import (Literal,
        Opt,
        LineEnd,
        Word,
        OneOrMore,
        Combine)

#pp.enable_diag()
#pp.__diag__.enable_debug_on_named_expressions = True



def grammar():
    """Grammar definition"""

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
    SIGN          = Opt(Word("-+", exact=1))



    NUMBER = Combine(SIGN + INT + DOT + INT) | Combine('.' + INT ) | Combine(SIGN + INT )

    n_patt          = (NO_OF_PATTERN + NUMBER)("no_patts")
    i_head          = (NO_OF_INPUT + NUMBER)("no_inputs")
    o_head          = (NO_OF_OUTPUT + NUMBER)("no_outputs")


    header = (VERSION_HEADER + V_NUMBER + GENERATED_AT + n_patt
              + i_head + o_head)
    pattern_list = (OneOrMore(NUMBER))('pattern')



    gramm = header + pattern_list
    gramm.ignore(Literal('#') + pp.restOfLine)

    return gramm


def save_csv(filename, data):
    """Convert string to csv and save to file"""

    #print(data)
    print("===")
    no_inputs = int(data['no_inputs'][0])
    no_outputs = int(data['no_outputs'][0])
    no_patts = int(data['no_patts'][0])
    patts = data['pattern']
    print(no_inputs, no_outputs, no_patts)
    #print(patts)
    chunk_size = no_inputs + no_outputs

    chunked_list = [list(item) for item in list(zip_longest(
                     *[iter(patts)]*chunk_size, fillvalue=''))]
    #print(chunked_list)
    csv_str = ""

    for el in chunked_list:
        csv_line = ','.join(map(str, el))
        csv_str += csv_line + "\n"

    with open(filename,"w",encoding="utf-8") as f:
        f.write(csv_str)



def parse_args(args):
    """Parse command line arguments"""

    prser = argparse.ArgumentParser(description='Convert SNNS pattern file to csv')
    prser.add_argument("input", help="input pat pattern file")
    prser.add_argument("output", help="output json pattern file", nargs='?')
    return  prser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args.output is None:
        output_file = os.path.basename(args.input)
        output_file = output_file.split('.')[0] + '.csv'
    else:
        output_file = args.output


    print(f'Parsing {args.input} file to {output_file}')
    parser = grammar()


    #result = parser.parseFile(args.input, parse_all=True)
    with  open(args.input, 'r') as f:
    #with open(args.input, 'r', encoding="utf-8", errors="ignore") as f:
        data = f.read()
        result = parser.parse_string(data, parse_all=True)

    #print(result.dump())
    save_csv(output_file, result.as_dict())

    #parser.add_argument("y", type=int, help="the exponent")
    #parser.add_argument("-v", "--verbosity", action="count", default=0)
    #answer = args.x**args.y
    #if args.verbosity >= 2:
    #    print("Running '{}'".format(__file__))
    #if args.verbosity >= 1:
    #    print("{}^{} == ".format(args.x, args.y), end="")
    #print(answer)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
