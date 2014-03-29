## Daniel Diaz 74393336
##
## Beckman Political Science Project
##
## Created Winter 2013
## Description: Allows for a user to upload a text file and do analytics on it

__author__ = 'danieldiaz'

import os
import easygui as eg
import re


def run():
    '''Main Function that will run the whole program
    '''
    ## init new section and speaker collection
    global SECTIONS
    global SPEAKERS
    global DATA
    #create welcome window
    ###TITLE = "Beckman Research Application"
    ###eg.msgbox("Welcome to the Beckman Research Application!", TITLE)

    #create window for text file
    ###msg = 'What is the name of the Text file \n' + 'Make sure it is contained within the documents folder and has been converted from PDF to text.'
    ###documentName = eg.enterbox(msg='What is the name of the Text file', title=' ', default='testShort', strip=True, image=None, root=None)
    documentName = 'TestHRAdobeExport'

    #####TODO: CHANGE THIS BACK WHEN BUILDING
    #datafile = os.path.abspath('../../../'+documentName+'.txt')
    datafile = os.path.abspath('test/' + documentName + '.txt')

    DATA = ReadFile(datafile)

    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())
    choices = ShowSectionTitlesToBeSelected()
    ###choice = eg.choicebox(msg, TITLE, choices)
    #print(choices)
    print(CollectionToPyDisplayString(choices))
    choice = 'Section Title:FOR SCHOOL CONSTRUCTION'

    ####SectionSelectedGUI(choice,SECTIONS,SPEAKERS)
    print(SectionSelectedGUI(choice))


#########################################################################
##COLLECTION##
#########################################################################
##### COLLECTION #####
# A collection is a list of Sections/ or for speaker tuples

def CollectionNew():
    ''' Return a new, empty collection
    '''
    return []


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


def CollectionToPyDisplayString(Collection):
    '''returns the collection with each elem with a newline'''
    result = ''
    for x in Collection:
        result = result + x + '\n'
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
    line.strip('')
    #special case for page numbers, they need to be ignored
    if line.startswith('---'):
        return False
    #if entire line is numbers dont include it
    if line.isdigit():
        return False
    for x in line:
        if x.isalnum():
            if x.islower():
                return False
    return True


def GetSectionText(IndexStart, IndexEnd):
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
    #print("This function has", DATA)
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
            tempSection = Section(GetSectionTitle(index), GetSectionText(index + 1, IndiciesOfHeaders[i + 1]))
            SECTIONS = CollectionAdd(SECTIONS, tempSection)
        i += 1
    return SECTIONS


def ConvertSectionToListOfLines(SectionChoice):
    global SECTIONS
    choice = SectionChoice[14:]
    #print('Choice: ' ,choice)
    for section in SECTIONS:
        if choice in section.title:
            text = section.text.split('\n')
            return section, text


def SectionFunctionality(Choice, Section, Speakers, RegexSpeakerList):
    spi = speaker_indicies_from_section(Section, RegexSpeakerList)
    #Speakers = Add_speaker_to_collection(spi,Section,Speakers)
    Speakers = Add_speaker_to_collection_with_regex(Section, Speakers)
    #print('Testing speaker collection')
    #print (Speakers)
    #print(RegexSpeakerList)
    #print(Section)
    #print(spi)
    #print(Speakers)
    if Choice == 'Look for speaker Keywords':
        #LookForSpeakerKeywords()
        keys = ['black', 'race', 'poor', 'african american']
        text = Search_speakers_for_keywords(Speakers, keys)
    elif Choice == 'Look for manually entered Keyword':
        print('text box should appear')
        askingforkey = eg.enterbox(msg='What keyword(s) are you looking for?', title=' ', default='', strip=True,
                                   image=None, root=None)
        keys = []
        keys.append(askingforkey)
        text = Search_speakers_for_keywords(Speakers, keys)
    elif Choice == 'Speaker Word Count':
        #text = Get_speaker_word_count(Speakers)
        text = Get_speaker_word_count_with_regex(Section)
        #elif Choice == 'Add Speaker Manually':
        #askingforspeaker = eg.enterbox(msg='What is the speakers name?(MUST BE IN ALL CAPS)', title='Speaker', default='SMITH', strip=True, image=None, root=None)
        #RegexSpeakerList.append(askingforspeaker)
    elif Choice == 'Show Found Speakers In Document':
        #text = ShowSpeakersToUser(RegexSpeakerList)
        text = str(RegexSpeakerList)
    elif Choice == 'Exit':
        sys.exit(0)
    else:
        text = "Exiting Program!"
        #break
    return text


