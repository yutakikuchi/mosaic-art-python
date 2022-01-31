# mosaic-art-python


## process of execution

### get images from the Metropolitan Museum

- The Metropolitan Museum of Art Collection API
  - https://metmuseum.github.io/

- We have to run the script to get the sample images as below.
  - `mkdir ./images`
  - `python get_metro_images.py <download_path> <query> <max_num>`

- We have to run the next script to generate the mosaic images as below.
  - `python gen_mosaic_image.py <main_photo_path> <download_path> <tile_width_size> <tile_height_size> <output_width_size> <output_height_size> <output_path>`

## Ref.
- https://zenn.dev/eetann/books/2020-09-25-make-mosaic-art-python
- https://gist.github.com/BilHim/77f17e2fa859a56c1d365c6e558b291f#file-mosaic-py