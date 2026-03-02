import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) < 2:
        print("Not a valid url")
        return

    url=sys.argv[1]
    file=requests.get(url)
    if file.status_code!=200:
        print("Unable to load the requested page")
        return

    html=file.text
    soup=BeautifulSoup(html, "html.parser")
    if soup.title:
        print(soup.title.text.strip())
    else:
        print("")
    if soup.body:
        text_output=soup.body.get_text()
        print(text_output.strip())
    else:
        print("")
    printed=[]
    req_links=soup.find_all("a")
    for tag in req_links:
        req_link=tag.get("href")
        if req_link:
            if req_link not in printed:
                print(req_link)
                printed.append(req_link)
