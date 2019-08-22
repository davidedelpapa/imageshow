# ImageShow

Create a video slideshow out of .jpg and .png pictures sitting in a folder.
It watermarks each picture with the date taken. The actual data for this is taken by EXIF or, in lack thereof, from last modified data.

**Version 0.1**

## Usage

``` sh
usage: imageshow.py [-h] [-o OUTPUT] [-i INPUT] [-t TARGET] [-p PREFIX]
                    [-f FONT] [-fs FONTSIZE] [-d DURATION] [-fps FRAMES]
                    [-iw INITIALWATERMARK] [-fw FINALWATERMARK]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output video file
  -i INPUT, --input INPUT
                        input image files
  -t TARGET, --target TARGET
                        name target temporary directory for images
  -p PREFIX, --prefix PREFIX
                        prefix temp files
  -f FONT, --font FONT  watermark font
  -fs FONTSIZE, --fontsize FONTSIZE
                        watermark font size
  -d DURATION, --duration DURATION
                        duration of each frame
  -fps FRAMES, --frames FRAMES
                        output video FPS
  -iw INITIALWATERMARK, --initialwatermark INITIALWATERMARK
                        watermark for first image
  -fw FINALWATERMARK, --finalwatermark FINALWATERMARK
                        watermark for last image
```

## Copyright

MIT

### CAVEAT

 - It uses [Google's font OldStandardTT](https://fonts.google.com/specimen/Old+Standard+TT)[Open Font License](http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL_web)
 - Some code taken from [StackOverflow](https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console), and modified, in order to display a progressbar. It should be public domain.
