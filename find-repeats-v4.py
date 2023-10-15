# This script finds tuples that are repeated relatively close
#    together in running text.

# Margaret Fleck, 2023

# This code is intended to process files of a reasonable length.  A
#     file might contain a sequence of contexts.  Between files, we
#     reset the context tables so that we're not constantly keeping a
#     lot of junk around indefinitely.

import argparse
from collections import Counter
import sys

# remove whitespace
def remove_whitespace(instring):
    words = instring.split()
    return "".join(words)



# merge adjacent repeat items when one continues the previous
# each item in the list is (string, start pos, distance back to last sighting)
def merge_repeats(raw_repeats):
    if len(raw_repeats) < 2:
        return raw_repeats
    output = []
    new = raw_repeats[0]
    tempstring = new[0]
    pos = new[1]  # glued to the first position in this merged string
    dist = new[2]
    movingpos = pos  # moves along string as we shift forwards 
    for next in raw_repeats[1:]:
#        if (next[1] == movingpos+1 and next[2] == dist):
        if (next[1] == movingpos+1):
            # this tuple continues previous one
            tempstring = tempstring+next[0][-1]   # merge the strings
            movingpos += 1
        else:
            output.append([tempstring,pos, dist])  # put merged tuple onto output
            tempstring = next[0]
            pos = next[1]
            dist = next[2]
            movingpos = pos  
    output.append([tempstring,pos, dist])  # put final merged tuple onto output
    return output


# remove ones that are too far back (further back than window distance) and add the new one
# most recent items are at the front
def adjust_last_seen_pos(last_seen_poslist,new_pos,window):
    rv = []
    # input is in reverse numerical order
    for pos in last_seen_poslist:
        if (new_pos - pos <= window):
            rv.append(pos)
    rv.append(new_pos)
    # convert rv from numerical order to reverse numerical order
    rv.reverse()
#    print(f">>>>{last_seen_poslist} --> {rv}")
    return rv

# Add tuples and collect both tuples and repeats
#    linestart is the first position in the line, relative to the start of the file.
#    last_seen is table of tuples with last position in the first
#    seen_repeated is a count of how many times tuple has been seen repeated
# Returns a list of tuples seen repeated in this line
#    form:  (tuple, start position, distance back to previous start position)
def find_repeats(line,last_seen,seen_repeated,k,linestart,window,required_num):
    repeats = []
    for pos in range(len(line)-k+1):
        mytuple = line[pos:pos+k]
        # Has this tuple been seen recently?
        last_seen_poslist = last_seen.get(mytuple,[])
        new_last_seen_poslist = adjust_last_seen_pos(last_seen_poslist,pos+linestart, window)
        if (new_last_seen_poslist[0] != pos+linestart):
            print("ouch")
        if (len(new_last_seen_poslist) >= required_num):
            repeats.append([mytuple, pos+linestart, pos+linestart-new_last_seen_poslist[1]])
            seen_repeated[mytuple] += 1
        # Add this tuple to the table of most recent positions
        last_seen[mytuple] = new_last_seen_poslist
    return repeats
    

# process file line by line
#    tuple positions are confined to an individual file.  That is, we assume there is a very
#    large context break between different files.  
# window is how far back in the input stream we will look for repeats
# numrequired is how many times we need to have seen the k-gram, including the most recent one
def process_file_simple (infile, k,window,outfile,outfile2,numrequired):
    linestart = 0  # position of first character of line w/in file
    last_seen = {}    # table of k-tuples seen in this file, with most recent position
    seen_repeated = Counter()   # count of how often each tuple has been seen repeated in this file
    merged_counts = Counter()   # how often has each merged tuple been seen
    ccc = 0  # avoid looking stuck when processing very large file
    with open(infile) as infi:
        rawline = infi.readline()
        while (rawline):
            ccc += 1
            if (ccc%10000 == 0): print(".", file=sys.stderr,end='',flush=True)
            line = rawline.strip()
            print(f">>>{linestart}   {line} \n")
            line_no_blanks = remove_whitespace(line)
            print(f">>>{linestart}  {line_no_blanks} \n")
#            show_repeats(line_no_blanks,last_seen,k,linestart,args.window)
            repeats = find_repeats(line_no_blanks,last_seen,seen_repeated,k,linestart,
                                   window,numrequired)
            print(repeats)
            print("\n")
            merged = merge_repeats(repeats)
            print(f" MERGED:  {merged}")
            print("\n")
            for mytuple in merged:
                merged_counts[mytuple[0]] += 1

            #reset for next line
            linestart+=len(line_no_blanks)
            rawline = infi.readline()
    print("\n", file=sys.stderr,end='',flush=True)
    print(f"\n{len(last_seen)} total {k}-grams of which {len(seen_repeated)} seen repeated\n")
    with open(outfile,"w") as outf:
        for mytuple in last_seen:
            print(f"{mytuple} {seen_repeated[mytuple]} {len(mytuple)}", file=outf)
    with open(outfile2,"w") as outf:
        for mytuple in merged_counts:
            print(f"{mytuple} {merged_counts[mytuple]} {len(mytuple)}", file=outf)
        
        

def main(args):
    process_file_simple(args.infile, args.k,args.window,args.outfile,
                        args.outfile2,args.numrequired)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find-repeats infile outfile outfile2')
    parser.add_argument('infile')
    parser.add_argument('-k',  type=int, default=3)
    parser.add_argument('--window',  type=int, default=1000)
    parser.add_argument('--numrequired',  type=int, default=2)
    parser.add_argument('outfile')
    parser.add_argument('outfile2')
    args = parser.parse_args()
    main(args)
    
