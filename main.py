from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
import pytube
import moviepy
import shutil
import eyed3
import os

from pytube import YouTube

user_link = input("Enter the link: ")
yt = YouTube(user_link)

def get_video_title():
    title = yt.title
    return title

def get_thumbnail_image():
    """ this downloads the thumbnail of the video to later set as the thumbnail of the mp3
    """
    thumbnail_url = yt.thumbnail_url
    # sends request to get the thumbnail from the video
    r = requests.get(thumbnail_url, stream=True)
    filename = thumbnail_url.split("/")[-1]
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded')
    else:
        print('Image Couldn\'t be retreived')

def convert_video_to_audio():
    """ this converts the mp4 file you just downloaded to an mp3 file
    """
    mp4_title = get_video_title() + ".mp4"
    mp3_title = get_video_title() + ".mp3"
    videoclip = VideoFileClip(mp4_title)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_title)
    audioclip.close()
    videoclip.close()

def set_thumbnail():
    """ this sets a thumbnail for the mp3 which is just the thumbnail from the youtube video
    """
    audiofile = eyed3.load(get_video_title() + ".mp3")
    if(audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, open('maxresdefault.jpg', 'rb').read(), 'image/jpeg')
    audiofile.tag.save()

def cleanup():
    """ this deletes the now-useless files
    """
    os.remove(get_video_title() + ".mp4")
    os.remove("maxresdefault.jpg")

ys = yt.streams.filter(progressive=True).get_highest_resolution()
ys.download()
convert_video_to_audio()
get_thumbnail_image()
set_thumbnail()
cleanup()