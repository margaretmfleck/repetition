# This script reads a csv file with the faculty mentor name in the last column
#      and adds the faculty member's netID in the following column.

# The "translations" file should be a CSV file with lines of the form
#     firstname,lastname,netID
# for all faculty members.  The department office can give you a preliminary
# version.

# Sadly, names on my.cs do not necessarily agree with names supplied by the
#     CS department office.   This script extracts only the first word in
#     the first name field, because middle initials are particularly unstable.
#     However, you may still need to edit the entries for some faculty in the
#     translation table to make it match what's on my.cs.   See comments below.

import csv
import argparse


"""
def print_csv(table,outfile):
    with open(outfile, 'w') as f:
        for row in table:
            for col in range(len(row)):
                if (col != 0):
                    f.write(", ")
                # comments around each entry b/c name fields often contain commas
                f.write(f'"{row[col]}"')  
            f.write("\n")
"""


# Read in the correspondence between names and netIDs
def read_translations(transfile):
    table = {}
    with open(transfile) as csvfile:
        myreader = csv.reader(csvfile)
        for row in myreader:
            if (len(row) < 3):
                print(f"WARNING: ROW TOO SHORT {row}")
            if tuple(row[:2]) in table:
                print(f"WARNING: DUPLICATE ENTRY FOR {row[:2]}")
            table[tuple(row[:2])] = row[2]
    #for x in table:
        #print(x)
    return table    

def first_component(string):
    outstring = string.strip()
    outstring = outstring.split(" ")
    #if (len(outstring) > 1):
        #print(f"MULTI: {outstring}")
    return(outstring[0])

# Returns list of first name and last name, ignoring middle initial.
def normalize_name(stringname):
    components = stringname.split(',')
    if (len(components) != 2):
        print(f"WARNING: BAD FORMAT IN NAME {stringname}")
    lastname = components[0]
    firstname = components[1]
    lastname = first_component(lastname)
    firstname = first_component(firstname)
    return tuple([lastname,firstname])


# Row is probably a list
"""
def write_row_as_csv(row,fp):
    for col in range(len(row)):
        if (col != 0):
            fp.write(", ")
        # comments around each entry b/c name fields often contain commas
        fp.write(f'"{row[col]}"')  
    fp.write("\n")
"""


"""
     Names from advisor assignments that don't match anything from table may be due to
         * faculty member not yet in table
         * faculty member who goes by middle name
         * table uses nickname rather than full name
         * faculty member who has left the department
         * advisor who stepped in to cover someone last time.
     In most of these cases, you need to fix the faculty table.  However, in the last
     two cases, just ignore the warning.   Unmatched names will be replaced by no assignment.
"""

def convert_csv(infile, outfile,table):
    problem_names = {}
    with open(infile) as csvfile:
        with open(outfile,"w") as of:
            myreader = csv.reader(csvfile)
            mywriter = csv.writer(of)
            for row in myreader:
                faculty_member = row[-1]
                if (len(faculty_member) == 0 or faculty_member == 'nan'):
                    newrow=row+[""]
                else:
                    newrow = row[:-1]
                    normname = normalize_name(faculty_member)
                    if normname in table:
                        newrow=row
                        newrow.append(table[normname])
                        #print(table[normname])
                    else:
                        # Advisor not found in faculty table
                        problem_names[normname]=1
                        newrow.append("")
                        newrow.append("")
                mywriter.writerow(newrow)
                #write_row_as_csv(newrow,of)
                #print(newrow)
                    
                
    for item in problem_names:
        print(f"{item} is not in faculty table")

def main(args):
    table=read_translations(args.translations)
    convert_csv(args.infile, args.outfile, table)

# Top-level entry point

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='add faculty netID')
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('translations')
    args = parser.parse_args()
    main(args)
    
