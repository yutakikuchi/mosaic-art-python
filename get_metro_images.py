import requests
import json
import os
import sys

url = "https://collectionapi.metmuseum.org/public/collection/v1/"

def get_object_lists(params):
  data = requests.get(url + "search", params=params).json()
  return data["objectIDs"]

def get_primary_image(object):
  data = requests.get(url + "objects/" + str(object)).json()
  if "primaryImageSmall" in data:
    return data["primaryImageSmall"]
  return None

def download_images(save_path, max_num, object_lists):
  num = 0
  for object in object_lists:
    if num >= max_num:
      break
    try:
      image = get_primary_image(object)
      if image:
        data = requests.get(image).content
        fname = os.path.basename(image)
        with open(save_path + fname, mode="wb") as f:
          f.write(data)
        num += 1
    except Exception as e:
      tb = sys.exc_info()[2]
      print("message:{0}".format(e.with_traceback(tb)))
      pass

if __name__ == "__main__":

  try:
    save_path = sys.argv[1]
    query = sys.argv[2]
    max_num = int(sys.argv[3])
    params = {
        "hasImages" : "true",
        "isPublicDomain" : "true",
        "q" : query
    }    
    object_lists = get_object_lists(params)
    download_images(save_path, max_num, object_lists)
  except Exception as e:
    tb = sys.exc_info()[2]
    print("message:{0}".format(e.with_traceback(tb)))
    print('Can not finish the process')