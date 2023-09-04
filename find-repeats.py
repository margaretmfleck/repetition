# This script finds tuples that are repeated relatively close
#    together in running text.

# Margaret Fleck, 2023

# This code is intended to process files of a reasonable length.   A file might contain a sequence
#     of contexts.  Between files, we reset the context tables so that we're not constantly
#     keeping a lot of junk around indefinitely.

import argparse

# remove whitespace
def remove_whitespace(instring):
    words = instring.split()
    return "".join(words)

# store tuples


#  with open(outfile,"w") as outfile:


# process file line by line
#    tuple positions are confined to an individual file.  That is, we assume there is a very
#    large context break between different files.  
def process_file_simple (infile):
    tuple_position = 0
    with open(infile) as infile:
        line = infile.readline().strip()
        while (line):
            print(line)
            line_no_blanks = remove_whitespace(line)
            print(f">>>{tuple_position}  {line_no_blanks}")
            tuple_position+=len(line_no_blanks)
            line = infile.readline().strip()

def main(args):
    table = {}
    process_file_simple(args.infile)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find-repeats infile outfile')
    parser.add_argument('infile')
#    parser.add_argument('outfile')
    args = parser.parse_args()
    main(args)
    
