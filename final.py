'''
Copyright Jackson Yoes 2024 (Jack0wack0 https://github.com/Jack0wack0) 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

Cody AI is used in this code. Cody AI is a free AI that can generate code. Any AI generated code will be denoted by a comment.

'''

# Imports
from pytube import YouTube
import os
import urllib.request
import re
import platform
import ssl

# Permanant Variables
youtube_regex = r'(https?://)?(www\.)?' r'((youtube\.com)|((m|music)\.youtube\.com))/' r'[^\s]+$' # this was googled and found on StackOverflow. https://stackoverflow.com/questions/3717115/regular-expression-for-youtube-links

# Functions
def startprogram():
    checkplatform()    # Forces HTTPS if the device is a MAC
    os.system("clear")
    print("Welcome to Youtube downloader!")
    init_link = input("Paste the link you want to download now: ")    # Obtains youtube link
    if checklink(init_link) == False:   # checks if the link is valid
        os._exit(os.EX_OK)    # People prioritize elegancy. I do things as violently as possible.
    checklinkvalid(init_link)    # Ensures the link is reachable
    checkcorrectvideo(init_link)    # Prints the title and other details of the video
    mkv_result, _ = check_mkv(init_link)    # Checks to make sure the video is not malware.
    if mkv_result == True:
        print("This video is marked as unsafe. Do not attempt to download.")
        os._exit(os.EX_OK)
    else:
        print("Video is safe. Downloading now.")
        downloadlink(init_link)    # Downloads the video
    

def checkplatform():
    if platform.system() == "Darwin":
        ssl._create_default_https_context = ssl._create_stdlib_context    # This automatically requires a https certification from youtube. Read more here: https://peps.python.org/pep-0476/
    else:
        print(f"Operating System: {platform.system()}")    # Detecting operating system


def checklink(init_link):
    if re.match(youtube_regex, init_link):    # Checks if the video matches the youtube regex
        return True
    else:
        print("Invalid link. Please try again.")
        return False
    

def checklinkvalid(init_link):    # Error Handling
    if not init_link:
        raise TypeError('No link provided')
    try:
        response = urllib.request.urlopen(init_link)
        if response.getcode() == 200:
            return True
    except Exception:
        print("Invalid link")
        os._exit(os.EX_OK)


def checkcorrectvideo(init_link):    # Prints the title and other details of the video
    parselink = YouTube(init_link)
    os.system("clear")
    print(f"Title: {parselink.title}")
    print(f"Views: {parselink.views}")
    print(f"Author: {parselink.author}")
    print(f"Filesize: {(parselink.streams.get_highest_resolution().filesize / 1000000)} MB")


# This function checks if the file downloaded contains the extension .mkv. .mkv is a common file extension for malware. This prevents middleman attacks.
def check_mkv(init_link):
  stream = YouTube(init_link).streams.get_highest_resolution()    # Get the highest resolution
  file = stream.download()   # Download
  if os.path.splitext(file)[1].lower() == '.mkv': #AI Generated Code. This line only.
    os.remove(file)     # Delete the download
    print("This video is marked as unsafe. Do not attempt to download.")
    safe = True
    return True, safe # Just return both cuz its more fun that way
  else:
    os.remove(file)    # Delete the download
    safe = False
    return False, safe

  
def downloadlink(dwlink):    # Download the whole thing
    streamdownload = YouTube(dwlink).streams.get_highest_resolution()
    output = os.path.expanduser("~/Downloads")
    streamdownload.download(output_path = output)
    print(f"Download complete. Location: {output}. Enjoy!")
  
startprogram()    # The only function outside of the functions