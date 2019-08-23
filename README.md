# ImageShow

Create a video slideshow out of .jpg and .png pictures sitting in a folder.
It watermarks each picture with the date taken. The actual data for this is taken by EXIF or, in lack thereof, from last modified data.

**Version 0.2**

## Usage

``` sh
usage: ImageShow [--help] [--version] {watermark} ...

positional arguments:
  {watermark}
    watermark  Watermarks the pictures.

optional arguments:
  --help       display help
  --version    show program's version number and exit

ImageShow 0.2 -- MIT (C) 2019 Davide Del Papa.
Option 'watermark'
usage: ImageShow watermark [-h] [-f FONT] [-fs FONTSIZE]
                           [-iw INITIALWATERMARK] [-fw FINALWATERMARK]
                           [-o OUTPUT] [-i INPUT] [-t TARGET] [-p PREFIX]
                           [-d DURATION] [-fps FRAMES]

optional arguments:
  -h, --help            show this help message and exit
  -f FONT, --font FONT  watermark font
  -fs FONTSIZE, --fontsize FONTSIZE
                        watermark font size
  -iw INITIALWATERMARK, --initialwatermark INITIALWATERMARK
                        watermark for first image
  -fw FINALWATERMARK, --finalwatermark FINALWATERMARK
                        watermark for last image
  -o OUTPUT, --output OUTPUT
                        output video file
  -i INPUT, --input INPUT
                        input image files
  -t TARGET, --target TARGET
                        name target temporary directory for images
  -p PREFIX, --prefix PREFIX
                        prefix temp files
  -d DURATION, --duration DURATION
                        duration of each frame
  -fps FRAMES, --frames FRAMES
                        output video FPS
```

## Copyright

MIT

### CAVEAT

 - It uses [Google's font OldStandardTT](https://fonts.google.com/specimen/Old+Standard+TT)[Open Font License](http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL_web)
 - Some code taken from [StackOverflow](https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console), and modified, in order to display a progressbar. It should be public domain.
