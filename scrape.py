from datetime import datetime
import traceback
import keyboard
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init, Style
import json
import re
import sys
import random
import time
import threading


my_start_url = "https://news.google.com/"
queue_urls = []
queue_urls.append(my_start_url)

# import copy
random.seed(int(time.time()))

# Example JSON data with cookies
cookie_json = [
{
    "domain": ".google.com",
    "expirationDate": 1752223441.813874,
    "hostOnly": False,
    "httpOnly": False,
    "name": "__Secure-1PAPISID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "GIcGdsdasdfaYqWr/A9mSfsdfSjS",
    "id": 1
},
{
    "domain": ".google.com",
    "expirationDate": 1125222342.813862,
    "hostOnly": False,
    "httpOnly": True,
    "name": "__Secure-1PSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "g.a000kghhVasfadsfasdfCgYKAZUSARawefawefsadfHXl2BoVAUF8yKolyMZpYbgqJMt8QZtnIR6W0076",
    "id": 2
},
]

init(autoreset=True)

# Define color variables
BLUE = Fore.BLUE
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
DKGREY = Fore.BLACK
RESET = Style.RESET_ALL

valid_pages = 0
iteration = 0
esc_pressed = False
total = 0
deleted = 0
seek_url = ""
consecutive_urls = ""

all_page_data = {}
my_page_data = {}
crawled_urls = []
LOAD_URLS = True

def on_esc(event):
    global esc_pressed
    if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
        esc_pressed = True

keyboard.on_press_key('esc', on_esc)


data_lock = threading.Lock()  # Create a lock for data access

# Function to save your data
def save_data():
    global consecutive_urls, my_page_data, crawled_urls, queue_urls
    print("*Autosave*")
    with data_lock:
    # with open('data.json', 'w') as file:
            my_page_data["last_url"] = consecutive_urls
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            filename = f"data{timestamp}.json"
            filename2 = f"urls_crawled{timestamp}.json"
            filename3 = f"urls_queued{timestamp}.json"
            save_to_json(my_page_data, filename)
            save_to_json(crawled_urls, filename2)
            save_to_json(queue_urls, filename3)


import threading

