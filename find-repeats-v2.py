# This script finds tuples that are repeated relatively close
#    together in running text.

# Margaret Fleck, 2023

# This code is intended to process files of a reasonable length.  A
#     file might contain a sequence of contexts.  Between files, we
#     reset the context tables so that we're not constantly keeping a
#     lot of junk around indefinitely.

import argparse
from collections import Counter

# remove whitespace
def remove_whitespace(instring):
    words = instring.split()
    return "".join(words)





# merge adjacent repeat items when one continues the previous
# each item in the list is (string, start pos, last seen start pos)
def merge_repeats(raw_repeats):
    if len(raw_repeats) < 2:
        return raw_repeats
    output = []
    new = raw_repeats[0]
    tempstring = new[0]
    pos1 = new[1]  # glued to the first position in this merged string
    pos2 = new[2]
    movingpos1 = pos1  # moves along string as we shift forwards 
    movingpos2 = pos2
    for next in raw_repeats[1:]:
        if (next[1] == movingpos1+1 and next[2] == movingpos2+1):
#        if (next[1] == movingpos1+1):
            # this tuple continues previous one
            tempstring = tempstring+next[0][-1]   # merge the strings
            movingpos1 += 1
            movingpos2 += 1
        else:
            output.append([tempstring,pos1, pos2])  # put merged tuple onto output
            tempstring = next[0]
            pos1 = next[1]
            pos2 = next[2]
            movingpos1 = pos1  
            movingpos2 = pos2
    output.append([tempstring,pos1, pos2])  # put final merged tuple onto output
    return output


# Add tuples and collect both tuples and repeats
#    linestart is the first position in the line, relative to the start of the file.
#    last_seen is table of tuples with last position in the first
#    seen_repeated is a count of how many times tuple has been seen repeated
# Returns a list of tuples seen repeated in this line
def find_repeats(line,last_seen,seen_repeated,k,linestart,window):
    repeats = []
    for pos in range(len(line)-k+1):
        mytuple = line[pos:pos+k]
        # Has this tuple been seen recently?
        last_seen_pos = last_seen.get(mytuple,-1)
        if (last_seen_pos >= 0 and pos+linestart-last_seen_pos <= window):
            repeats.append([mytuple, pos+linestart, last_seen_pos])
            seen_repeated[mytuple] += 1
        # Add this tuple to the table of most recent positions
        last_seen[mytuple] = pos+linestart
    return repeats
    

# process file line by line
#    tuple positions are confined to an individual file.  That is, we assume there is a very
#    large context break between different files.  
def process_file_simple (infile, k,window,outfile,outfile2):
    linestart = 0  # position of first character of line w/in file
    last_seen = {}    # table of k-tuples seen in this file, with most recent position
    seen_repeated = Counter()   # count of how often each tuple has been seen repeated in this file
    merged_counts = Counter()   # how often has each merged tuple been seen
    with open(infile) as infi:
        line = infi.readline().strip()
        while (line):
            print(f">>>{linestart}   {line} \n")
            line_no_blanks = remove_whitespace(line)
            print(f">>>{linestart}  {line_no_blanks} \n")
#            show_repeats(line_no_blanks,last_seen,k,linestart,args.window)
            repeats = find_repeats(line_no_blanks,last_seen,seen_repeated,k,linestart,window)
            print(repeats)
            print("\n")
            merged = merge_repeats(repeats)
            print(merged)
            print("\n")
            for mytuple in merged:
                merged_counts[mytuple[0]] += 1

            #reset for next line
            linestart+=len(line_no_blanks)
            line = infi.readline().strip()
    print(f"\n{len(last_seen)} total {k}-grams of which {len(seen_repeated)} seen repeated\n")
    with open(outfile,"w") as outf:
        for mytuple in last_seen:
            print(f"{mytuple} {seen_repeated[mytuple]}", file=outf)
    with open(outfile2,"w") as outf:
        for mytuple in merged_counts:
            print(f"{mytuple} {merged_counts[mytuple]}", file=outf)
        
        

def main(args):
    process_file_simple(args.infile, args.k,args.window,args.outfile,args.outfile2)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find-repeats infile outfile outfile2')
    parser.add_argument('infile')
    parser.add_argument('-k',  type=int, default=3)
    parser.add_argument('--window',  type=int, default=1000)
    parser.add_argument('outfile')
    parser.add_argument('outfile2')
    args = parser.parse_args()
    main(args)
    
