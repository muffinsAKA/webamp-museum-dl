# Webamp Skin Downloader

import requests
import json
import time
import pandas as pd
import tqdm

# Set pandas column width to be as long as needed to display full URL
pd.set_option('display.max_colwidth', None)

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
print(f'{total_skins} total skins found')

# Create future home of all da links
link_table = pd.DataFrame()

# Run query for 1000 skins (api limit) and offset the next request by 1000
for i in tqdm.tqdm(range(0, total_skins, 1000), desc="Gathering skin database"):
    
    # Create query for current offset of skins
    QUERY = (
    "query {" + '\n'
  f"skins(first: 1000, offset: {i})" + "{" + '\n'
    "nodes {" + '\n'
      "filename" + '\n'
      "download_url" + '\n'
    "}" + '\n'
  "}" + '\n'
"}"
    )

    # Request query
    r = requests.post(BASE_URL + QUERY)
    
    # Load query response into json
    json_data = json.loads(r.text)

    # Identify the skins list in the json
    df_data = json_data['data']['skins']['nodes']

    # Append load new skins into a pandas dataframe
    df_new = pd.read_json(json.dumps(df_data) , orient='list')

    # Append the newest skins dataframe with the overall link_table dataframe
    link_table=pd.concat([df_new,link_table], ignore_index=True)

    # Sleep for 2 seconds to not spam
    time.sleep(2)

 # Find the total length of the skins (should be equal to the total count but who knows!)
links_total = len(link_table)
print(links_total)

# Set your headers, kids. You never know.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

# For each of the skins, send a download request and auto-rename to the skin name
for i in tqdm.tqdm(range(links_total), desc="Downloading Skins"):
  filename = link_table.iloc[i]['filename']
  download_url = link_table.iloc[i]['download_url']
  print(download_url)
  r = requests.get((download_url), headers=headers, allow_redirects=True)
  open(f'{filename}'.replace('zip', ''), "wb").write(r.content)
  time.sleep(1)