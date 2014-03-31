## Daniel Diaz 74393336
##
## Beckman Research Project
##
## Created 2013 copyright Daniel Diaz All Rights Reserved
## Description: Allows for a user to upload a text file and do analytics on it

__author__ = 'danieldiaz'

import os
import easygui as eg
import re
import sys
import codecs


def run():
    """Main Function that will run the whole program including the gui
    :param:none
    :rtype:none
    """
    global TITLE
    global SECTIONS
    global SPEAKERS
    global DATA
    #Welcome Window
    eg.msgbox("Welcome to the Beckman Research Application!", TITLE)
    #Instruction Window
    instruction_string = MakeInstructionString()
    eg.msgbox(instruction_string, TITLE)
    #create window for text file
    msg = ('What is the name of the Text file \n'
           + 'Make sure it is contained within the same folder as the application')
    documentname = eg.enterbox(msg='What is the name of the Text file'
                               , title=TITLE
                               , default='TextDocument'
                               , strip=True
                               , image=None
                               , root=None)
    datafile = os.path.abspath('../../../' + documentname + '.txt')
    DATA = ReadFile(datafile)

    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())
    SECTIONS = CleanSection()

    choices = ShowSectionTitlesToBeSelected()
    choice = eg.choicebox(msg, TITLE, choices)
    #once the use has chose a section to analyze, run the gui
    SectionSelectedGUI(choice)

    if eg.ccbox('EXIT?', TITLE):  # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)  # user chose Cancel

    msg = "Do you want to continue?"
    title = "Please Confirm"
    if eg.ccbox(msg, title):  # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:
        sys.exit(0)  # user chose Cancel


def nonguirun():
    """Main Function that will run the whole program without the gui for testing purposes
    :param:none
    :rtype:none
    """
    global TITLE
    global SECTIONS
    global SPEAKERS
    global DATA
    #testing file path diff than app file path
    datafile = os.path.abspath('test/' + 'TestThis' + '.txt')
    DATA = ReadFile(datafile)
    #Show Section Titles To User
    SECTIONS = AddSectionToCollection(GetSectionTitleIndicies())
    SECTIONS = CleanSection()
    ShowSectionTitlesToBeSelected()
    #hard coded choice
    choice = 'Section Title:FEDERAL ASSISTANCE TO STATES FOR SCHOOL CONSTRUCTION'

    SectionSelectedGUI(choice)

    #print(SECTIONS)
    #print(CollectionToStrHeaders(SECTIONS))
    #print(ShowSectionTitlesToBeSelected())
    #print('\n\n These are all the section titles \n\n')
    #print(sectiontitlestemp)
    #print('\n\n These are all the sections \n\n')
    #tempstrheaders = SectionTitlesCleaning()
    #print(tempstrheaders)
    #for x in tempstrheaders:
    #print(x)
    #eg.choicebox('','',tempstrheaders)
    #print(tempstrheaders[33:35])


