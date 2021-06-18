import requests
from requests import exceptions
import cv2
import os
import argparseparser = argparse.ArgumentParser()
parser.add_argument("-q","--query", required=True, help='enter search term')
args = vars(parser.parse_args())HP_initial_offset = 0
HP_group_size = 50
currentOffset = HP_initial_offsetaccesskey = '1540554f52b34f48ab49ae7052c6804d'
search_url = "https://api.bing.microsoft.com/v7.0/images/search"
# url for web search: "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": accesskey}myexceptions = {IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, 
                exceptions.ConnectionError, exceptions.Timeout}search_term = args["query"]
params = {"q": search_term, "offset":HP_initial_offset, "count":HP_group_size,"textDecorations": True, "textFormat": "HTML"}response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()total = 0
downloadedCount = min(HP_group_size,search_results['totalEstimatedMatches'] )os.mkdir(search_term)
currentOffset = 0
for offset in range(0, downloadedCount, HP_group_size): 
  params['offset'] = currentOffset
  response = requests.get(search_url, headers=headers, params=params)
  response.raise_for_status()
  search_results = response.json()
  for res in search_results["value"]:
    try:
      r = requests.get(res['contentUrl'], timeout=30)
      ext = res['encodingFormat']
      fname = search_term + '/'+  str(total).zfill(8) + '.' + ext
      fl = open(fname, 'wb')
      fl.write(r.content)
      fl.close()

      img = cv2.imread(fname)
      if img is None:
        print('bad file detected, deleting the file')
        os.remove(fname) 
        continue
      img1 =cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      
      total = total + 1
      fname = search_term + '/'+  str(total).zfill(8) + '.' + ext
      cv2.imwrite(fname, img1)
      total = total + 1
  
    except Exception as e:
      print(e)
      if type(e) in myexceptions:
        continue
  currentOffset = search_results['totalEstimatedMatches']