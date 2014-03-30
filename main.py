## Daniel Diaz 74393336
##
## Beckman Political Science Project
##
## Created Winter 2013 copyright Daniel Diaz All Rights Reserved
## Description: Allows for a user to upload a text file and do analytics on it

__author__ = 'danieldiaz'

import os
import easygui as eg
import re
import sys
import codecs


def run():
    """Main Function that will run the whole program
    """
    global TITLE
    global SECTIONS
    global SPEAKERS
    global DATA

    ##eg.msgbox("Welcome to the Beckman Research Application!", TITLE)

    #create window for text file
    msg = ('What is the name of the Text file \n'
           + 'Make sure it is contained within the documents folder and has been converted from PDF to text.')
    documentName = eg.enterbox(msg='What is the name of the Text file'
                               , title=' '
                               , default='TestThis'
                               , strip=True
                               , image=None
                               , root=None)
    #documentName = 'TestHRAdobeExport'

    #####TODO: CHANGE THIS BACK WHEN BUILDING
    datafile = os.path.abspath('../../../'+documentName+'.txt')
    #datafile = os.path.abspath('test/' + documentName + '.txt')
    ##TODO:THIS IS ONLY FOR TESTING!!!!
    #datafile = 'users/danieldiaz/Dev/school/Beckman/BeckmanPyCharm/dist/TestThis.txt'

    DATA = ReadFile(datafile)

    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())
    #TODO: remove from prod?
    if len(SECTIONS) < 10:
        #do section titles loop so easy gui doesnt break
        choice = ShowSectionTitlesLoop()
    else:
        choices = ShowSectionTitlesToBeSelected()
        choice = eg.choicebox(msg, TITLE, choices)
    #print(choices)
    #print(CollectionToPyDisplayString(choices))

    SectionSelectedGUI(choice)

    if eg.ccbox('EXIT?', TITLE):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)           # user chose Cancel

    msg = "Do you want to continue?"
    title = "Please Confirm"
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)           # user chose Cancel

def nonguirun():
    """Main Function that will run the whole program
    """
    global TITLE
    global SECTIONS
    global SPEAKERS
    global DATA

    datafile = os.path.abspath('test/' + 'TestThis' + '.txt')
    ##TODO:THIS IS ONLY FOR TESTING!!!!

    DATA = ReadFile(datafile)

    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())

    #print('\n\n These are all the section titles \n\n')
    #print(sectiontitlestemp)

    #TODO: hey \r should not count as a sectiontitle its an error

    print('\n\n These are all the sections \n\n')
    tempstrheaders = SectionTitlesCleaning()
    print(tempstrheaders)
    #for x in tempstrheaders:
        #print(x)

    eg.choicebox('','',tempstrheaders)
    #print(tempstrheaders[33:35])

#########################################################################
##COLLECTION##
#########################################################################
##### COLLECTION #####
# A collection is a list of Sections/ or for speaker tuples

def CollectionNew():
    """ Return a new, empty collection
    :rtype : list
    """
    return []


def CollectionAdd(Collection, CollectionToAdd):
    """ Return list of Sections with input Section added at end.
    :param Collection:
    :param CollectionToAdd:
    """
    Collection.append(CollectionToAdd)
    return Collection


def CollectionToStr(Collection):
    """ Return a string representing the collection
    :param Collection:
    """
    result = ""
    for x in Collection:
        result += SectionStr(x)
    return result


def CollectionToStrHeaders(Collection):
    """returns just the Headers
    :param Collection:
    """
    result = ""
    for x in Collection:
        result += SectionStrHeaders(x)
    return result


def CollectionToPyDisplayString(Collection):
    """returns the collection with each elem with a newline
    :param Collection:
    """
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
    """Return the section to string
    :param Section:
    """
    return "Section Title:" + Section.title + "\n" + "Section Text: " + Section.text + "\n\n"


def SectionStrHeaders(Section):
    """Return the section title to string
    :param Section:
    """
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

def SectionTitlesCleaning():
    """
    """
    global SECTIONS
    append = False
    titlearray = []
    for tempsection in SECTIONS:
        titlearray.append(tempsection.title)
    print(titlearray)
    cleantitlearray= []
    for temptitle in titlearray:
        #remove commaz
        string = temptitle
        #print (string)
        for ch in [',','.','-','\r','\n','&','_','(',')','\t','\t11173','\t11235','\\']:
            string = string.replace(ch,'')
        #print(string)
        validletters = 'abcdefghijklmnopqrstuvwxyz '
        newstring = ''
        for letter in string.lower():
            if letter in validletters:
                newstring += letter
                #print (newstring)
        #this new string should be lower
        #print(newstring)
        #if newstring != '' and newstring != '\n' \
        #and newstring != '\r' and not newstring.isdigit():
        if newstring != '':
            cleantitlearray.append(newstring.upper())
            #print(temptitleintemp)
    return cleantitlearray


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

