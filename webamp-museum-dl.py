# Webamp Skin Downloader

import requests
import json
import time
from tqdm import *
import os
import math
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import sys

# VARIABLES
md5dupes = 0
urls = []
fns = []
types = []
md5pool = []
new_md5pool = []
name_pool = []
skins_db = {
   "skins": [],
   "dupes": [],
   "config": {
  
   }
  }


art = r"""
                        ::                        
                      .*@@#:               .      
                    .*@#:.*@#:          :+%@      
                  .*@#:    .*@#:     -*@@@@@      
                .*@#:        .*@#-=#@@@@#.@@      
              .*@*.           :*@@*+#@#: -@@      
            .*@#:          -*@@*-.+@%: .#@*       
          .*@#:        .=#@%+:  =@%-  +@%:        
        .*@#:       :+%@*-.   -%@=  +@%@#:        
      .*@*.      -*@%+:     :%@@#++@@= .+@#:      
    .*@#:    .=#@#=.          .:-=*@@@@. .*@#:    
  .*@#:     #@@@@@@@@@@@%=      :*@@*@@.   .*@#:  
 =@@=       @@:    .=%@+.   .=*@%+:  @@.     :@@* 
  :#@*.     @@.   =%@+   :+%@#=.   :+@@.   .+@%-  
    :#@*.   @@@@@@@+  :+%@*-    :*@@*-    +@%-    
      :#@+.   -%@+.-*@@*-    -*@@+:     =@%-      
        :#@*=%@#+#@#+:   :+#@#=.     .+@%-        
          *@@@@@#-    :+@@*-       .+@%-          
        -%@@@*-    -*@@*:         +@%-            
      :%@%+:    =#@%+:          =@%-              
      %@-   :+#@##@*.        .+@%-                
      %@.-*@@*-   :#@*.    .+@%-                  
      %@@%+:        :#@*..+@%-                    
      #+:             :#@@%-                      

                                                         
  [ webamp skin downloader v0.00001 alpha ]
                          by muffinsAKA"""

# print logo
print("\033[38;5;208m" + art + "\033[0m")

print('')
input("[ Press Enter to continue... ]")
print('')
print("\033[38;5;208m" + 'Is this your first time downloading skins using this tool?')
print("\033[0m" + '1.) Yes     2.) No')
first_time = int(input())
if first_time == 1:
  print('')
  print("\033[38;5;208m" + 'Ok cool.')
  time.sleep(1)
if first_time == 2:
  print('')
  print("\033[38;5;208m" + 'Did you move anything or is it all still in the same folder as this app?')
  print("\033[38;5;208m" + 'Like your skins folder, your database file.....those things.')
  print("\033[0m" + '1.) It\'s all still here     2.) I moved it')
  file_location = int(input())
  if file_location == 1:
    print('')
    print("\033[38;5;208m" + 'Thank god. Alright moving on.')
    time.sleep(1)
    input('[ Press any key to move on ]')
  if file_location == 2:
    print('')
    print("\033[38;5;208m" + 'Well put it back. I\'m not building a whole customized folder flow.')
    time.sleep(2)
    print(r"""It should look like this:

          [Script Folder]
                |
                |
                [Skins]
                |  -> [Modern]
                |  -> [Classic]
                |
                webamp-museum-dl.py
                webamp_skins_db.json""")
    print('')
    time.sleep(2)
    input("\033[38;5;208m" + 'lmk when you put that shit back')

print('')
print("\033[38;5;208m" + 'How many downloads do you want going at the same time?')
print("\033[0m" + '1.) As many as possible    2.) Custom')
dl_amt = int(input())
if dl_amt == 1:
  cpus = cpu_count()
  dl_custom = cpus - 1
  print('')
  print("\033[38;5;208m" + 'You got it, pal. See you on the other side.')
  time.sleep(1)
  print('3')
  time.sleep(1)
  print('2')
  time.sleep(1)
  print('1.5')
  time.sleep(1)
  print("\033[38;5;208m" + 'haha jk')
  time.sleep(1)
