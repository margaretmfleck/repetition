# This script finds tuples that are repeated relatively close
#    together in running text.

# Margaret Fleck, 2023

# This code is intended to process files of a reasonable length.  A
#     file might contain a sequence of contexts.  Between files, we
#     reset the context tables so that we're not constantly keeping a
#     lot of junk around indefinitely.

import argparse

# remove whitespace
def remove_whitespace(instring):
    words = instring.split()
    return "".join(words)


#  with open(outfile,"w") as outfile:


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


# Show repeated tuples, trying to assemble ones that fit together
def assemble_repeats(line,last_seen,k,linestart,window):
    repeats = []
    for pos in range(len(line)-k+1):
        mytuple = line[pos:pos+k]
        last_seen_pos = last_seen.get(mytuple,-1)
        if (last_seen_pos >= 0 and pos+linestart-last_seen_pos <= window):
            repeats.append([mytuple, pos+linestart, last_seen_pos])
#    print(f"   {repeats} \n")
    print(merge_repeats(repeats))
    print("\n")


# Display tuples in this line that have been seen recently
def collect_repeats(line,last_seen,k,linestart,window):
    for pos in range(len(line)-k+1):
        mytuple = line[pos:pos+k]
        last_seen_pos = last_seen.get(mytuple,-1)
        if (last_seen_pos >= 0 and pos+linestart-last_seen_pos <= window):
            print(f"{mytuple}/{pos+linestart}/{last_seen_pos}",end="  ")
    print("\n")


# Adds tuples from line, with last position where they were seen.
# Linestart is the first position in the line, relative to the start of the file.
def add_tuples(line,last_seen,k,linestart):
    for pos in range(len(line)-k+1):
        mytuple = line[pos:pos+k]
#        print(f"{mytuple}/{pos+linestart}",end="  ")
        last_seen[mytuple] = pos+linestart
#    print("\n")


"""
This is buggy because it won't detect repeats within the same line in the file.
"""


# process file line by line
#    tuple positions are confined to an individual file.  That is, we assume there is a very
#    large context break between different files.  
def process_file_simple (infile, k):
    tuple_position = 0  # position of first character of line w/in file
    last_seen = {}    # table of k-tuples seen in this file, with most recent position
    seen_repeated = {}    # table of k-tuples seen more than once in this file
    with open(infile) as infile:
        line = infile.readline().strip()
        while (line):
            print(f">>>{tuple_position}   {line} \n")
            line_no_blanks = remove_whitespace(line)
#            print(f">>>{tuple_position}  {line_no_blanks} \n")
#            show_repeats(line_no_blanks,last_seen,k,tuple_position,args.window)
            assemble_repeats(line_no_blanks,last_seen,k,tuple_position,args.window)
            add_tuples(line_no_blanks,last_seen,k,tuple_position)
            #reset for next line
            tuple_position+=len(line_no_blanks)
            line = infile.readline().strip()

def main(args):
    process_file_simple(args.infile, args.k)


# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='find-repeats infile outfile')
    parser.add_argument('infile')
    parser.add_argument('-k',  type=int, default=3)
    parser.add_argument('--window',  type=int, default=1000)
#    parser.add_argument('outfile')
    args = parser.parse_args()
    main(args)
    
