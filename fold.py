# Reads lines of text from a file and concatenates to try to
#   make line lengths at least k characters (including spaces).
# Output to stdout

# Margaret Fleck, 2023

import argparse
from collections import Counter
import sys



# process file line by line
def process_file (infile, k):
    ccc = 0  # avoid looking stuck when processing very large file
    out_line = ""
    with open(infile) as infi:
        for rawline in infi:
            rawline = rawline.rstrip()
            ccc += 1
            if (ccc%10000 == 0): print(".", file=sys.stderr,end='',flush=True)
            if rawline.strip():
                out_line += " " + rawline
                if (len(out_line) >= k):
                    print(out_line)
                    out_line = ""
        print(out_line)
        

def main(args):
    process_file(args.infile, args.k)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fold infile k')
    parser.add_argument('infile')
    parser.add_argument('k',type=int)
    args = parser.parse_args()
    main(args)
    