#########################################################################
##SPEAKER##
#########################################################################

Speaker = namedtuple('Speaker', 'name text')

##for seraching for speakers
def FindAllSpeakersWithRegex(Data):
    #returns a list of names
    #  which will be transformed into a set to get distinct then back into list
    names = []
    for line in Data:
        #also cover dr case
        findmr = re.findall(r'Mr\.\s\b[A-Z]+[A-Z]+\b', line)
        findmrs = re.findall(r'Mrs\.\s\b[A-Z]+[A-Z]+\b', line)
        finddr = re.findall(r'Dr\.\s\b[A-Z]+[A-Z]+\b', line)
        #print(findmr,findmrs)
        names = names + findmr + findmrs + finddr
        #names = re.findall(r'Mr|Mrs|Dr|Mri\.\s\b[A-Z]+[A-Z]+\b',line)
    set1 = set(names)
    namesList = list(set1)
    return namesList


def ListOfSpeakersFromFindAllSpeakersWithRegex(RegexSpeakerList):
    NewList = []
    for x in RegexSpeakerList:
        #x = x.strip(' ')
        if 'Mrs.' in x:
            x = x.strip('Mrs.')
        elif 'Mr.' in x:
            x = x.strip('Mr.')
        elif 'Dr.' in x:
            x = x.strip('Dr.')
        x = x.strip()
        NewList.append(x)
    return NewList


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
    #TODO:possibly do errors replace on this line???
    infile = open(Filename, 'r', encoding='utf-16', errors='ignore')
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


def ShowSpeakersToUser(RegexSpeakerList):
    title = "Beckman Research Application"
    msg = 'Found Speakers: ' + '.\n' + str(RegexSpeakerList) + '.\n' + 'Continue to do Analysis'
    eg.msgbox(msg, title)


#step 3
def DisplaySectionAnalysisOptions():
    #choice is the section u want to analyze
    #section choice is what u want to do to that section
    #tempSection
    title = "Beckman Research Application"
    msg = 'Choose an option'
    SectionChoices = ['Look for manually entered Keyword', 'Look for speaker Keywords', 'Speaker Word Count',
                      'Show Found Speakers In Document', 'Exit']
    SelectedChoice = eg.choicebox(msg, title, SectionChoices)
    return SelectedChoice


#########################################################################
##GUI##
#########################################################################

def SectionSelectedGUI(SectionChoice):
    #once section selected, get speakers
    section, sectionText = ConvertSectionToListOfLines(SectionChoice)
    RegexSpeakerList = ListOfSpeakersFromFindAllSpeakersWithRegex(FindAllSpeakersWithRegex(sectionText))
    #TODO: add back in for prod
    #ShowSpeakersToUser(RegexSpeakerList)
    AnalysisOption = ""
    while AnalysisOption != "Exit":
        AnalysisOption = DisplaySectionAnalysisOptions()
        DisplayText = SectionFunctionality(AnalysisOption, Section, CollectionOfSpeakers, RegexSpeakerList)
        title = "Beckman Research Application"
        ##eg.msgbox(DisplayText,title)
    return RegexSpeakerList


#RUN PROGRAM
SECTIONS = CollectionNew()
SPEAKERS = CollectionNew()
DATA = []
run()