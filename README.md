# bboxLabeler
Python application to quickly and easily label images with bounding boxes for object detection. This 
will output a pickle file where the index is the name of the name of the image 
and will story the x & y of the upper left corner, height and width.

## Dependencies
* Tkinter
* OS
* Pandas
* PIL

## Installation 
``` 
$ git clone https://github.com/nedhulseman/image-labeleling-app.git
```

## Usage
``` 
$ python bboxLabeler.py
```
### Using GUI App
1. Use File Explorer to browse to directory containing the library of images to be labeled. 
   - Note that this applciation will not alter images in any way. This will simply store the location of the bounding box on the image. 
   - If you resize the images after recording the bounding box location that the coordinates will need to be transformed.
2. Use File Explorer to browse to directory where the saved picle file is or if new, where you would like to store the output pickle file
3. Once image is loaded, draw box on image. Once you hit the 'Next Image' or 'Save' button, the coordinates are recorded in the DataFrame. If you select 'Previous Image', the coordinates will be erased for that image.
3. Make sure to save any progress before exiting
4. If you want to continue from a previous section, make sure to add the path using "Output bbox Coordinates" file browser


