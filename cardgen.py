
#https://gist.github.com/DrLulz/fc802d43e310cec1ecd7
#http://joshualitven.com/creating-anki-cards-using-python/
#https://github.com/dae/anki/tree/master/anki

import os
from anki import Collection
#^Download the anki repo, point PYTHONPATH at it
import json
import urllib.request
import wani_reader
import wani_sound_dl
import romkan
import time

def hasCard(collection, text):
    return len(collection.findCards('deck:WaniKaniVocab expression:"' + text + '"')) > 0


def addVocabCard(col, vocab):
    deck_id = col.decks.id("WaniKaniVocab")
    col.decks.select( deck_id )
    model = col.models.byName( "JP Reading" )
    model['did'] = deck_id
    col.models.save( model )
    col.models.setCurrent( model )

    mp3name = wani_sound_dl.downloadMp3ForVocab(vocab)
    kana = vocab['kana']
    meaning = vocab['meaning']

    note = col.newNote()
    note['Expression'] = kana
    note['Meaning'] = meaning
    note['Audio'] = "[sound:%s]" % mp3name
    note.addTag("level%d" % vocab['level'])
    
    col.addNote(note)

cwd = os.getcwd()
col = Collection("collection.anki2")
os.chdir(cwd) #Collection() changes cwd for no goddamn reason

try:
    vocabList = wani_reader.getVocabList()

    for vocab in vocabList:
        name = romkan.to_hepburn(vocab['kana'])
        if not hasCard(col, vocab['kana']):
            addVocabCard(col, vocab)
            print("Created card for " + name)
            time.sleep(1)
        else:
            print("-Skipped existing card " + name)
        
    

finally:
    col.close()
