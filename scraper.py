import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) <2:
        print("Not a valid url")
        return
    url = sys.argv[1].strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" +url
    try:
        file =requests.get(url)
    except:
        print("Unable to load the requested page")
        return
    if file.status_code!=200:
        print("Unable to load the requested page")
        return
    html =file.text
    soup= BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        print(soup.title.string.strip())
    else:
        print("")
    if soup.body:
        text_output =soup.body.get_text(separator=" ", strip=True)
        print(text_output)
    else:
        print("")
    printed =[]
    req_links= soup.find_all("a")
    for tag in req_links:
        req_link =tag.get("href")
        if req_link and req_link not in printed:
            print(req_link.strip())
            printed.append(req_link)
