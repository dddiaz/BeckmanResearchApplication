----------------------------
Beckman Research Application
----------------------------

Language:Python v3
Built For: MAC OS X
Created By: Daniel Diaz
            www.danieldelvindiaz.com
            dddiaz@uci.edu
Copyright: Daniel Diaz All Rights Reserved

This is the Beckman Research Application.
It takes in a text document relating to house or senate transcripts
This application will analyze doc, split it into sections, then split into speakers
It will ask the user what info it wnats then will display:
    Section Titles
    Speakers
    Speaker Word COunt
    Speaker Keywords (the associated text and speaker related to a key word)

To Use this application you must have a text ffile.
If using a scanned pdf of a senate/congressional transcript, must convert to text (ENCODING UTF-16!!!!)
My suggestion would be to use Adobe acrobat pro and the save as feature.
This seems to give the best results with rgards to pdf text interpretation.


STEPS TO CONVERT:
TO Convert you need to do a workaround (there are permissions issue)
first open the doc in preview, export as pdf
then open file in adobe acrobat pro
then save as where the format should be plain text
and under settings it should be utf-16

Notes for Jenny:
#TODO: add no title logic, it seems to break the program for some reason
##TODO: hey u may have figured a way to do page numbers, tell jenny,
##TODO: case where title is multi line????
##TODO: The doc Translation is way better with adobe

##NOTE: You hardcoded the setting for txt export as utf-16!!!!!