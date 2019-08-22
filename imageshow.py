import os
import os.path, time
import shutil
from datetime import datetime
from PIL import Image, ImageOps
from wand.drawing import Drawing, Color
import wand
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=False, default='output', help="output video file")
ap.add_argument("-i", "--input", required=False, default='.', help="input image files")
ap.add_argument("-t", "--target", required=False, default='tmp', help="name target temporary directory for images")
ap.add_argument("-p", "--prefix", required=False, default='img', help="prefix temp files")
ap.add_argument("-f", "--font", required=False, default='./res/OldStandard-Regular.ttf', help="watermark font")
ap.add_argument("-fs", "--fontsize", required=False, default=32, help="watermark font size")
ap.add_argument("-d", "--duration", required=False, default=3.5, help="duration of each frame")
ap.add_argument("-fps", "--frames", required=False, default=24.0, help="output video FPS")
ap.add_argument("-iw", "--initialwatermark", required=False, default='', help="watermark for first image")
ap.add_argument("-fw", "--finalwatermark", required=False, default='', help="watermark for last image")
args = vars(ap.parse_args())

source = args['input']
target = args['target']
prefix = args['prefix']

video_name = "{0}.mp4".format(args['output'])
framelenght = args['duration']
fps = args['frames']

FONT = args['font']
FONTSIZE = args['fontsize']
INITIAL_WATERMARK = args['initialwatermark']
FINAL_WATERMARK = args['finalwatermark']

size = 1024, 768
FINAL_WATERMARK = '      ? ? ?'

os.chdir(os.path.abspath(source))
if not os.path.exists(target):
    os.mkdir(target)

def get_exif_date_taken(path):
    return datetime.strptime(Image.open(path)._getexif()[36867], '%Y:%m:%d %H:%M:%S')
def get_os_date_taken(path):
    return datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")

def get_file_name(file_name, target, prefix, creation):
    if (file_name == 'initial') or (file_name == 'final'):
        return './{0}/{1}.jpg'.format(target, file_name)
    return './{0}/{1}-{2}.jpg'.format(target, prefix, str(creation))

def resize(input, output, size):
    try:
        im = Image.open(input)
        im.thumbnail(size, Image.ANTIALIAS)
        old_size = im.size
        delta_w = size[0] - old_size[0]
        delta_h = size[1] - old_size[1]
        padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
        new_im = ImageOps.expand(im, padding)
        new_im.save(output, "JPEG")
    except IOError:
        print("Cannot resize {0}".format(input))

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = 'Complete', decimals = 1, length = 50, fill = '█'):
    """
    ShoutOut: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# Save and rename according to creation date; 
#   if png convert to jpg;
#   watermarks with creation date
files = [file for file in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), file))]
l = len(files)
p = 'Creating temp files:'
printProgressBar(0, l, prefix = p)

for i, filename in enumerate(files):
    file_name, file_extension = os.path.splitext(filename)
    # check extension and getfilename
    if file_extension.lower() == '.png':
        creation = get_os_date_taken(filename)
        newfilename = get_file_name(file_name, target, prefix, creation)
        # convert to jpg
        im = Image.open(filename)
        rgb_im = im.convert('RGB')
        rgb_im.save(newfilename)
    elif (file_extension.lower() == '.jpg') or (file_extension.lower() == '.jpeg'):
        try:
            creation = get_exif_date_taken(filename)
        except:
            #print("No EXIF data for {0}: using fllback".format(filename))
            creation = get_os_date_taken(filename)
        newfilename = get_file_name(file_name, target, prefix, creation)
        # just copy to target dir
        shutil.copy(filename, newfilename)
    else:
        print("Invalid file {0}; It works only with .jpg or .png files".format(filename))
        printProgressBar(i + 1, l, prefix =p)
        continue
    
    # Resize & Watermark. 
    #    Do not watermark the initial and final images
    resize(newfilename,newfilename, size)

    if file_name=="initial" :
        if INITIAL_WATERMARK == '':
            printProgressBar(i + 1, l, prefix =p)
            continue
        watermark = INITIAL_WATERMARK
    elif file_name=="final":
        if FINAL_WATERMARK == '':
            printProgressBar(i + 1, l, prefix =p)
            continue
        watermark = FINAL_WATERMARK
    else:
        watermark = creation.strftime('%d %m %Y')

    with Drawing() as draw:
        with wand.image.Image(filename=newfilename) as image:
            #print(newfilename)
            draw.font = FONT
            draw.font_size = FONTSIZE
            draw.text_antialias = True
            draw.stroke_color = Color('yellow')
            draw.text(round(image.width / 2) - 100, image.height - 50, watermark)
            draw(image)
            image.save(filename=newfilename)
    printProgressBar(i + 1, l, prefix =p)

# Create video
os.chdir(os.path.abspath("./{0}".format(target)))

images = [img for img in os.listdir(os.getcwd()) if (img.endswith(".jpg") and (not img.startswith("initial")) and (not img.startswith("final")) )]
images = sorted(images)
if os.path.isfile('./initial.jpg'):
    images.insert(0, "initial.jpg")
if os.path.isfile('./final.jpg'):
    images.append("final.jpg")

(width,height) = size
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))
frame_rep = int(fps * framelenght)

l = len(images)
p = 'Creating video:'
printProgressBar(0, l, prefix = p)

for i, im in enumerate(images):
    frame = cv2.imread(os.path.join(os.getcwd(), im))
    for _ in range(frame_rep):
        video.write(frame)
    printProgressBar(i + 1, l, prefix =p)
cv2.destroyAllWindows()
video.release()
