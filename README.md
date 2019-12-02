# bboxLabeler
Python application to quickly and easily label images with bounding boxes for object detection. This 
will output a JSON file for each image you label. The JSON file will be in the following format.
{
   'xmin'  : 10,
   'ymin'  : 25,
   'xmax'  : 45, 
   'ymax'  : 60,
   'path'  : "c:\usr\Desktop\project\empire-state\empirestate.jpg",
   'image' : "empirestate.jpg",
   'label' : "Empire State Building"
}

## Dependencies
* Tkinter
* OS
* JSON
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
   ![Step 1: Select directory](https://github.com/nedhulseman/image-labeleling-app/blob/master/Step1.JPG)
2. Draw the Bounding box on your image in the desired location
![Step 2: Draw Bounding Box](https://github.com/nedhulseman/image-labeleling-app/blob/master/Step2.JPG)
3. Select the button 'Next Image' to navigate to the next image and the current image bounding box information will be saved to a JSON with the same name as the image.
![Step 3: Select next to save information and move to next image](https://github.com/nedhulseman/image-labeleling-app/blob/master/Step3.JPG)


