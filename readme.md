I wasn't able to find a free scraping utility online, so I made one in python.

I don't think it acts as competition to many of the fee-based scraping tools, as when I demo'd them they were easy to use, easy to browse, easy to convert. This project is none of those things. However, if you're willing to spend a little time on setting it up and deal with the inconvenience of editing the python file directly with your latest cookie and such, and accept its output is one giant JSON file, it should work well!

I made this about 6 months ago to crawl a private database I had access to then convert them to one giant JSON file which mirrors the URL structure of the site in the JSON node structure. I did this because I was considering plugging it into AI or at least giving me more options to search said database. I'm just now uploading as I had to remove much of the identifying information from that database and make it more generic. I never was sure I was going to put a public version of it so its a bit user unfriendly, but it has nice options, and is pretty much failsafe regardless how the website is structured. It also will save the data it has crawled so far every 10 minutes. If you're worried about hitting the target website too often you can change the ```time.sleep(1)``` (seconds) to add a delay between requests.

The command line / terminal output is pretty mesmerizing if I do say so myself with useful information about what it's accessing. The BL urls list (red text) is good to understand how many pages will be in your all_page_data.json file when it exits.

Be careful with this program as if the website is very large it may just crawl the entire thing. There are exceptions where depth could surpass how it works recursively (actually not that difficult to modify) but websites tend to be flat and have multiple links to the same page throughout their structure so getting too much is likely to be more of a problem than getting too little. That said it is good at not duplicating data.

There is even a somewhat prototype search page for the JSON file with ```scrape.html```. It has an amcharts integration trying to show the node structure of the JSON file graphically, but to be honest most websites url structure is super flat so it's not all that useful.
You'll have to disable CORS in Chrome somehow. (E.g. To use it to load a local file in Chrome you'll have to do something like windows key + r > paste ```chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security``` then copy and paste the local file (e.g. ```C:\stuff\scrape\scrape.html```) into the address bar of Chrome.

For the JSON file itself: The JSON structure has the text_content as the main page text. The rest is probably a little too much, but there seemed no real reason to leave out the extra page information gathered by beautiful soup - the python library used to process the page.

Within text_content consecutive line feeds or '\n' 's are cut down to two, the same with whitespace.

Some pages cannot be crawled with this. It could be because they have detection for this type of stuff. I did not try to get around it, but your mileage may vary. For example this does not work to scrape https://news.google.com.

How to crawl:

Get the editthiscookie extension from chrome extension store
Navigate to the site you want to scrape
Click its icon in the upper right after ensuring its pinned in your managed extensions
Click export
Cookies will be copied to the clipboard and look like this, but longer:

```
[
{
    "domain": ".google.com",
    "expirationDate": 1752296841.813874,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__Secure-1PAPISID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "GIcGpTFFvGxFYqWr/A9mSVJih2bw3C_SjS",
    "id": 1
},
{
    "domain": ".google.com",
    "expirationDate": 1752296841.813862,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__Secure-1PSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "g.a000kghhVC-KxI1mulXx8gXgnh34ilaLyP6MJ_Q5RXO0G_9cATKqI9RLxEHQ1NY63kdwHRXH7wACgYKAZUSARISFQHGX2Mi_3U20LW0jn20hOszNHXl2BoVAUF8yKolyMZpYbgqJMt8QZtnIR6W0076",
    "id": 2
},
]
```
You will need to do a find > replace in a text editor and replace "false" 's with "False" and "true" 's with "True" as for python that matters.

Now edit the scrape.py section in question pasting over the cookie there presently, from '[' to ']'.

Still within scrape.py change the ```my_start_url``` to the parent page you want to start crawling at.
Add and remove items from the ```name_blacklist``` & ```phrase_blacklist```. Phrase blacklist is based on text on the page, name blacklist is based on the URL or the title of the page if I recall correctly.

The ```allow_list``` should be the folders (full url starting at https://...) of the website you would like to crawl. So, it does need to be edited, but if you want to crawl the entire site (unlikely) you can just copy ```my_start_url``` to it. 

Obviously for any errors about running:
```python scrape.py```

such as missing 'requests'
one simply performs ```pip3 install requests``` and repeats as necessary.

Hit Esc to end the crawl.

Running it again resumes where it left off.

If you decide to start crawling a new website recommend you backup the all_page_data.json as your extracted database from your current scraping project...

Then delete files matching something like this pattern (basically any recent files created or modified since you last ran scrape.py), and modify scrape.py with a new cookie, new my_start_page, and new allow_list url's for your new scraping project.

```all_page_data*.json
urls_crawled*.json
urls_problematic.json
urls_queue*.json
data*.json```
