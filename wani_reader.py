
#https://www.wanikani.com/api
#https://gist.github.com/DrLulz/fc802d43e310cec1ecd7
#http://joshualitven.com/creating-anki-cards-using-python/
#https://github.com/dae/anki/tree/master/anki

import os
import json
import urllib.request
import romkan

import wani_sound_dl

def getDataFromWaniKani():
    api_key = "REDACTED"

    vocab_url_template = "https://www.wanikani.com/api/user/%s/vocabulary/"
    
    vocab_url = vocab_url_template % api_key
    
    response = urllib.request.urlopen(vocab_url)
    data = response.read()

    f = open('rawresponse.bytes', 'wb')
    f.write(data)

    return data
    

def getDataFromCacheFile():
    f = open('rawresponse.bytes', 'rb')
    out = f.read()
    return out


def getVocabList():
    dataString = getDataFromWaniKani().decode("utf-8")

    vocabJson = json.loads(dataString)

    realVocabList = list(filter(lambda x: x['user_specific'] is not None, vocabJson['requested_information']['general']))

    for vocab in realVocabList:
        kanji = vocab['character']
        kana = vocab['kana']
        meaning = vocab['meaning']
        vocab.pop('user_specific') #buncha junk in there we don't need
    
##        romaji = romkan.to_hepburn(kana)
##        print(kanji, kana, romaji, meaning)
    return realVocabList


##vocabList = getVocabList()
##
###print(vocabList[0:10]) 
##
##for vocab in vocabList[0:10]:
##    soundUrl = wani_sound_dl.getMp3Url(vocab['character'])
##    filename = "collection.media/wk_" + romkan.to_hepburn(vocab['kana']) + ".mp3"
##    #urllib.request.urlretrieve(soundUrl, filename)
##    print(filename)
##
##print("Download complete")
