#==============================================================================
# This function is for parsing a citations list from an RTF file in order to 
# generate a publications list for a markdown version of my publication list. 
# 
# I generate the rtf using Zotero to make a bibliography. 
# You then need to go into the rtf using a text editor (not Word!!)
# and delete the codes at the beginning
# (i.e., {\rtf \li720 \fi-720 \sl240 \slmult1 \sa240 )
# and the closed bracket at the end. 
# Then feed this file into the code and out will come a formatted file, Parsed_refs.tex
# This isn't actually a tex file, you just need to insert it in a section
# of the CV
#==============================================================================
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:50:50 2015

@author: smudd
"""

# This is for parsing RTF files prodced by Zotero for ingestion into my tex cv
import re
import numpy as np


def read_rtf_references(filename):
    fi = open(filename, 'r')
    fo = open("Parsed_refs.md",'w')
    lines = fi.readlines()
    newlines = []
    
    print ("Lines are: ")
    print( lines)

    for line in lines:
        print ("line is: ")
        
        line = line.replace('\uc0\u8220{}', '\'')
        line = line.replace('\uc0\u8217{}', '\'')
        line = line.replace('\uc0\u8216{}', '\'')
        line = line.replace('\uc0\u8211{}', '-')
        newlines.append(line)

    #reset the lines    
    lines = newlines
    newlines = []
    
    # now replace the rtf code for italics with the latex code
    for line in lines:
        p = re.compile('\\\\i( [^}]* )\\\\i0{}', re.VERBOSE)
        line = p.sub(r'*\1*',line)
        newlines.append(line)
        #print "line is: "
        #print line

    #reset the lines    
    lines = newlines
    newlines = []
    #print "lines are now: "
    #print lines

    # Sometimes italic is like this:
    for line in lines:
        p3 = re.compile('{\\\\i{}( [^}]* )\\}', re.VERBOSE)
        line = p3.sub(r'*\1*',line)
        newlines.append(line)
        #print "line is: "
        #print line

    #reset the lines    
    lines = newlines
    newlines = []


    # replace the dois with html links to doi.org
    for line in lines:
        p2 = re.compile('doi:( [^}]* ).\\\\', re.VERBOSE)
        line = p2.sub(r'[doi:\1](http://dx.doi.org/doi:\1).',line)
        newlines.append(line)
        #print "line is: "
        #print line

    #reset the lines    
    lines = newlines
    newlines = [] 

    # make my nmae bold
    for line in lines:

        # the 1 in the replace code just means I want to replace the first instance
        line1 = line.replace('S. M. Mudd','**S. M. Mudd**',1)
        line2 = line1.replace('S.M. Mudd','**S.M. Mudd**',1)
        line3 = line2.replace('Mudd, S.M.','**Mudd, S.M.**',1)
        line4 = line3.replace('Mudd, S. M.','**Mudd, S. M.**',1)
        newlines.append(line4)
        #print "line is: "
        #print line

    #reset the lines    
    lines = newlines
    newlines = [] 
    
    # now get the year of the paper
    years = []    
    for line in lines:
        print ("line is: ")
        print (line)
        match = re.search('\d{4}', line).span()
        year= line[match[0]:match[1]]
        print( "date is: ")
        print (year)
        years.append(year) 
    
    # now sort the lines according to year 
    yeararray = np.asarray(years) 
    
    print( "ya length: " + str(len(years)))
    print ("lines lenght: " + str(len(lines)))
    
    # sort and get the indices    
    sorted_index = yeararray.ravel().argsort()
    #reverse this index
    
    print ("sorted index is: ")
    print( sorted_index )   
    
    reversed_arr = np.fliplr([sorted_index])[0]
    sorted_index = reversed_arr
    
    print ("reversed sorted index is: ")
    print (sorted_index)
    

    newyears = []
    # now make the new list
    for i in sorted_index:
        newlines.append(lines[i])
        newyears.append(years[i])
        

    # now add the codes for hanging indent and the numbering at the beginning of
    # each line
    fo.write('{% include toc.html %}\n \n')
    lines = newlines
    newlines = []
    last_year = 1655
    i = 0
    for line in lines:
        
        this_year = newyears[i]
        print ("this year: " + str(this_year))
        print( "last year: " + str(last_year) )       
        
        if this_year != last_year:
            yearline = '**01.** ' + str(this_year)
            fo.write(yearline)
            fo.write('\n \n \n')
        line = '  1. '+line
        newlines.append(line)
        fo.write(line)
        fo.write('\n')
        last_year = this_year
        i = i+1
        
    
    
    
    #print out the lines to screen
    #print "The newlines are: "
    #print newlines    
    
    # Somme commented out code to test re
    #p = re.compile('\\\\i( [^}]* )\\\\i0{}', re.VERBOSE)
    #a = p.sub(r'subsection{\1}','\i Yo\i0{} \i{second}')    
    #print "a: " + a
    
    fi.close()
    fo.close()

if __name__ == "__main__":
    #fit_weibull_from_file(sys.argv[1])
    filename = 'c:\\Users\\smudd\\Documents\\Latex_projects\\CV\\Refs_July_2015.rtf'
    
    read_rtf_references(filename) 
