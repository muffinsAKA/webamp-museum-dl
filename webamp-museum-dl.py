# Webamp Skin Downloader

import requests
import json
import time
import pandas as pd
from tqdm import *
import os
import math
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import sys

# VARIABLES
urls = []
fns = []
types = []
md5_pool = []
name_pool = []
skins_db = {
   "skins": [
   
   ],
   "dupes": [
   
   ],
   "config": [
   
   ]
  }
fn_dupes = {
   "dupes": [
   
   ]
  }

cfg = {
   "config": [
   
   ] 

  }

# FUNCTIONS
# Download function that extracts the tuple to create variables
def download_url(inputs):
    
    url, fn, type = inputs[0], inputs[1], inputs[2]

    fn.replace('/','-')
    
    # If there's no url, add it to the number of missing show urls
    if url:
  
      # Request the url for download and then write to file
      with requests.get(url, stream=True) as r:
        r.raise_for_status()
        
        if type:
          fn = os.path.join(classic_path + '/' + fn)
        
        if not type:
           fn = os.path.join(modern_path + '/' + fn)

        with open(f'{fn}', 'wb') as f:
            pbar = tqdm.tqdm(total=int(r.headers['Content-Length']),
                        desc=f"Downloading {fn}",
                        unit='MiB',
                        unit_divisor=1024,
                        unit_scale=True,
                        dynamic_ncols=True,
                        colour='#ea0018',
                        mininterval=3
                        )
            
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


# Function that opens the multiple download_url functions
def download_parallel(args):
    cpus = cpu_count()
    ThreadPool(cpus - 1).map(download_url, args)

# Function to check for duplicate files
def md5_check(md5):
    
  # Checks if md5 is in the pool and if it is present delete the skin
  if md5 in md5_pool:
      skins_db.pop([i])
      return True
  else:
      md5_pool.append(md5)
      return False
  
# Function to check for duplicate filenames
def namecheck(filename):

  if filename in name_pool:
      filename_split = os.path.splitext(filename)
      filename = filename_split[0] + '_DUPE' + filename_split[1]
      return True
  else:
      name_pool.append(filename)
      return False

# Save db from last time
def save_db():
  with open('webamp_skins_db.json', 'w', encoding='utf-8') as f:
    
    for d in fn_dupes:
       skins_db['dupes'].append(fn_dupes[d])
    
    cfg['config'].append(offset_amt)
    cfg['config'].append(total_skins)
    f.write(json.dumps(skins_db))

    
# def save_cfg(): 
#   cfg_save = {
#   'offset': offset_amt,
#   'total-skins': total_skins            
#   }
#   with open('webamp.cfg', 'w', encoding='utf-8') as w:
#     w.write(json.dumps(cfg_save))
#     print('cfg file created')
#     w.close()       

         

# Make directory/files for skins/cfg
skins_dir = "skins"
classic_dir = "/classic"
modern_dir = "/modern"

curdir = os.getcwd()
path = os.path.join(curdir, skins_dir)
classic_path = os.path.join(path + classic_dir)
modern_path = os.path.join(path + modern_dir)

if not os.path.exists(path):
   os.mkdir(path)
   print('"/Skins" folder created')

if not os.path.exists(classic_path):
  os.mkdir(classic_path)
  print('"./Classic" folder created')

if not os.path.exists(modern_path):
   os.mkdir(modern_path)
   print('"./Modern" folder created')

# if there's a cfg file in the directory, load it
if os.path.exists(curdir + '/webamp_skins_db.json'):
  load_cfg = True
else:
   load_cfg = False

if load_cfg:
  with open('webamp_skins_db.json', 'r',encoding='utf-8') as c:
    skins_db = json.load(c)
    c.close()
  loaded_skins_amt = len(skins_db['skins'])
  
# if cfg file exists, load it into 'cfg' as list for use
if load_cfg:
  cfg = skins_db['config']


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
print(f'{total_skins} total skins available online')

if load_cfg:
  print(f'{loaded_skins_amt} currently in your database')
  if loaded_skins_amt == total_skins:
     print('No more skins to get!')
     sys.exit()

if load_cfg:
  db_range = range(loaded_skins_amt, math.ceil(total_skins/1000))
  offset_amt = cfg['offset']

if not load_cfg:
  db_range = range(0, math.ceil(total_skins/1000))
  offset_amt = 0
   

# Run query for 1000 skins (api limit) and offset the next request by 1000
for i in trange(db_range, desc="Getting skins database"):

  # Create query for current offset of skins
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
  if load_cfg:
    for s in fresh_skins:

      skins_db['skins'].append([s])


  if not load_cfg:
    for s in fresh_skins:
       
      skins_db['skins'].append(s)


  # Increase offset for next round
  offset_amt = offset_amt + 1000

# Find the total length of the skins (should be equal to the total count but who knows!)
links_total = len(skins_db['skins'])

if load_cfg:
  print(f'{links_total} new skins to download')

# Set your headers, kids. You never know.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

# For each of the skins, send a download request and auto-rename to the skin name
for i in trange(links_total, desc="Sorting Skins"):
  
  filename = skins_db['skins'][i]['filename']
  md5 = skins_db['skins'][i]['md5']
  typename = skins_db['skins'][i]['__typename']
  dl_link = skins_db['skins'][i]['download_url']

  # if type = true, skin is classic.  if false, modern.
  if typename == 'ClassicSkin':
    types.append(True)
  else:
    types.append(False)

  # if md5 matches list, duplicate!
  if md5_check(md5):
      print(f'Skipping duplicate: {filename} ')
      dl_link = ''

  if dl_link:
    urls.append(dl_link)
    fns.append(filename)

  if load_cfg:
    if filename not in saved_db['dupes'].keys():      
      fn_dupes['dupes'] = filename

  if not load_cfg:
    fn_dupes['dupes'] = filename
    

  # after all links have been processed...
  if i == links_total-1:
    inputs = zip(urls, fns, types)
    save_db()
    download_parallel(inputs)

if load_cfg:
  total_new_skins = loaded_skins_amt + links_total
  print(f'{total_new_skins} new skins downloaded')

if not load_cfg:
   print(f'{links_total} skins downloaded')



