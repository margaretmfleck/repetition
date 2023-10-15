# Average length of lines in a document
#     after spaces have been removed
# Margaret Fleck, 2023

import argparse
from collections import Counter
import sys


# remove whitespace
def remove_whitespace(instring):
    instring = instring.strip()
    words = instring.split()
    return "".join(words)


# process file line by line
def process_file (infile):
    ccc = 0  # avoid looking stuck when processing very large file
    totalchars = 0
    totallines = 0
    with open(infile) as infi:
        for rawline in infi:
            if rawline.strip():
                totallines += 1
                rawline = remove_whitespace(rawline)
                totalchars += len(rawline)
#            print(rawline)
        print(f" {totallines} lines, {totalchars} non-blank chars, {totalchars/totallines} average length")

def main(args):
    process_file(args.infile)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fold infile')
    parser.add_argument('infile')
#    parser.add_argument('k',type=int)
    args = parser.parse_args()
    main(args)
    
