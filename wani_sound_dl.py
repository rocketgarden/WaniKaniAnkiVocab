import os
import urllib
import re
import io
import romkan

def getMp3Url(slug):
    
    slug_url_template = "https://www.wanikani.com/vocabulary/%s"
    
    slug = urllib.parse.quote(slug)
    url = slug_url_template % slug

    for line in open('cookie.txt'):
        header = {
            "Cookie": line
        }

    request = urllib.request.Request(url, headers = header)
    page = urllib.request.urlopen(request)
    data = page.read()
    encoding = page.info().get_content_charset('utf-8')
    html = data.decode(encoding)
    match = re.search(r"(https://cdn\.wanikani\.com/audio/[\w\d]*\.mp3)", html)

    return match.group(0)
    
    
def downloadMp3ForVocab(vocab):
    soundUrl = getMp3Url(vocab['character'])
    mp3Name = "wk_" + romkan.to_hepburn(vocab['kana']) + ".mp3"
    filename = "collection.media/" + mp3Name
    urllib.request.urlretrieve(soundUrl, filename)
    print("Downloaded " + mp3Name)
    return mp3Name


