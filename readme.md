# Intro

I wasn't able to find a free, crawling, website scraping utility online, so I made one in python.

(Edit: looks like there are some free tools out there that scrape, though quite a bit more complicated than my project - Selenium integration, etc. - wish this article was posted 6 months ago! :)
https://blog.apify.com/top-11-open-source-web-crawlers-and-one-powerful-web-scraper/



# Output

The JSON output looks something like this, though it also has the main domain content parallel with the first level of folders for the domain:

```
{
    "name": "https://www.nationalgeographic.com/",
    "children": [
        {
            "name": "topic",
            "path": "topic",
            "children": [
                {
                    "name": "topic/careers",
                    "path": "topic/careers",
                    "children": [
                        {
                            "name": "Careers at National Geographic",
                            "meta_tags": {
                                ...
                            },
                            "text_content": "\n\nCareers at National Geographic\n\nSkip to contentNewslettersSubscribeMenuCareers at National GeographicNational Geographic was founded in 1888 by a group of visionaries who embodied an era of exploration, discovery, invention, and change. With offices around the world and headquarters in Washington, D.C., we offer a unique opportunity to be part of a world-class institution with a strong global brand and a rich history. Explore our open positions now.A career with us means working hard to achieve our mission in a collaborative and inclusive culture. We have a talented team with diverse people, ideas, interests, and ...",
                            "url": "https://www.nationalgeographic.com/pages/topic/careers",
                            "value": 1,
                            "path": "pages/topic/careers",
                            "children": [],
                            "crawled": true,
                            "links": [
                                "https://www.nationalgeographic.com/newsletters/signup",
                                ...
                            ],
                            "branch": false
                        }
                    ],
                    "value": 1,
                    "crawled": false,
                    "url": "https://www.nationalgeographic.com/topic/careers",
                    "branch": true
                }
            ],
            "value": 0,
            "crawled": false,
            "url": "https://www.nationalgeographic.com/topic",
            "branch": true
        },
```

For the JSON file itself: The JSON structure has the text_content as the main page text. The rest is probably a little too much, but there seemed no real reason to leave out the extra page information gathered by beautiful soup - the python library used to process the page.

Within text_content consecutive line feeds or '\n' 's are cut down to two, the same with whitespace. BeautifulSoup doesn't return the raw HTML, it returns mostly text.

# Details

I don't think it acts as competition to many of the fee-based scraping tools, as when I demo'd them they were easy to use, easy to browse, easy to convert. This project is none of those things. However, if you're willing to spend a little time on setting it up and deal with the inconvenience of editing the python file directly with your latest cookie and such, and accept its output is one giant JSON file, it should work well!

I made this about 6 months ago to crawl a private knowledgebase I had access to then convert them to one giant JSON file which mirrors the URL structure of the site in the JSON node structure. I did this because I was considering plugging it into AI or at least giving me more options to search said database. I'm just now uploading as I had to remove much of the identifying information from that database and make it more generic. I never was sure I was going to put a public version of it so its a bit user unfriendly, but it has nice options, and is pretty much failsafe regardless how the website is structured. It also will save the data it has crawled so far every 10 minutes. If you're worried about hitting the target website too often you can change the ```time.sleep(1)``` (seconds) to add a delay between requests. Because I made this 6 months ago I'm not sure exactly all the information regarding it, but I did my best before publishing it. I am fairly certain it will work on linux, but I never tested it. I do believe the libraries imported into python are all cross platform.

This program does not use the sitemap at all, except to consider it another page to grab links from if an HTML version of it exists in the hierarchy of the HTML pages, themselves. I don't find sitemaps to be particularly compelling for a starting point to scrape, but it might be good to check a site's sitemap to understand what folders to look at and input into this program.

For some reasona a NoneType error will happen rarely when starting scraping a new site. Because this program was designed with a lot of failsafes, just run it again and it should resolve the issue, or delete your JSON files and start over, assuming they're corrupted by users misconfiguring different URL's in scrape.py between resuming sessions.

The command line / terminal output is pretty mesmerizing if I do say so myself with useful information about what it's accessing. The BL urls list (red text) is good to understand how many pages will be in your all_page_data.json file when it exits.

![scrape in action](scrape.png?raw=true "Scrape in action")

Be careful with this program as if the website is very large it may just crawl the entire thing. There are exceptions where depth could surpass how it works recursively (actually not that difficult to modify) but websites tend to be flat and have multiple links to the same page throughout their structure so getting too much is likely to be more of a problem than getting too little. That said it is good at not duplicating data. The depth is set to 15 by default, but the depth reported from the terminal output is more the chain as in it doesn't think of depth as a result of the folder structure of the website, but the link in its chain. It will process all unprocessed links on a particular page before it reduces the depth variable, but it will also process all the pages on the links for the page it's processing from that page... so it basically goes on a treasure hunt and all the depths get resolved as more and more URL's are processed near the end of the crawl. This isn't the best algorithm but it is certainly easy to implement and it should process just as fast as any other single thread crawler.

Some pages cannot be crawled with this. It could be because they have detection for this type of stuff. I did not try to get around it, but your mileage may vary. For example this does not work to scrape https://news.google.com.

# Viewer

There is even a somewhat prototype search page for the JSON file with ```scrape.html```. It has an amcharts integration trying to show the node structure of the JSON file graphically, but to be honest most websites url structure is super flat so it's not all that useful.
You'll have to disable CORS in Chrome somehow. (E.g. To use it to load a local file in Chrome you'll have to do something like windows key + r > paste ```chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security``` then copy and paste the local file (e.g. ```C:\stuff\scrape\scrape.html```) into the address bar of Chrome.

# How-to

This is designed for crawling websites you have to login to. So, we'll need the cookie first.
Get the ```editthiscookie``` extension from chrome extension store
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

Still within scrape.py change the ```my_start_url``` to the parent page you want to start crawling at. It's best practice to just make this the domain and put the actual start page in the ```allow_list``` below.
Add and remove items from the ```name_blacklist``` & ```phrase_blacklist```. Phrase blacklist is based on text on the page, name blacklist is based on the URL or the title of the page if I recall correctly.

The ```allow_list``` should be the folders (full url starting at https://... so https://news.google.com/articles for example) of the website you would like to crawl. So, it does need to be edited, but if you want to crawl the entire site (unlikely) you can just copy ```my_start_url``` to it. 

Obviously for any errors about running:
```python scrape.py```

such as missing 'requests'
one simply performs ```pip3 install requests``` and repeats as necessary.

Hit Esc to end the crawl.

Running it again resumes where it left off.

# Starting a new crawl

If you decide to start crawling a new website recommend you backup the all_page_data.json as your extracted database from your current scraping project...

Then delete files matching something like this pattern (basically any recent files created or modified since you last ran scrape.py), and modify scrape.py with a new cookie, new my_start_page, and new allow_list url's for your new scraping project.

```
all_page_data*.json
urls_crawled*.json
urls_problematic.json
urls_queue*.json
data*.json
```

Use for commercial reasons or use for private reasons at your own risk keeping in mind the licenses of the imported libraries (Beautiful Soup, colorama, amcharts5 etc.)
