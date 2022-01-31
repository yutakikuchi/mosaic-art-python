import glob
from PIL import Image
from scipy import spatial
import numpy as np
import sys

def get_ref_images(tile_photos_path):
  tile_paths = []
  for file in glob.glob(tile_photos_path + '/*'):
    try:
      tile_paths.append(file)
    except Exception as e:
      tb = sys.exc_info()[2]
      print("message:{0}".format(e.with_traceback(tb)))
      pass
  return tile_paths

def get_resize_images(tile_paths, tile_size):
  tiles = []
  for path in tile_paths:
    try:
      tile = Image.open(path)
      tile = tile.resize(tile_size).convert('RGB')
      tiles.append(tile)
    except Exception as e:
      tb = sys.exc_info()[2]
      print("message:{0}".format(e.with_traceback(tb)))
      pass
  return tiles

def get_mean_colors(tiles):
  colors = np.empty((0,4), dtype=np.uint32)
  for tile in tiles:
    try:
      img = np.array(tile)
      mean_br = np.array([img.mean(dtype=np.uint32)])
      mean_color = img.mean(axis=0, dtype=np.uint32).mean(axis=0, dtype=np.uint32)
      mean_br = np.append(mean_br, mean_color)
      colors = np.append(colors, [mean_br], axis=0)
    except Exception as e:
      tb = sys.exc_info()[2]
      print("message:{0}".format(e.with_traceback(tb)))
      pass
  return colors

def get_closest_tile(colors, width, height, resized_photo):
  tree = spatial.cKDTree(colors, leafsize=16)
  closest_tiles = np.zeros((width, height), dtype=np.uint32)
  img_array = np.array(resized_photo)
  for y in range(height):
    for x in range(width):
      try: 
        pixdata = img_array[y][x]
        comp = np.empty((0,4), dtype=np.uint32)
        mean_brightness = np.array(pixdata).mean(dtype=np.uint32)
        tmp_array = np.append([mean_brightness], pixdata)
        comp = np.append(comp, np.array([tmp_array], dtype=np.uint32), axis=0)
        closest = tree.query(comp)
        closest_tiles[x, y] = closest[1]
      except Exception as e:
        tb = sys.exc_info()[2]
        print("message:{0}".format(e.with_traceback(tb)))
        pass
  return closest_tiles

def save_mosaic_img(width, height, closest_tiles, tiles, tile_size, output_size, output_path):
  try:
    output = Image.new('RGB', (output_size[0], output_size[1]))
    for j in range(height):
      for i in range(width):
        x, y = i*tile_size[0], j*tile_size[1]
        index = closest_tiles[i, j]
        output.paste(tiles[index], (x, y))
    output.save(output_path)
  except Exception as e:
    tb = sys.exc_info()[2]
    print("message:{0}".format(e.with_traceback(tb)))
    pass     
  
def gen_mosaic_img(main_photo_path, tile_photos_path, tile_size, output_size, output_path):
  
  tile_paths = get_ref_images(tile_photos_path)
  tiles = get_resize_images(tile_paths, tile_size)
  colors = get_mean_colors(tiles)
  
  width = int(output_size[0] / tile_size[0])
  height = int(output_size[1] / tile_size[1])

  resized_photo = Image.open(main_photo_path).resize((width, height))
  resized_photo = resized_photo.convert('RGB')

  closest_tiles = get_closest_tile(colors, width, height, resized_photo)
  save_mosaic_img(width, height, closest_tiles, tiles, tile_size, output_size, output_path)
  

if __name__ == "__main__":
  # ref : https://gist.github.com/BilHim/77f17e2fa859a56c1d365c6e558b291f#file-mosaic-py
  try:
    main_photo_path = sys.argv[1]
    tile_photos_path = sys.argv[2]
    tile_size = (int(sys.argv[3]), int(sys.argv[4]))
    output_size = (int(sys.argv[5]), int(sys.argv[6]))
    output_path = sys.argv[7]
    gen_mosaic_img(main_photo_path, tile_photos_path, tile_size, output_size, output_path)
  except Exception as e:
    tb = sys.exc_info()[2]
    print("message:{0}".format(e.with_traceback(tb)))
    print('Can not finish the process')