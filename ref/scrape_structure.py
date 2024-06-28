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


# import copy
random.seed(int(time.time()))

# Example JSON data with cookies
cookie_json = [
{
    "domain": ".alarm.com",
    "expirationDate": 1731983377.227883,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GA1.1.674450394.1696855247",
    "id": 1
},
{
    "domain": ".alarm.com",
    "expirationDate": 1731461536.987283,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_ga_9RM70S4LW0",
    "path": "/",
    "sameSite": "unspecified",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GS1.1.1696901519.1.1.1696901536.0.0.0",
    "id": 2
},
{
    "domain": ".alarm.com",
    "expirationDate": 1731983377.251271,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_ga_C28495QEHH",
    "path": "/",
    "sameSite": "unspecified",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "GS1.1.1697423377.10.0.1697423377.0.0.0",
    "id": 3
},
{
    "domain": ".alarm.com",
    "expirationDate": 1704677521,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_gcl_au",
    "path": "/",
    "sameSite": "unspecified",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1.1.610826006.1696901521",
    "id": 4
},
{
    "domain": ".alarm.com",
    "expirationDate": 1717764116.367764,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_zitok",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "64dadd8d1cfd1e458b201683204091",
    "id": 5
},
{
    "domain": ".alarm.com",
    "expirationDate": 1728478469.376133,
    "hostOnly": False,
    "httpOnly": False,
    "name": "adc_e_alarm_locale",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "en-us",
    "id": 6
},
{
    "domain": ".alarm.com",
    "expirationDate": 1710931571,
    "hostOnly": False,
    "httpOnly": False,
    "name": "adc_e_cookie_banner",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "True",
    "id": 7
},
{
    "domain": ".alarm.com",
    "expirationDate": 1728478469.376268,
    "hostOnly": False,
    "httpOnly": False,
    "name": "adc_e_donottrack",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "False",
    "id": 8
},
{
    "domain": ".alarm.com",
    "expirationDate": 1728523936.65351,
    "hostOnly": False,
    "httpOnly": False,
    "name": "adc_e_gpc_enabled",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "False",
    "id": 9
},
{
    "domain": ".alarm.com",
    "expirationDate": 1728478469.376211,
    "hostOnly": False,
    "httpOnly": False,
    "name": "adc_e_origin_locale",
    "path": "/",
    "sameSite": "strict",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "en-us",
    "id": 10
},
{
    "domain": ".alarm.com",
    "expirationDate": 1731864150.979222,
    "hostOnly": False,
    "httpOnly": True,
    "name": "loggedInAsRep",
    "path": "/",
    "sameSite": "unspecified",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1",
    "id": 11
},
{
    "domain": ".alarm.com",
    "expirationDate": 1728926547.024508,
    "hostOnly": False,
    "httpOnly": True,
    "name": "twoFactorAuthenticationId",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "7AFC7AA2847E0153B35257CB84F6134D8948739805A14C05031007F63AD28B36",
    "id": 12
},
{
    "domain": ".answers.alarm.com",
    "expirationDate": 1697865751.520917,
    "hostOnly": False,
    "httpOnly": True,
    "name": "authtoken",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "\"eyJhbGciOiJIUzI1NiIsImtpZCI6Imh0dHBzOi8vbWluZHRvdWNoLmNvbS9hdXRodG9rZW4vZGVraS8xNzA1ODAzIiwidHlwIjoiSldUIn0.eyJhdWQiOiJodHRwczovL2Fuc3dlcnMuYWxhcm0uY29tIiwiZXhwIjoxNjk3ODY1NzUyLCJpYXQiOjE2OTczMDQxNTIsInN1YiI6MTcwNTgwMywiaXNzIjoiaHR0cHM6Ly9hbnN3ZXJzLmFsYXJtLmNvbS9AYXBpL2Rla2kvc2VydmljZXMvMyJ9.SkWkFmL1SEOWwvxwOxWoOs5dalhcch7uu8CCogWdJMA\"",
    "id": 13
},
{
    "domain": ".answers.alarm.com",
    "expirationDate": 1731415245.412428,
    "hostOnly": False,
    "httpOnly": True,
    "name": "dekisession",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "\"ODFjZmM4MTMtZDUyMi00ZTQ5LWE1NTQtZDhlMmJlMDBkZTVifDIwMjMtMTAtMDlUMTI6NDA6NDQ=\"",
    "id": 14
},
{
    "domain": "answers.alarm.com",
    "hostOnly": True,
    "httpOnly": True,
    "name": "mtwebsession",
    "path": "/",
    "sameSite": "unspecified",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "bc09720ab09cf1096d676a99f1539e93",
    "id": 15
}
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
last_url = ""

all_page_data = {}
urls = []
LOAD_URLS = False

data_lock = threading.Lock()  # Create a lock for data access

# Function to save your data
def save_data():
    with data_lock:
        with open('data.json', 'w') as file:
                global last_url
                my_page_data["last_url"] = last_url
                timestamp = datetime.now().strftime("%Y%m%d%H%M")
                filename = f"data{timestamp}.json"
                filename2 = f"urls{timestamp}.json"
                save_to_json(my_page_data, filename)
                save_to_json(urls, filename2)
    

lines_to_display = 3

print("Attempting to load json data...")

# Check if a filename argument was provided
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    # Use a default filename if no argument is provided
    filename = 'all_page_data.json'

def count_nodes(node):
    if "children" in node:
        count = 1  # Initialize with 1 to count the current node
        for child in node["children"]:
            count += count_nodes(child)
        return count
    else:
        return 1  # Leaf node

if (LOAD_URLS):
    try:
        with open('urls.json', 'r') as file:
            urls = json.load(file)
            print("Avoiding these urls:")
            # Get random lines
            random_lines = random.sample(urls, lines_to_display)
            print(GREEN+str(len(urls))+RESET+" urls loaded from urls.json")
            print("...")
            for line in random_lines:
                print(line)
            print("...")

    except:
        # Handle the exception (e.g., print an error message, set default values, or take appropriate action)
        print("Failed to load JSON urls")
        
        urls = [] #also a name_blacklist to prevent unnecessary soup calls

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
    "MyBinder MyBinder",
    "Support ReleaseNotes",
    "OperationAlerts OperationsAlertsDashboard"
]
phrase_blacklist = [
    "#",
    "deki",
    "Special:",
    "MyBinder",
    "ReleaseNotes"
    "Skilljar.aspx",
    "mindtouch.com"
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

def on_esc(event):
    global esc_pressed
    if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
        esc_pressed = True

keyboard.on_press_key('esc', on_esc)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    with open('urls.json', 'w') as file:
        filtered_links = list(set(urls))
        json.dump(filtered_links, file)


def my_save_to_json(my_page_data):
    global last_url
    my_page_data["last_url"] = last_url
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
    global total, last_url

    target_path = target_url.replace("https://", "")
    parts = target_path.split('/')
    if len(parts) > 1:
        term_part = parts[-2]
    elif len(parts) > 0:
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
        #  current_node = {'name': parts[0], "path": "answers.alarm.com", 'children': []}
        #  all_page_data = current_node
        exit("No Data")
        # return None, None, my_buffer, False
    # print(target_path)
    if "url" in current_node:
        if current_node["url"] is target_url:
            return current_node, current_node, current_node    
    if current_node["path"] == target_path:
        return current_node, current_node, current_node

    for part in parts:
        # Find the child node with the current part and path as its attributes
        child_node = None
        # print(current_node)
        # if "children" in current_node:
        index = 0
        for node in current_node["children"]:
            if "path" in node:
                my_parts = '/'.join(parts[:parts.index(part) + 1])
                if node['path'] == my_parts:
                    # print(BLUE + 'Path found: ' + node["path"] + GREEN, '/'.join(parts[:parts.index(part) + 1]) + RESET)
                    if part is term_part:
                        print(BLUE + 'Path found: ' + my_parts + RESET)
                    parent_branch = child_node #couldn't hurt
                    child_node = node
                    break
            index += 1


        # Make some branches
        if child_node is None:
            path_node = '/'.join(parts[:parts.index(part) + 1])
            my_url = "https://" + path_node
            child_node = {'name': path_node, 'path': path_node, 'children': [], "value": parts.index(part), "crawled": False, "url": my_url, "branch" : True}
            if my_url not in urls and my_url != "https://answers.alarm.com":
                urls.append(my_url)
            print(YELLOW + 'Adding... ' + child_node["path"] + RESET)
            current_node["children"].append(child_node)
            total += 1
            

        # Move to the child node and continue processing the URL
        if 'children' in current_node:
            parent_branch = current_node
            current_node = current_node["children"][-1]
        else: #couldn't hurt
            path_node = '/'.join(parts[:parts.index(part) + 1])
            my_url = "https://" + path_node
            child_node = {'name': path_node, 'path': path_node, 'children': [], "value": parts.index(part), "crawled": False, "url": my_url, "branch" : False}
            if my_url not in urls and my_url != "https://answers.alarm.com":
                urls.append(my_url)
            print(GREEN + 'Adding... ' + child_node["path"] + RESET)
            current_node["children"].append(child_node)
            total += 1
            if parent_branch is None: parent_branch = current_node
            return current_node, parent_branch, my_buffer

        # Check if the current path matches the target path
        if current_node['path'] == target_path:
            found_node = current_node
            return found_node, parent_branch, my_buffer
    
    
    return found_node, parent_branch, my_buffer

def is_valid_url(url):
    # Regular expression pattern to match valid URLs with "https://answers.alarm.com"
    url = str(url)

    # Remove the pound symbol '#' if it exists in the URL
    url = url.replace('#', '')

    pattern = r'^https://answers.alarm.com\S+'
    res = re.match(pattern, url) is not None
    if res is None:
        res = "https://answers.alarm.com"
    return res


def crawl_page(url, depth=1, max_depth=3, all_page_data=[], session_cookies=session_cookies, crawled=False, seek=False):
    global valid_pages, esc_pressed, urls, name_blacklist, iteration, total, deleted
    global seek_url, last_url
    parent_branch = None

   
    if depth > max_depth or esc_pressed: #or (url in urls):
        return False, all_page_data
    iteration += 1
    exists = False
    
    # url, all_page_data = find_uncrawled(all_page_data, url, all_page_data)
    
    try:
        # Send an HTTP GET request with your session cookies
        
        response = requests.get(url, cookies=session_cookies)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Create a dictionary to store the hierarchical data
            page_data = {"name": url}


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
            
            # Append the page_data to the all_page_data array
            
            page_data['value'] = depth #we have to set the value to something
            links = soup.find_all('a')
            #all_page_data.append(page_data)
            node = None

                        # Create a list to store the links
            link_list = []

            # Iterate through the links and extract their attributes
            for lk in links:
                link_list.append(lk.get('href'))

            # Function to validate URLs

            # Filter URLs
            link_list = [eurl for eurl in link_list if is_valid_url(eurl) and all(phrase not in eurl for phrase in phrase_blacklist)]

            urls_set = set(urls)
            my_links_set = set(link_list)
            unique_urls_set = my_links_set - urls_set
            link_list = list(unique_urls_set)
  
            if 'og:url' in page_data['meta_tags']:
                url = page_data['meta_tags']['og:url']
            page_data['url'] = url
            if not seek:
                if page_data['name'] in name_blacklist: 
                    if page_data['url'] not in urls and page_data['url'] != "https://answers.alarm.com": urls.append(page_data["url"])
                    return False, all_page_data
                adding_parts = True
                
                node, parent_branch, all_page_data = generate_branches(url, all_page_data)
                if node is None:
                    return False, all_page_data
                if 'children' not in node:
                    node.children = []
                exists = False
                for kid in node["children"]:
                    if 'path' in kid:
                        if kid["name"] == page_data["name"]: #all this convoluted mess is to prevent articles from being added multiple times
                            if "branch" in kid:
                                if not kid["branch"] and not node["branch"]: #pretty much guarantees its an end-cap if we delete it
                                    node["children"].remove(kid)
                                    total -=1
                                    deleted += 1
                                    print(RED+"Uh, Scratch that..."+RESET)
                                else:
                                    print(YELLOW+"Not really supposed to be seeking branches.."+RESET)
                                    exists = True
                                    my_url = page_data['url']
                                    if page_data['url'] not in urls and page_data['url'] != "https://answers.alarm.com":
                                        print("Removing.. "+my_url)
                                        urls.append(page_data["url"])
                                    # return False, all_page_data
                if not exists:
                    page_data["path"] = url
                    page_data["children"] = []
                    page_data["crawled"] = crawled
                    page_data["links"] = link_list
                    page_data["branch"] = False
                    valid_pages += 1
                    node["children"].append(page_data)
                    total += 1
                    # node.append(page_data)
                    if page_data["url"] != "https://answers.alarm.com": urls.append(page_data["url"])
                    last_url = page_data["url"]
            # else:
                # if exists:
                #     return False, all_page_data
            
            # my_save_to_json(all_page_data)
            my_val = page_data['value']
            my_name_blacklisted = len(urls)
            my_pages = valid_pages + total
            
            print("Iteration: "+BLUE+f"{iteration}"+RESET+" Total/Souped Nodes: "+GREEN+f"{my_pages}"+BLUE+'/'+GREEN+f"{valid_pages}"+RESET+" Depth: "+YELLOW+f"{my_val}"+RESET+" BL urls: "+RED+f"{my_name_blacklisted}"+RESET+" Deleted Nodes: "+RED+f"{deleted}"+RESET)
            if (len(last_url) > 4):
                my_last_url = ' ... '+last_url[-int(len(last_url) / 4):]
                print(f"(last_url)({my_last_url})")
            # Parse and follow links on the page
            
            
            # if node is None:
            #     print("None??")
            #     return False, all_page_data
            # print(link_list)
            # print(seek, depth)
            if (seek):
                print(seek_url)
                if '/' in seek_url:
                    parts = '/'.split(seek_url)
                else:
                    parts = seek_url
                print (parts)
            for next_url in link_list:
                if next_url:
                    skip = False
                    for bl in phrase_blacklist:
                        if bl in next_url: skip = True
                    # if next_url not in urls and not skip:
                    if not skip:
                        # if next_url == link_list[-1]: save_node = 
                        # time.sleep(1)
                        # print(seek_url, next_url)
                        # print (seek_url, next_url)
                        if (seek):
                        # if (seek and (seek_url in next_url)):
                            for part in reversed(parts):
                                if part in next_url or parts[-1] is part:
                                    print (part, next_url)
                                    if parts[-1] is part:
                                # if next_url in seek_url or seek_url in next_url:
                                        if part not in parts:
                                            print(YELLOW+"Can't find starting point, finding lower-right-most child in the tree..."+RESET)
                                            while "child" in my_node:
                                                my_node = my_node[children][-1]
                                                if "url" in my_node:
                                                    if len(my_node["url"]) > 5:
                                                        next_url = url
                                        else:
                                            print(GREEN+"Starting where left off:"+RESET)
                                            print(seek_url)
                                        seek = False
                                    child_page, all_page_data = crawl_page(next_url, depth=depth + 1, max_depth=max_depth, all_page_data=all_page_data, session_cookies=session_cookies, crawled=crawled, seek=seek)
                        elif (not seek and next_url not in urls):
                            child_page, all_page_data = crawl_page(next_url, depth=depth + 1, max_depth=max_depth, all_page_data=all_page_data, session_cookies=session_cookies, crawled=crawled, seek=seek)
                            # print('hi')
                    # if child_page:
                    #     if 'children' not in node:
                    #         node["children"] = []
                    #     node["children"].append(child_page) add total
                    if (esc_pressed): return parent_branch, all_page_data
            
            return False, all_page_data
                    

    except Exception as e:
        print(f"Error while crawling {url}: {e}")
        traceback.print_exc()
    
# Define the starting URL
start_url = "https://answers.alarm.com/"

# Set the maximum depth for crawling
max_crawl_depth = 15
my_seek = False

if all_page_data == {}:
    my_page_data = {"name": start_url, "children": [], "value" : 0, "path":"answers.alarm.com", "branch": True, "seek": False, "last_url": ""}
else:
    my_page_data = all_page_data
    my_seek = True
    seek_url = my_page_data["last_url"]
    if len(seek_url) < 10:
        seek_url = "https://answers.alarm.com"
        last_url = "https://answers.alarm.com"
    seek_url = seek_url.replace("https://", "")
    # try:
    #     start_url = str(random.sample(urls, 1))
    # except:
    #     start_url = start_url


# Create a timer thread to save data every 2 minutes
timer = threading.Timer(120.0, save_data)  # 120.0 seconds = 2 minutes

# Start the timer
timer.start()

# Start crawling and add the root page to the data
root_page, all_page_data = crawl_page(start_url, max_depth=max_crawl_depth, all_page_data=my_page_data, seek=my_seek)

# Save the root_page_data to a JSON file
my_save_to_json(all_page_data)

# Unregister the event handler when you're done
keyboard.unhook_all()
timer.cancel()