def Add_speaker_to_collection_with_regex (Section,S):
    sText = Section.text
    OrderedList = re.findall(r'Mr\.\s\b[A-Z]+[A-Z]+\b',sText)
    TextSplit = re.split(r'Mr\.\s\b[A-Z]+[A-Z]+\b',sText)
    SpeakerDict = {}
    for speaker in OrderedList:
        x = str(speaker)
        SpeakerDict[x]=""
    #print("listoftextlen:", listoftextlen)
    #start at 1 instead of 0 bc we dont need to include text split from title
    i = 1
    #print("starting dict add")
    for spkr in OrderedList:
        #print("the speaker is: ", spkr)
        if spkr in SpeakerDict:
            oldText = SpeakerDict.get(spkr,"\n")
            SpeakerDict[spkr]= oldText + TextSplit[i]
            i = i + 1
    for key,value in SpeakerDict.items():
        tempSpeakerTuple = Speaker(key,value)
        TempCollection = CollectionAdd(S,tempSpeakerTuple)
    return TempCollection

def speaker_indicies_from_section(Section,ListOfSpeakers):
    '''Takes in section, and list of speakers, and assigns spoken text to speaker tuple.'''
    sText = Section.text
    sText = sText.split('\n')
    speaker_indicies = []
    for x in ListOfSpeakers:
        for line in sText:
            ##ifnore the period after mr. mrs. and skip to period after name ex MR. MADDEN
            #get the first 20 chars to look for name
            #TODO: IMPROVE THIS
            AdjustedLine = line[0:20]
            if x in AdjustedLine:
                #call read text function
                indexOfSpeaker = sText.index(line)
                speaker_indicies.append(indexOfSpeaker)
    ##need to add a dummy EOF marker so i dont get out of bounds exception
    speaker_indicies.append(len(sText))
    #print speaker_indicies
    return speaker_indicies

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

def Search_speakers_for_keywords(Collection_of_speakers, list_of_keywords):
    '''todo: add to lower logic'''
    returnString = ''
    for speaker in Collection_of_speakers:
        for word in list_of_keywords:
            counter = 0
            ##TODO:IMPROVE FOR CASE OF MR> MRS>
            sentences = re.split(r' *[\.\?!][\'"\)\]]* *', speaker.text)
            sentences_with_keyword_for_single_speaker = []
            for sentence in sentences:
                if word in sentence:
                    counter += 1
                    sentences_with_keyword_for_single_speaker.append(sentence)
        if counter != 0:
            printstatement = ' The speaker: ' + speaker.name + ' mentioned' + ' '+ word + ' ' + str(counter) + ' times:\n'
            for x in sentences_with_keyword_for_single_speaker:
                printstatement = printstatement + '\t' + x + '\n'
            returnString = returnString + printstatement
    #returnString = CleanSearchReturnString(returnString)
    return returnString

def Get_speaker_word_count_with_regex(Section):
    '''takes in list of speaker names and returns word count
    first does a split then search then count'''
    '''wordcount tuple with speaker name and word count'''
    #SpeakerWC = namedtuple('SpeakerWC', 'name count')
    #init speakerwc tuples
    SpeakerWCDict = {}
    #for speaker in ListOfSpeakers:
        #x = str(speaker)
        #SpeakerWCDict[x]=0
    #print(SpeakerWCDict)
    sText = Section.text
    #TODO add logic for mrs????
    OrderedList = re.findall(r'Mr\.\s\b[A-Z]+[A-Z]+\b',sText)
    #print("orderedlist: ",OrderedList)
    TextSplit = re.split(r'Mr\.\s\b[A-Z]+[A-Z]+\b',sText)
    #print("TextSplit: ",TextSplit)
    for speaker in OrderedList:
        x = str(speaker)
        SpeakerWCDict[x]=0
    #print(SpeakerWCDict)
    #print(TextSplit)
    listoftextlen = []
    for x in TextSplit:
        length = len(re.split('\W+',x))
        listoftextlen.append(length)
    #print("listoftextlen:", listoftextlen)
    #start at 1 instead of 0 bc we dont need to include text split from title
    i = 1
    #print("starting dict add")
    for spkr in OrderedList:
        #print("the speaker is: ", spkr)
        if spkr in SpeakerWCDict:
            value = SpeakerWCDict.get(spkr,0)
            #print("the old value is: ", value)
            #print("the vvalue to be added is: ", listoftextlen[i])
            SpeakerWCDict[spkr]= value + listoftextlen[i]
            i = i + 1
    result = ''
    for key,value in SpeakerWCDict.items():
        result_line = key +': '+str(value)+' words'+'\n'
        result = result + result_line
    return result