#########################################################################
##COLLECTION##
#########################################################################
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
    :param Section
    """
    return ("Section Title:" + Section.title + "\n")


def IsLineUppercase(line):
    """finds out if we are dealing with section title
    :param : line
    :rtype : bool
    """
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


def CleanSection():
    """
    this will clean section title and if it becomes empty, append it to previous section
    """
    global SECTIONS
    tempSECTIONS = []
    count = 0

    #append a begin section to avoid errors
    tempSECTIONS.append(Section('BEGIN', 'No Text.'))

    for section in SECTIONS:
        #print('The section is:',section)
        #clean section title so it will match later
        tempSectionTitle = CleanTitle(section.title)
        #print('the temp title is:',tempSectionTitle)
        text = section.text
        #print('the text from the section is:', text)
        if tempSectionTitle == '' or tempSectionTitle == ' ':
            #todo: add no title logic, will make sure that sention has all associated text and not just partial
            tempSectionTitle = 'No Title Found.' + str(count)
            #dont append anpther section
            #attatch text to previous section
            #print(tempSectionTitle,'is empty')
            #print('text to be appended:',tempSECTIONS[count].text)
            #print('text to be added:',text)
            #tempSECTIONS[count-1].text = text + '\n' + section.text

            #temp2 = Section(tempSectionTitle, section.text)
            #previousSection = tempSECTIONS[count]
            #previousSectionTitle = previousSection.title
            #previousSectionText = previousSection.text
            #textToAppend = previousSectionText + '\n' + section.text
            #tempSECTIONS[count] = Section(previousSectionTitle,textToAppend)

            tempSECTIONS.append(Section(tempSectionTitle, section.text))
        else:
            #append anpther section because title isnt empty
            tempSECTIONS.append(Section(tempSectionTitle, section.text))
        #print('the altered tempsections is:', tempSECTIONS)
        count += 1
    SECTIONS = tempSECTIONS
    return SECTIONS


def CleanTitle(string):
    """
    clean a single title
    :param string:
    """
    for ch in [',', '.', '-', '\r', '\n', '&', '_', '(', ')', '\t', '\t11173', '\t11235', '\\']:
        string = string.replace(ch, '')
    validletters = 'abcdefghijklmnopqrstuvwxyz '
    newstring = ''
    for letter in string.lower():
        if letter in validletters:
            newstring += letter
    #replace multiple spaces
    newnewstring = re.sub(" +", " ", newstring)
    return newnewstring.upper()


def SectionTitlesCleaning():
    """
    This function is used to clean the section title
    it should remove any non a-z chars
    """
    global SECTIONS
    append = False
    titlearray = []
    for tempsection in SECTIONS:
        titlearray.append(tempsection.title)
    cleantitlearray = []
    for temptitle in titlearray:
        string = temptitle
        for ch in [',', '.', '-', '\r', '\n', '&', '_', '(', ')', '\t', '\t11173', '\t11235', '\\']:
            string = string.replace(ch, '')
        validletters = 'abcdefghijklmnopqrstuvwxyz '
        newstring = ''
        for letter in string.lower():
            if letter in validletters:
                newstring += letter
                #print (newstring)
        #this new string should be lower
        #print(newstring)
        if newstring != '':
            #must make upper case b/c previous logic did a tolower
            cleantitlearray.append(newstring.upper())
    return cleantitlearray


def GetSectionText(IndexStart, IndexEnd):
    """gets text using section header indexes
    :param IndexStart:
    :param IndexEnd:
    """
    global DATA
    x = DATA[IndexStart:IndexEnd]
    '''FIX: YOU REMOVED A NEWLINE CHAR WIEN U JOINED< SEE IF THE MESSED ANYTHING UP'''
    result = ''.join(x)
    return result


def GetSectionTitle(Index):
    """gets text using section header indexes
    """
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
    """this will add the sections to the collection using the indicies of headers
    :param IndiciesOfHeaders:
    """
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
    """
    :param SectionChoice:
    """
    global SECTIONS
    choice = SectionChoice[14:]
    #print('Choice: ' ,choice)
    for section in SECTIONS:
        if choice in section.title:
            text = section.text.split('\n')
            return section, text


def SectionFunctionality(Choice, Section, RegexSpeakerList):
    """
    This is called in sectionselectedgui loop
    after a user has made a choice of analysis, this will run the specific choice
    after running it wil return the reult string
    :param Choice:
    :param Section:
    :param RegexSpeakerList:
    """
    global SECTIONS
    global SPEAKERS
    global TESTING

    #this spi variable may be depreciated
    spi = speaker_indicies_from_section(Section, RegexSpeakerList)
    #Speakers = Add_speaker_to_collection(spi,Section,Speakers)
    Speakers = Add_speaker_to_collection_with_regex(Section, SPEAKERS)

    if Choice == 'Look for speaker Keywords':
        #LookForSpeakerKeywords()
        keys = ['black', 'race', 'poor', 'african american']
        text = Search_speakers_for_keywords(Speakers, keys)
    elif Choice == 'Look for manually entered Keyword':
        if TESTING:
            keys = ['poor', 'Chicago']
        else:
            #TODO: this could be imporved by asking the user for comma seperated list
            askingforkey = eg.enterbox(msg='What keyword(s) are you looking for?', title=' ', default='', strip=True,
                                       image=None, root=None)
            keys = []
            keys.append(askingforkey)
        text = Search_speakers_for_keywords(Speakers, keys)
    elif Choice == 'Speaker Word Count':
        text = Get_speaker_word_count_with_regex(Section)
        #RegexSpeakerList.append(askingforspeaker)
    elif Choice == 'Show Found Speakers In Document':
        #text = ShowSpeakersToUser(RegexSpeakerList)
        text = str(RegexSpeakerList)
    elif Choice == 'Exit':
        sys.exit(0)
    else:
        text = "Exiting Program!"
    return text


#########################################################################
##SPEAKER##
#########################################################################
#speaker tuple has both the speaker name and the associated speaker text
Speaker = namedtuple('Speaker', 'name text')


def Add_speaker_to_collection_with_regex(Section, S):
    """
    :param Section:
    :param S:
    """
    #todo: the parameter S for this function may be depreciated
    sText = Section.text
    OrderedList = re.findall(r'Mr\.\s\b[A-Z]+[A-Z]+\b', sText)
    TextSplit = re.split(r'Mr\.\s\b[A-Z]+[A-Z]+\b', sText)
    SpeakerDict = {}
    for speaker in OrderedList:
        x = str(speaker)
        SpeakerDict[x] = ""
    #print("listoftextlen:", listoftextlen)
    #start at 1 instead of 0 bc we dont need to include text split from title
    i = 1
    #print("starting dict add")
    for spkr in OrderedList:
        #print("the speaker is: ", spkr)
        if spkr in SpeakerDict:
            oldText = SpeakerDict.get(spkr, "\n")
            SpeakerDict[spkr] = oldText + TextSplit[i]
            i = i + 1
    for key, value in SpeakerDict.items():
        tempSpeakerTuple = Speaker(key, value)
        TempCollection = CollectionAdd(S, tempSpeakerTuple)
    return TempCollection


def speaker_indicies_from_section(Section, ListOfSpeakers):
    """Takes in section, and list of speakers, and assigns spoken text to speaker tuple.
    :param Section:
    :param ListOfSpeakers:
    """
    sText = Section.text
    #print(Section)
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


def FindAllSpeakersWithRegex(Data):
    """For looking for speakers in the doc
    """
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
    """todo: add to lower logic
    """
    #todo:remove test from priduction
    global TESTING
    if TESTING:
        print(Collection_of_speakers, list_of_keywords)
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
            printstatement = ' The speaker: ' + speaker.name + ' mentioned' + ' ' + word + ' ' + str(
                counter) + ' times:\n'
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
    OrderedList = re.findall(r'Mr\.\s\b[A-Z]+[A-Z]+\b', sText)
    #print("orderedlist: ",OrderedList)
    TextSplit = re.split(r'Mr\.\s\b[A-Z]+[A-Z]+\b', sText)
    #print("TextSplit: ",TextSplit)
    for speaker in OrderedList:
        x = str(speaker)
        SpeakerWCDict[x] = 0
    #print(SpeakerWCDict)
    #print(TextSplit)
    listoftextlen = []
    for x in TextSplit:
        length = len(re.split('\W+', x))
        listoftextlen.append(length)
    #print("listoftextlen:", listoftextlen)
    #start at 1 instead of 0 bc we dont need to include text split from title
    i = 1
    #print("starting dict add")
    for spkr in OrderedList:
        #print("the speaker is: ", spkr)
        if spkr in SpeakerWCDict:
            value = SpeakerWCDict.get(spkr, 0)
            #print("the old value is: ", value)
            #print("the vvalue to be added is: ", listoftextlen[i])
            SpeakerWCDict[spkr] = value + listoftextlen[i]
            i = i + 1
    result = ''
    for key, value in SpeakerWCDict.items():
        result_line = key + ': ' + str(value) + ' words' + '\n'
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
    infile = codecs.open(Filename, 'r', encoding='utf-16', errors='replace')
    #TODO: add custom error replace
    #infile = codecs.encode(infile,encoding='ASCII',errors='ignore')
    data = infile.readlines()
    infile.close()
    return data


#########################################################################
##Display##
#########################################################################

def MakeInstructionString():
    """
    Make Instruction String
    """
    result = ("Instructions to use this app:\n" +
              "\tStep One: Open PDF in Preview\n" +
              "\tStep One: Save PDF as pdf document. (This is to avoid permissions issues)\n" +
              "\tStep One: Open new pdf in Adobe Acrobat Pro\n" +
              "\tStep One: Click Save As then in the menu choose text(plain)\n" +
              "\tStep One: Foroptions make sure utf-16 is selected.w\n" +
              "\tStep One: Put resulting text file in same directory as app\n" +
              "\tStep One: When prompted enter the text file name (excluding the extension)\n" +
              "\tStep One: Follow App Instructions\n")
    return result


def ShowSectionTitlesToBeSelected():
    '''will be used when displaying info for
    user to choose section title to analyze
    '''
    global SECTIONS
    #print(SECTIONS)
    headers = CollectionToStrHeaders(SECTIONS)
    #print(headers)
    #headers = SectionTitlesCleaning()
    headers_split = headers.split('\n')
    headers_clean = []
    #headers_clean.append('Whole Document')
    for title in headers_split:
        #print(title)
        #todo: remove hack where you dont show no title , b/c that will result in partial info
        if title != '':
            if not 'No Title' in title:
                headers_clean.append(title)
                #print(title)
    return headers_clean


def removeNonAscii(s): return "".join(filter(lambda x: ord(x) < 128, s))


def ShowSectionTitlesLoop():
    """
    a hack to get arround easy gui breaking when too many sections
    """
    global SECTIONS
    global TITLE
    SelectedChoice = 'Next Page'
    headersclean = CleanSection()
    lenofcollection = len(headersclean)
    numofpages = lenofcollection / 10 + 1
    pagecounter = 0

    #firstmessage = 'hey headsclean is:' + str(len(headersclean))
    #eg.msgbox(msg=firstmessage)
    #secondmessage = 'hey numberofpages is:' + str(numofpages)
    #eg.msgbox(msg=secondmessage)
    #thirdmessage = 'hey pagecounter is:' + str(pagecounter)
    #eg.msgbox(msg=thirdmessage)

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
            end = (pagecounter * 10) + 10
            #FIX: it seems there are a constant amount of section titles arround 30


            #msg = 'hey start,end' + str(start) + str(end)
            #eg.msgbox(msg=msg)

            if end >= lenofcollection:
                end = lenofcollection
            #headersclean.append('Next Page')

            optionstodisplay = headersclean[start:end]
            optionstodisplay.append('Next Page')
            SelectedChoice = eg.choicebox(msg, TITLE, optionstodisplay[start:end + 1])

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
    ShowSpeakersToUser(RegexSpeakerList)
    AnalysisOption = ""
    while AnalysisOption != "Exit":
        AnalysisOption = DisplaySectionAnalysisOptions()
        DisplayText = SectionFunctionality(AnalysisOption, section, RegexSpeakerList)
        title = "Beckman Research Application"
        eg.msgbox(DisplayText, title)
    return 0

#####RUN PROGRAM#####
TESTING = False
TITLE = "Beckman Research Application"
SECTIONS = CollectionNew()
SPEAKERS = CollectionNew()
DATA = []

if TESTING:
    nonguirun()
else:
    run()