class RepeatTimer:
    def __init__(self, interval):
        self.interval = interval
        self.timer = None

    def start(self):
        self.timer = threading.Timer(self.interval, self.start)
        self.timer.start()
        save_data()

    def cancel(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

# ----------------------------- Execution v --------------------------------------(kind of)
print("Attempting to load json data...")

# Check if a filename argument was provided
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    # Use a default filename if no argument is provided
    filename = 'all_page_data.json'

def count_nodes(node):
    count = 0
    if "children" in node:
        if "text_content" in node:
            count = 1
        for child in node["children"]:
            count += count_nodes(child)
        return count
    else:
        return 1  # Leaf node

if (LOAD_URLS):
    lines_to_display = 3

    try:
        with open('urls_crawled.json', 'r') as file:
            crawled_urls = json.load(file)
            print("Avoiding these urls:")
            # Get random lines
            if lines_to_display < len(crawled_urls):
                random_lines = random.sample(crawled_urls, lines_to_display)
                print(GREEN+str(len(crawled_urls))+RESET+" urls loaded from json")
                print("...")
                for line in random_lines:
                    print(line)
                print("...")

        with open('urls_queue.json', 'r') as file:
            queue_urls = json.load(file)
            print("Seeking these urls:")
            # Get random lines
            if lines_to_display < len(queue_urls):
                random_lines = random.sample(queue_urls, lines_to_display)
                print(GREEN+str(len(queue_urls))+RESET+" urls loaded from json")
                print("...")
                for line in random_lines:
                    print(line)
                print("...")
        
        with open('urls_problematic.json', 'r') as file:
            mean_urls = json.load(file)
            print("Problematic urls:")
            # Get random lines
            if lines_to_display < len(mean_urls):
                random_lines = random.sample(mean_urls, lines_to_display)
                print(GREEN+str(len(mean_urls))+RESET+" urls loaded from json")
                print("...")
                for line in random_lines:
                    print(line)
                print("...")

    except:
        # Handle the exception (e.g., print an error message, set default values, or take appropriate action)
        print("Failed to load JSON urls")
        traceback.print_exc()
        
        

try:
    with open(filename, 'r') as file:
        all_page_data = json.load(file)
        total = count_nodes(all_page_data)
        print(BLUE+"JSON loaded "+GREEN+str(total)+RESET+" nodes from "+YELLOW+filename+RESET)
        
except:
    # Handle the exception (e.g., print an error message, set default values, or take appropriate action)
    print("Failed to load JSON all_page_data")
    all_page_data = {} #this is our main array of json site data


name_blacklist = [
    "dolphins",
    "controversy",
    "inappropriate"
]
phrase_blacklist = [
    "#",
    "penguin feet",
    "scary fish"
]

#just the list of urls that are problematic
mean_urls = []


allow_list = [
    "https://news.google.com/topics/"
]

# Initialize an empty dictionary for the session cookies
session_cookies = {}



# Iterate through the JSON data and extract cookies
for cookie in cookie_json:
    cookie_name = cookie.get("name")
    cookie_value = cookie.get("value")
    if cookie_name and cookie_value:
        session_cookies[cookie_name] = cookie_value

# Print the resulting session_cookies dictionary
# print(session_cookies)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    with open('urls_crawled.json', 'w') as file:
        filtered_links = list(set(crawled_urls))
        json.dump(filtered_links, file)
    with open('urls_queue.json', 'w') as file:
        filtered_links = list(set(queue_urls))
        json.dump(filtered_links, file)
    with open('urls_problematic.json', 'w') as file:
        filtered_links = list(set(mean_urls))
        json.dump(filtered_links, file)
    

def my_save_to_json(my_page_data):
    global consecutive_urls
    my_page_data["last_url"] = consecutive_urls
    timestamp = datetime.now().strftime("%Y%m%d%H")
    save_to_json(my_page_data, filename)
    filename2 = f"all_page_data_{timestamp}.json"
    save_to_json(my_page_data, filename2)
    
    # Save the URLs to a JSON file


# Reduces consecuitive \n's or whitespaces characters over 3 to only 2
def process_text_content(text_content):
    # Replace more than two consecutive newlines with two newlines
    text_content = re.sub(r'\n{3,}', '\n\n', text_content)
    
    # Replace more than two consecutive whitespaces with two whitespaces
    text_content = re.sub(r'\s{3,}', '  ', text_content)

    # Define the start and end markers
    start_marker = "Expand/collapse global hierarchy"
    end_marker = "Back to top"
    
    # Use regular expressions to find the text between markers
    pattern = re.compile(re.escape(start_marker) + "(.*?)" + re.escape(end_marker), re.DOTALL)
    match = pattern.search(text_content)
    
    if match:
        # Extract and return the text between the markers
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return text_content


def generate_branches(target_url, all_page_data):
    global total, consecutive_urls, my_start_url

    target_path = target_url.replace(my_start_url, "")
    target_path = target_url.replace(my_start_url, "")
    parts = target_path.split('/')
    parts = parts[1:]
    # print(parts)
    # parts = parts[:-1]
    if len(parts) > 1:
        term_part = parts[-1]
    elif len(parts) > 0 and len(parts) <= 1:
        term_part = parts[0]
    else:
        term_part = ""
    # print(parts)
    # Start with the root node
    # buffer_node = copy.deepcopy(all_page_data)
    my_buffer = all_page_data
    current_node = my_buffer
    found_node = None

    if current_node == {} or not isinstance(current_node, dict):
 
        #  all_page_data = current_node
        exit("No Data")
        # return None, None, my_buffer, False
    # print(target_path)
    if "url" in current_node:
        if current_node["url"] is target_url:
            return current_node, current_node, current_node  , False 
    if current_node["path"] == target_path:
        return current_node, current_node, current_node, False
    # print(parts, term_part)

    parent_branch = current_node

    for part in parts:
        # Find the child node with the current part and path as its attributes
        child_node = None
        created = False
        # print(current_node)
        # if "children" in current_node:
        index = 0
        for node in current_node["children"]:
            if "path" in node:
                my_parts = '/'.join(parts[:parts.index(part) + 1])
                
                # print (node['path'], my_parts)
                if node['path'] == my_parts:
                    child_node = node
                    # for some reason this term_part == part is needed, which is inevitable and the other target_path should work but seems like it would need another loop to catch it
                    if node['path'] == target_path or term_part == part:
                        print(BLUE + 'Path found: ' + my_parts + RESET)
                        return node, parent_branch, my_buffer, created
                    break
            index += 1


        # Make some branches
        if child_node is None:
            path_node = '/'.join(parts[:parts.index(part) + 1])
            my_url = my_start_url + path_node
            child_node = {'name': path_node, 'path': path_node, 'children': [], "value": parts.index(part), "crawled": False, "url": my_url, "branch" : True}
            if my_url not in crawled_urls:
                crawled_urls.append(my_url)
            
            print(YELLOW + 'Adding pathing... ' + child_node["path"] + RESET)
            current_node["children"].append(child_node)
            created = True
            # total += 1
            

        # Move to the child node and continue processing the URL
        if 'children' in current_node:
            parent_branch = current_node
            current_node = current_node["children"][-1]
        else: #couldn't hurt
            path_node = '/'.join(parts[:parts.index(part) + 1])
            my_url = my_start_url + path_node
            child_node = {'name': path_node, 'path': path_node, 'children': [], "value": parts.index(part), "crawled": False, "url": my_url, "branch" : False}
            if my_url not in crawled_urls and my_url != my_start_url:
                crawled_urls.append(my_url)
            print(GREEN + 'GEN:Adding... ' + child_node["path"] + RESET)
            current_node["children"].append(child_node)
            created = True
            # total += 1
            if parent_branch is None: parent_branch = current_node
            return current_node, parent_branch, my_buffer, created

        # Check if the current path matches the target path
        if current_node['path'] == target_path:
            found_node = current_node
            return found_node, parent_branch, my_buffer, created
    
    if created:
        print("Created")
    print("Not found, yet.")
    return found_node, parent_branch, my_buffer, created

# Regular expression pattern to match valid URLs with "https://ans...
def is_valid_url(url):
    global allow_list
    

    url = str(url)
    # Remove the pound symbol '#' if it exists in the URL
    url = url.replace('#', '')

    res = False

    for eurl in allow_list:
    # Reformat each string and append to the pattern list
        # formatted_pattern = re.escape(url) + r'\S+'
        if url == eurl:
            return True
        eurl = re.escape(eurl) 
        formatted_pattern = eurl + r'\S+'
        #the "is not none" below is for forcing it to return True (value) or False (none)
        res = re.match(formatted_pattern, url) is not None
        # print(res)
        if res:
            return res
    
    return res

def text_peep(text, length):
    if len(text) > length and not isinstance(text, list):
        return text[-length:]
    return text

    
def update_master_list(existing_urls, master_urls):
    for url in existing_urls:
        if url not in master_urls:
            master_urls.append(url)
    return master_urls

def remove_from_master_list(urls_to_remove, master_urls):
    if not isinstance(urls_to_remove, list):
        print("Trying to curate...", text_peep(urls_to_remove, 32))
        for m_url in master_urls:
            if m_url == urls_to_remove:
                print("Page Crawled...", text_peep(m_url, 32))
                master_urls.remove(m_url)

    for url in urls_to_remove:
        for m_url in master_urls:
            if m_url == url:
                print("Page Crawled...", m_url)
                master_urls.remove(m_url)
    return master_urls


#main beast
def crawl_page(url, depth=1, max_depth=3, all_page_data=[], crawled_urls=[], queue_urls=[], session_cookies=session_cookies, crawled=False, seek=False):
    global valid_pages, esc_pressed, name_blacklist, iteration, total, deleted
    global seek_url, consecutive_urls
    global allow_list, my_start_url
    parent_branch = None
    print("Checking... " + text_peep(url, 32))
    
    
    iteration += 1
    exists = False
    
    if (esc_pressed): return url, depth - 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek

    if url != my_start_url:
        while url in crawled_urls or is_valid_url(url) == False: 
            if len(queue_urls) > 0:
                if url in queue_urls:
                    queue_urls.remove(url)
                if len(queue_urls) > 0:
                    url = queue_urls[-1]
                else:
                    url = my_start_url
                    break
            else:
                url = my_start_url
                break
        


    try:
        # Send an HTTP GET request with your session cookies
        print("Crawling... " + url)
        response = requests.get(url, cookies=session_cookies)
        time.sleep(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Create a dictionary to store the hierarchical data
            page_data = {"name": url}
            if url == None or isinstance(url, type(None)):
                return url, depth - 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek

            # Extract and store meta tags
            meta_tags = soup.find_all('meta')
            meta_data = {}
            for tag in meta_tags:
                tag_name = tag.get('name', tag.get('property', ''))
                tag_content = tag.get('content', '')
                meta_data[tag_name] = tag_content
            page_data['meta_tags'] = meta_data

            if 'og:title' in page_data['meta_tags']:
                page_data['name'] = page_data['meta_tags']['og:title']
            else:
                match = re.search(r'/([^/]+)/([^/]+)\.aspx$', page_data['name'])
                if match:
                    page_data['name'] = match.group(1) + " " + match.group(2)
        
            # Extract and store text content
            text_content = soup.get_text()
            page_data['text_content'] = process_text_content(text_content)

            if page_data['text_content'] == "":
                page_data['text_content'] = "Nothing here."
            
            if 'og:url' in page_data['meta_tags']:
                url = page_data['meta_tags']['og:url']
            page_data['url'] = url


            # Append the page_data to the all_page_data array
            
            page_data['value'] = depth #we have to set the value to something, depth has lost all meaning in the evolution of the code
            links = soup.find_all('a')
            #all_page_data.append(page_data)
            node = None

                        # Create a list to store the links
            link_list = []


            # Iterate through the page's links 
            for lk in links:
                link_list.append(lk.get('href'))
            # Removes ? and extra characters after
            pattern = r'\?.*'
            # Filter them a little, but carefully because they are weird or maybe this code is.
            if not isinstance(link_list, type(None)):
                for i, my_url in enumerate(link_list):
                    if not isinstance(my_url, type(None)):
                        link_list[i] = re.sub(pattern, '', my_url)


            
            # Function to validate URLs

            # Filter URLs using compiled lists
            link_list = [eurl for eurl in link_list if is_valid_url(eurl) and \
                        all(phrase not in eurl for phrase in phrase_blacklist) and \
                        all(doneurl != eurl for doneurl in crawled_urls) and \
                        all(meanurl != eurl for meanurl in mean_urls)]
            
            
            queue_urls = update_master_list(link_list, queue_urls)
            #Generate Paths:
            node, parent_branch, all_page_data, created = generate_branches(url, all_page_data)
            # node = parent_branch   

            page_data["path"] = url.replace(my_start_url, "")
            page_data["children"] = []
            page_data["crawled"] = crawled
            page_data["links"] = link_list
            page_data["branch"] = False
            if "text_content" in page_data: valid_pages += 1
            if not isinstance(node, type(None)):
                if 'children' not in node:
                    node.children = []
            else:
                # print("Node not found for some reason.")
                #We run another pass because frankly it's surprisingly complicated to get the
                #generate_branches to generate the branch end points and link it to the creation of the page
                #Tbh I should probably just split it into two functions, just a kludgy evolution, which also makes it
                #robust.
                node, parent_branch, all_page_data, created = generate_branches(url, all_page_data)
                if not isinstance(node, type(None)):
                    if 'children' not in node:
                        node.children = []

                # return None, all_page_data
            # if (not created):
            if "text_content" not in node["children"]:
                node["children"].append(page_data)

                print(GREEN + 'Adding... ' + url + RESET)
                my_val = page_data['value']
                my_name_blacklisted = len(crawled_urls)
                my_pages = valid_pages + total
                queue_number = len(queue_urls)
                
                print("Iteration: "+BLUE+f"{iteration}  "+RESET+"Queued: "+YELLOW+f"{queue_number}"+RESET+" crawls")
                print("Total/Currently Souped Nodes: "+GREEN+f"{my_pages}"+BLUE+'/'+GREEN+f"{valid_pages}"+RESET+" Depth: "+YELLOW+f"{my_val}"+RESET+" BL urls: "+RED+f"{my_name_blacklisted}"+RESET+" Deleted Nodes: "+RED+f"{deleted}"+RESET)
            else:
                my_node = node["children"]
                print(YELLOW+"Seems like it already exists..."+RESET+my_node)

            if url not in crawled_urls:
                crawled_urls.append(url)
                #crawled_urls is the banlist / crawled URL list
            consecutive_urls = page_data["url"]
            queue_urls = remove_from_master_list(url, queue_urls)
            # print (crawl_urls, url)
            if (len(queue_urls) > 0):
                next_url = queue_urls[-1]
                print("Next Url... ", text_peep(next_url, 32))
                # print(crawl_urls)
                if next_url == url:
                    print("Odd.. This is supposed to be removed.")
                    return parent_branch, all_page_data
                # the following three returns should be very rare, if ever
                return next_url, depth + 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek
            else:
                print("No more links to crawl")
                return url, depth - 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek
            
            return url, depth - 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek
                    

    except Exception as e:
        print(f"Error while crawling {url}: {e}")
        traceback.print_exc()
        return url, depth - 1, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek
  

    
# Define the starting URL
start_url = my_start_url

# Set the maximum depth for crawling
max_crawl_depth = 15
my_seek = False
seek_url = ""

if all_page_data == {}:
    my_page_data = {"name": start_url, "children": [], "value" : 0, "path":"Partner", "branch": True, "seek": False, "last_url": ""}
else:
    my_page_data = all_page_data
    my_seek = True
    seek_url = my_page_data["last_url"]

if len(seek_url) < 10:
    seek_url = my_start_url
    consecutive_urls = my_start_url

# Create a timer thread to save data every few minutes (10)
# Usage
rt = RepeatTimer(600.0)
rt.start()

# Start crawling and add the root page to the data

next_url = seek_url
max_depth=max_crawl_depth
all_page_data=my_page_data
seek=my_seek
depth = 0
crawled = True


consecutive_urls = []
last_url = ""
maxtries = 5
tries = 0
while (len(queue_urls) > 0 and not esc_pressed):
    
            
    next_url, depth, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek = crawl_page(next_url, depth, max_depth, all_page_data, crawled_urls, queue_urls, session_cookies, crawled, seek)
    if last_url == next_url:
        if next_url in consecutive_urls:
                
                for url in consecutive_urls:
                    if url == next_url:
                        tries += 1
                        print("Try:", tries)
                        consecutive_urls.append(next_url)
                if tries >= maxtries:
                    # if url not in crawled_urls:
                    #         crawled_urls.append(url)
                    queue_urls = remove_from_master_list(next_url, queue_urls)
                    mean_urls = update_master_list(next_url, mean_urls)
                    if len(queue_urls) > 0: 
                        next_url = queue_urls[-1]
                    else:
                        print("No more queue.")
                        break
        else:
                consecutive_urls = []
                consecutive_urls.append(next_url)
    
    last_url = next_url

rt.cancel()
print("1")
# Save the root_page_data to a JSON file
my_save_to_json(all_page_data)
print("2")
# Unregister the event handler when you're done
keyboard.unhook_all()
print("3")
exit()
print("4")