if dl_amt == 2:
  time.sleep(1)
  cpus = cpu_count()
  max_dl = cpus - 1
  print('')
  print("\033[38;5;208m" + f'Hit me with it. How many downloads at a time? (MAX: {max_dl})')
  dl_custom = int(input())
  if dl_custom <= max_dl:
    print('')
    print("\033[38;5;208m" + f'ok {dl_custom} at a time. have fun out there, champ')
    time.sleep(3)
  else:
      print('')
      print("\033[38;5;208m" + f'buddy. pal. {dl_custom}? what is this?')
      time.sleep(3)
      print('')
      print("\033[38;5;208m" + 'One more shot.')
      time.sleep(1)
      print('')
      print("\033[38;5;208m" + f'Hit me with it. How many downloads at a time? (MAX: {max_dl})')
      dl_custom = int(input())
      if dl_custom <= max_dl:
        print("\033[38;5;208m" + 'You got it, pal. See you on the other side.')
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(3)
        print('1.5')
        time.sleep(1)
        print("\033[38;5;208m" + 'haha jk')
        time.sleep(1)
      else:
        print("\033[38;5;208m" + 'goodbye.')
        time.sleep(5)
        sys.exit(1)

# FUNCTIONS
# Download function that extracts the tuple to create variables
def download_url(inputs):
    
  url, fn, type = inputs[0], inputs[1], inputs[2]

  fn = fn.replace('/','-')

  # If there's no url, add it to the number of missing show urls
  if url:

    print(url)
    # if the filename exists in the folder already
    if fn in os.listdir(classic_path) or os.listdir(modern_path):

      filename_split = os.path.splitext(fn)
      fn = filename_split[0] + '_DUPE' + filename_split[1]
    
    if type:
      fn = os.path.join(classic_path + '/' + fn)
    
    if not type:
      fn = os.path.join(modern_path + '/' + fn)
        
    # Request the url for download and then write to file
    with requests.get(url, stream=True) as r:
      r.raise_for_status()

      with open(f'{fn}', 'wb') as f:
          fn_short = os.path.split(fn)
          
          pbar = tqdm(total=int(r.headers['Content-Length']),
                      desc=f"Downloading {fn_short[1]}",
                      unit='MiB',
                      unit_divisor=1024,
                      unit_scale=True,
                      dynamic_ncols=True,
                      colour='#FEB60C',
                      mininterval=3
                      )
          
          for chunk in r.iter_content(chunk_size=1024):
              if chunk:
                  f.write(chunk)
                  pbar.update(len(chunk))


# Function that opens the multiple download_url functions
def download_parallel(args):
    cpus = cpu_count()
    ThreadPool(dl_custom).map(download_url, args)

# Save db from last time
def save_db():
  with open('webamp_skins_db.json', 'w', encoding='utf-8') as f:
    skins_db['dupes'] = md5pool
    skins_db['config']['total_skins'] = len(skins_db['skins'])
    f.write(json.dumps(skins_db))

# Make directory/files for skins/cfg
print('')
print('Creating folders for skins')
time.sleep(1)
skins_dir = "skins"
classic_dir = "/classic"
modern_dir = "/modern"

# setup directory structures
curdir = os.getcwd()
path = os.path.join(curdir, skins_dir)
classic_path = os.path.join(path + classic_dir)
modern_path = os.path.join(path + modern_dir)

if not os.path.exists(path):
   os.mkdir(path)
   print('')
   print('"/Skins" folder created')
   time.sleep(1)

if not os.path.exists(classic_path):
  os.mkdir(classic_path)
  print('')
  print('"./Classic" folder created')
  time.sleep(1)

if not os.path.exists(modern_path):
   os.mkdir(modern_path)
   print('')
   print('"./Modern" folder created')
   time.sleep(1)

# if there's a cfg file in the directory, load it
if os.path.exists(curdir + '/webamp_skins_db.json'):
  load_cfg = True
  print('')
  print('Previous database found!')
  time.sleep(2)
else:
   load_cfg = False
   print('')
   print('No previous database found. Starting fresh~')
   time.sleep(2)

if load_cfg:
  with open('webamp_skins_db.json', 'r',encoding='utf-8') as c:
    skins_db = json.load(c)
    c.close()
  loaded_skins_amt = len(skins_db['skins'])


# Set base query URL
BASE_URL = 'https://api.webamp.org/graphql?query='

# Create query for total number of skins available
TOTAL_QUERY = """query {
  skins {
    count
    }
  }"""
  
   
# Send total skins query
t = requests.post(BASE_URL + TOTAL_QUERY)

# Load total skins into variable as json
total_data = json.loads(t.text)

# Identify the total count from the json
total_skins =  total_data['data']['skins']['count']

