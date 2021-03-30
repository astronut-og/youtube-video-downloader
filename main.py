from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
import pytube
import moviepy
import shutil
import eyed3
import os
import mutagen
from pytube import YouTube
from mutagen.easyid3 import EasyID3
from pytube import Playlist


def get_user_input():
    user_input = input("Enter the link: ")
    if "playlist" in user_input:
        playlist = Playlist(user_input)
        print("This is a playlist, starting download")
        for song in playlist.videos:
            download_video(song)
        print("Finished downloading playlist")
    else:
        youtube_obj =  YouTube(user_input)
        download_video(youtube_obj)

def download_video(youtube_obj):
    title = get_video_title(youtube_obj)
    youtube_video = youtube_obj.streams.filter(progressive=True).get_highest_resolution()
    youtube_video.download()
    print("MP4 is downloaded")
    convert_video_to_audio(title)
    print("Converted the MP4 to MP3")
    get_thumbnail_image(youtube_obj)
    print("Thumbnail downloaded")
    set_thumbnail(title)
    print("Thumbnail has been set")
    set_artist(youtube_obj, title)
    print("Artist has been set")
    cleanup(title)
    cls()
    array.append(f"{title} has been successfully downloaded")
    for song in array:
        print(song)


def get_video_title(youtube_obj):
    return youtube_obj.title

def get_thumbnail_image(youtube_obj):
    """ this downloads the thumbnail of the video to later set as the thumbnail of the mp3
    """
    thumbnail_url = youtube_obj.thumbnail_url
    print(thumbnail_url)
    thumbnail_url = thumbnail_url.split("?")[0]
    print(thumbnail_url)
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

def convert_video_to_audio(filename):
    """ this converts the mp4 file you just downloaded to an mp3 file
    """
    mp4_title = filename + ".mp4"
    mp3_title = filename + ".mp3"
    videoclip = VideoFileClip(mp4_title)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_title)
    audioclip.close()
    videoclip.close()

def set_thumbnail(filename):
    """ this sets a thumbnail for the mp3 which is just the thumbnail from the youtube video
    """
    mp3_url = filename + ".mp3"
    audiofile = eyed3.load(mp3_url)
    if(audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, open('maxresdefault.jpg', 'rb').read(), 'image/jpeg')
    audiofile.tag.save()

def set_artist(youtube_obj, filename):
    audio = EasyID3(filename + ".mp3")
    artist_name = youtube_obj.author
    audio['artist'] = f"{artist_name}"
    audio.save()

def cleanup(filename):
    """ this deletes the now-useless files
    """
    os.remove(filename + ".mp4")
    os.remove("maxresdefault.jpg")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

status = True
array = []
while status:
    get_user_input()