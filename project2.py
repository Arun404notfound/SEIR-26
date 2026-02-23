import sys
import requests
from bs4 import BeautifulSoup
import re

P = 53
M = 2**64
def fetch_page(url):
    req_page=requests.get(url)
    if req_page.status_code==200:
        return req_page.text
    return None

def text_content(html):
    soup=BeautifulSoup(html, "html.parser")
    if soup.body:
        return soup.body.get_text()
    return ""

def fetch_words(text):
    words =re.findall(r"[A-Za-z0-9]+", text)
    lower_words =[]
    for wrd in words:
        lower_words.append(wrd.lower())
    return lower_words

def word_freq_count(words):
    word_freq ={}
    for wrd in words:
        if wrd in word_freq:
            word_freq[wrd] += 1
        else:
            word_freq[wrd] =1
    return word_freq

def polynomial_hash(word):
    initial_value =0
    power =1
    for chr in word:
        initial_value =(initial_value + (ord(chr) * power)) % M
        power =(power * P) % M
    return initial_value

def simhash(freq_dict):
    vec=[0]*64
    for word in freq_dict:
        a= polynomial_hash(word)
        f= freq_dict[word]
        b= bin(a)[2:].zfill(64)
        for i in range(64):
            if b[i]== '1':
                vec[i]+= f
            else:
                vec[i]-= f
    final=""
    for v in vec:
        if v >0:
            final +="1"
        else:
            final +="0"
    return int(final,2)

def common_bits_count(h1, h2):
    b1 = bin(h1)[2:].zfill(64)
    b2 = bin(h2)[2:].zfill(64)
    count_bits = 0
    for i in range(64):
        if b1[i] == b2[i]:
            count_bits += 1
    return count_bits

def main():
    if len(sys.argv) < 3:
        print("Give two urls")
        return

    url_1 = sys.argv[1]
    url_2 = sys.argv[2]
    html_1 = fetch_page(url_1)
    html_2 = fetch_page(url_2)
    if html_1 == None or html_2 == None:
        print("error fetching pages")
        return
    text_1 = text_content(html_1)
    text_2 = text_content(html_2)
    words_1 = fetch_words(text_1)
    words_2 = fetch_words(text_2)
    freq_1 = word_freq_count(words_1)
    freq_2 = word_freq_count(words_2)
    sim_1 = simhash(freq_1)
    sim_2 = simhash(freq_2)
    common = common_bits_count(sim_1, sim_2)
    print(common)