# Announce skin count total
print('')
print(f'> {total_skins} total skins available on webamp.org')
time.sleep(1)

# if database detected, announce number of skins in database
if load_cfg:
  print('')
  print(f'> {loaded_skins_amt} currently in your database')
  time.sleep(1)

  # if this number is equal to the amount of skins available on webamp.org, exit
  if loaded_skins_amt == total_skins:
     print('')
     print('No more skins to get!')
     time.sleep(1)
     print('Let\'s get outta here, kid.')
     time.sleep(3)
     sys.exit()

# if database detected, calculate how to prepare query request based on existing skins
if load_cfg:

  # grab offset from config 
  offset_amt = skins_db['config']['total_skins']

  # number of new skins available 
  first = total_skins - loaded_skins_amt

  # if number of new skis is less than or equal to 1,000 only one request is required (due to 1000 limit per request)
  if first <= 1000:
    db_range = trange(0, 1, desc="Updating skins database", colour="#FEB60C")

  # if more than 1000 requests calculate how many requests will be needed
  else:
    db_range = trange(0, math.ceil(first/1000), desc="Updating skins database", colour="#FEB60C")
  
# if no database, send requests until max # of skins is gathered
if not load_cfg:
  db_range = trange(0, math.ceil(total_skins/1000), desc="Getting skins database", colour="#FEB60C")
  offset_amt = 0
   

# Run query for 1000 skins (api limit) and offset the next request by 1000
for i in db_range:

  QUERY = (
    "query {" + '\n'
  f"skins(first: 1000, offset: {offset_amt})" + "{" + '\n'
    "nodes {" + '\n'
      "filename(normalize_extension: true)" + '\n'
      "download_url" + '\n'
      "__typename" + '\n'
      "md5" + '\n'
    "}" + '\n'
  "}" + '\n'
  "}"
    )

  # Request query
  r = requests.post(BASE_URL + QUERY)
  
  # Load query response into json
  json_data = json.loads(r.text)

  # Identify the skins list in the json
  fresh_skins = json_data['data']['skins']['nodes']
  
  # Append new skins
  for i in range(len(fresh_skins)):
    if load_cfg:
      for s in range(len(skins_db['skins'])):
        if fresh_skins[i]['md5'] == skins_db['skins'][s]['md5']:
          skins_db['skins'].pop([s])
          md5dupes = md5dupes + 1
    skins_db['skins'].append(fresh_skins[i])
    
  # set offset amt for updated runs with more than one query needed
  if load_cfg:
    if first > 1000:
      offset_amt = offset_amt + len(fresh_skins)

  # Increase offset for next round on a fresh run
  if not load_cfg:
     offset_amt = offset_amt + 1000




# Find the total amount of skins that are new as well as what's currently in the database
new_links_total = len(fresh_skins)
links_total = len(skins_db['skins'])

# if database found, print how many new skins are available
if load_cfg:
  print('')
  print(f'{new_links_total} new skins to download')
  time.sleep(1)

# Set your headers, kids. You never know.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

# set the range based on whether or not previous skins exist
if load_cfg:
  sort = trange(0, new_links_total-1, desc="Sorting Skins", colour="#FEB60C")

if not load_cfg:
  sort = trange(links_total, desc="Sorting Skins", colour="#FEB60C")


print('')
print(f'{md5dupes} duplicates removed')
time.sleep(2)



# For each of the skins, send a download request and auto-rename to the skin name
for i in sort:
  filename = skins_db['skins'][i]['filename']
  typename = skins_db['skins'][i]['__typename']
  dl_link = skins_db['skins'][i]['download_url']
  
  # if type = true, skin is classic.  if false, modern.
  if typename == 'ClassicSkin':
    types.append(True)
  else:
    types.append(False)

  # add download link and filenames to separate lists
  if dl_link:
    urls.append(dl_link)
    fns.append(filename)

    
# add urls, filenames, and types to a tuple
inputs = zip(urls, fns, types)

# call the save database function. used for resuming next time and requiring less queries. also saves the offset of where you left off.
save_db()

# send all of info needed as a tuple to the download function
download_parallel(inputs)

# if database was detected, announce total of new skins downloaded
if load_cfg:
  print('')
  print(f'{new_links_total} new skins downloaded')

# if no database, announce total of skins downloaded
if not load_cfg:
   print('')
   print(f'{links_total} skins downloaded')



