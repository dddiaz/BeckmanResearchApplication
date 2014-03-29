## Daniel Diaz 74393336
##
## Beckman Political Science Project
##
## Created Winter 2013
## Description: Allows for a user to upload a text file and do analytics on it

##Coding Practices:
##	Global Var: all caps (SECTIONS,SPEAKER,TITLE,DATA(listoflines))
##	FunctionName: CamelCase
##	Params: First caps/camelcase
##	in scope vars: all lowercase seperated by underscore
__author__ = 'danieldiaz'

import os
import easygui as eg

def Main():
    '''Main Function that will run the whole program
    '''
    ## init new section and speaker collection
    SECTIONS = CollectionNew()
    SPEAKERS = CollectionNew()
    DATA = []

    #create welcome window
    ###TITLE = "Beckman Research Application"
    ###eg.msgbox("Welcome to the Beckman Research Application!", TITLE)

    #create window for text file
    ###msg = 'What is the name of the Text file \n' + 'Make sure it is contained within the documents folder and has been converted from PDF to text.'
    ###documentName = eg.enterbox(msg='What is the name of the Text file', title=' ', default='testShort', strip=True, image=None, root=None)
    documentName = 'testShort'
    #####TODO: CHANGE THIS BACK WHEN BUILDING
    #datafile = os.path.abspath('../../../'+documentName+'.txt')
    datafile = os.path.abspath('test/'+documentName+'.txt')

    DATA = ReadFile(datafile)

    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())
    choices = ShowSectionTitlesToBeSelected()
    ###choice = eg.choicebox(msg, TITLE, choices)
    print(choices)

#########################################################################
##COLLECTION##
#########################################################################
##### COLLECTION #####
# A collection is a list of Sections/ or for speaker tuples

def CollectionNew():
    ''' Return a new, empty collection
    '''
    return [ ]

def CollectionAdd(Collection, CollectionToAdd):
    """ Return list of Sections with input Section added at end.
    """
    Collection.append(CollectionToAdd)
    return Collection

def CollectionToStr(Collection):
    ''' Return a string representing the collection
    '''
    result = ""
    for x in Collection:
        result = result + SectionStr(x)
    return result

def CollectionToStrHeaders(Collection):
    '''returns just the Headers
    '''
    result = ""
    for x in Collection:
        result = result + SectionStrHeaders(x)
    return result

#########################################################################
##SECTION##
#########################################################################
##### Section #####
## A section consists of its title and its associated text.

from collections import namedtuple

Section = namedtuple('Section', 'title text')

def SectionStr(Section):
    '''Return the section to string'''
    return ("Section Title:" + Section.title + "\n" + "Section Text: " + Section.text + "\n\n")

def SectionStrHeaders(Section):
    '''Return the section title to string'''
    return ("Section Title:" + Section.title + "\n")

def IsLineUppercase(line):
    '''finds out if we are dealing with section title'''
    line.strip('/n')
    return(line.istitle())

def GetSectionText(IndexStart,IndexEnd):
    '''gets text using section header indexes'''
    global DATA
    x = DATA[IndexStart:IndexEnd]
    '''FIX: YOU REMOVED A NEWLINE CHAR WIEN U JOINED< SEE IF THE MESSED ANYTHING UP'''
    result = ('').join(x)
    return result

def GetSectionTitle(Index):
    '''gets text using section header indexes'''
    global DATA
    return DATA[Index]

def GetSectionTitleIndicies():
    '''will take in the list of lines from readlines
    and return it parsed up into Sections'''
    '''TODO:do check if index is from header to EOF'''
    global DATA
    print("This function has", DATA)
    indiciesofheaders = []
    iterator = 0
    for line in DATA:
        if IsLineUppercase(line) and line != '\n':
            indiciesofheaders.append(iterator)
        iterator += 1
    ##need to add a dummy EOF marker so i dont get out of bounds exception
    indiciesofheaders.append(len(DATA))
    return indiciesofheaders

def AddSectionToCollection(IndiciesOfHeaders):
    '''this will add the sections to the collection using the indicies of headers
    '''
    global DATA
    global SECTIONS
    i = 0
    lenofdata = len(DATA)
    for index in IndiciesOfHeaders:
    ## this will extract the text from the line number of the header to the line
    ## number of the next header
        if index != lenofdata:
            tempSection = Section(GetSectionTitle(index),GetSectionText(index+1,IndiciesOfHeaders[i+1]))
            SECTIONS = CollectionAdd(SECTIONS,tempSection)
        i += 1
    return SECTIONS

#########################################################################
##SPEAKER##
#########################################################################

Speaker = namedtuple('Speaker', 'name text')

#########################################################################
##FILEIO##
#########################################################################
def GetFileName():
    '''get file name from user'''
    print('Please make sure the file you want to upload is text only (a txt file)')
    filename = input('What is the input file name?')
    return filename

def ReadFile(Filename):
    ''' Read file, returns list! of lines'''
    #possibly do errors replace on this line???
    infile = open(Filename, 'r', encoding='utf-8', errors='ignore')
    data = infile.readlines()
    infile.close()
    return data

#########################################################################
##Display##
#########################################################################

def ShowSectionTitlesToBeSelected():
    '''will be used when displaying info for
    user to choose section title to analyze
    '''
    global SECTIONS
    #print(Sections)
    headers = CollectionToStrHeaders(SECTIONS)
    headers_split = headers.split('\n')
    headers_clean = []
    #headers_clean.append('Whole Document')
    for title in headers_split:
        if title != '':
            headers_clean.append(title)
    return headers_clean


#RUN PROGRAM
Main()