#########################################################################
##FILEIO##
#########################################################################
def GetFileName():
    '''get file name from user'''
    print('Please make sure the file you want to upload is text only (a txt file)')
    filename = input('What is the input file name?')
    return filename


def ReadFile(Filename):
    ''' Read file, returns list! of lines
    :rtype : list
    '''
    #TODO:possibly do errors replace on this line???
    #infile = open(Filename, 'r', encoding='utf-16', errors='ignore')
    #infile = open(Filename, 'r')

    #infile = codecs.open(Filename, 'r', encoding='utf-16', errors='ignore')
    infile = codecs.open(Filename, 'r', encoding='utf-16', errors='replace')
    #TODO: add custom error replace

    #infile = codecs.encode(infile,encoding='ASCII',errors='ignore')
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
    headers = SectionTitlesCleaning()
    #headers_split = headers.split('\n')
    headers_clean = []
    #headers_clean.append('Whole Document')
    for title in headers:
        if title != '':
            headers_clean.append(title)
    return headers_clean

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def ShowSectionTitlesLoop():
    """
    a hack to get arround easy gui breaking when too many sections
    """
    global SECTIONS
    global TITLE
    SelectedChoice = 'Next Page'
    headersclean = SectionTitlesCleaning()
    lenofcollection = len(headersclean)
    numofpages = lenofcollection/10 + 1
    pagecounter = 0

    #firstmessage = 'hey headsclean is:' + str(len(headersclean))
    #eg.msgbox(msg=firstmessage)
    #secondmessage = 'hey numberofpages is:' + str(numofpages)
    #eg.msgbox(msg=secondmessage)
    #thirdmessage = 'hey pagecounter is:' + str(pagecounter)
    #eg.msgbox(msg=thirdmessage)

    #TODO: remove hack from prod
    #headersclean.__delitem__(34)


    #codecs.encode(headersclean,encoding='ascii',errors='replace')
    for title in headersclean:
        #title.encode(encoding='ascii',errors='replace')
        removeNonAscii(title)

    #eg.choicebox('','',headersclean)

    while SelectedChoice == 'Next Page':
        msg = 'Choose an option'
        if pagecounter <= numofpages:
            #msg = 'hey entered 4loop:'
            #eg.msgbox(msg=msg)

            start = pagecounter * 10
            end = (pagecounter*10) + 10
            #FIX: it seems there are a constant amount of section titles arround 30


            #msg = 'hey start,end' + str(start) + str(end)
            #eg.msgbox(msg=msg)

            if end >= lenofcollection:
                end = lenofcollection
            #headersclean.append('Next Page')

            optionstodisplay = headersclean[start:end]
            optionstodisplay.append('Next Page')
            SelectedChoice = eg.choicebox(msg, TITLE, optionstodisplay[start:end+1])

        #TODO:add error for this case, error the user didnt choose anything
        else:
            return 'Error'
        pagecounter += 1
    return SelectedChoice


def ShowSpeakersToUser(RegexSpeakerList):
    title = "Beckman Research Application"
    msg = 'Found Speakers: ' + '.\n' + str(RegexSpeakerList) + '.\n' + 'Continue to do Analysis'
    eg.msgbox(msg, title)


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
    global SPEAKERS
    section, sectionText = ConvertSectionToListOfLines(SectionChoice)
    RegexSpeakerList = ListOfSpeakersFromFindAllSpeakersWithRegex(FindAllSpeakersWithRegex(sectionText))
    #TODO: add back in for prod
    #ShowSpeakersToUser(RegexSpeakerList)
    AnalysisOption = ""
    while AnalysisOption != "Exit":
        AnalysisOption = DisplaySectionAnalysisOptions()
        DisplayText = SectionFunctionality(AnalysisOption, Section, SPEAKERS, RegexSpeakerList)
        title = "Beckman Research Application"
        eg.msgbox(DisplayText,title)
    return 0

#RUN PROGRAM
TITLE = "Beckman Research Application"
SECTIONS = CollectionNew()
SPEAKERS = CollectionNew()
DATA = []

#run()

nonguirun()
