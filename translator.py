import os

import math

import speech_recognition as sr

from googletrans import Translator

from gtts import gTTS

def input_video_path() :
    
    global video_path
    
    video_path = input("\nEnter the path of the video you want to translate: ")
    
    if (os.path.isfile(video_path) == False) :
        
        print("\nThe specified file does not exist.")
        
        input_video_path()
    
    if (os.path.splitext(video_path)[1] != ".mp4") :
        
        print("\nThe specified file is not an mp4 file.")
        
        input_video_path()

def input_original_language() :
    
    global o_language
    
    global o_language_code
    
    o_language = input("\nOriginal Language: ")
    
    codes = open("language_codes.txt", "r")
    
    codes = codes.read().encode("latin-1").decode("utf-8")
    
    if codes.lower().find("\n" + o_language.lower() + " ") == -1 :
        
        print("\nThis language either is not available, doesn't exist or was typed incorrectly. Please check it again.")
        
        input_original_language()
    
    o_language_code = codes[codes.lower().find("\n" + o_language.lower() + " ") + len("\n" + o_language.lower() + " | ") : ]
    
    o_language_code = o_language_code[0 : o_language_code.find("\n")]

def input_target_language() :
    
    global t_language
    
    global t_language_code
    
    t_language = input("\nTarget Language: ")
    
    codes = open("language_codes.txt", "r")
    
    codes = codes.read().encode("latin-1").decode("utf-8")
    
    if codes.lower().find("\n" + t_language.lower() + " ") == -1 :
        
        print("\nThis language either is not available, doesn't exist or was typed incorrectly. Please check it again.")
        
        input_target_language()
    
    t_language_code = codes[codes.lower().find("\n" + t_language.lower() + " ") + len("\n" + t_language.lower() + " | ") : ]
    
    t_language_code = t_language_code[0 : t_language_code.find("\n")]

print("Video Translator")

input_video_path()

input_original_language()

input_target_language()

print("\nExtracting speech from video (This might take a while as the application has to listen to the whole video) ...")

video_duration = float(os.popen('ffmpeg\\bin\\ffprobe.exe -i "' + video_path + '" -show_entries format=duration -v quiet -of csv="p=0"').read())

os.system('ffmpeg\\bin\\ffmpeg.exe -i "' + video_path + '" -q:a 0 -map a audio.wav -y -hide_banner -loglevel panic')

transcription = [""]

transcription_num = 0

r = sr.Recognizer()

for i in range(math.ceil(video_duration / 20)) :
    
    with sr.AudioFile("audio.wav") as source :
        
        audio = r.record(source, duration = 20)
    
    if len(transcription[transcription_num]) > 10000 :
        
        transcription.append("")
        
        transcription_num += 1

    transcription[transcription_num] = transcription[transcription_num] + " " + r.recognize_google(audio, language=o_language_code)

    os.system("ffmpeg\\bin\\ffmpeg.exe -ss 20 -i audio.wav -c copy audio1.wav -y -hide_banner -loglevel panic")
    
    os.remove("audio.wav")
    
    os.rename("audio1.wav", "audio.wav")

os.remove("audio.wav")

print("\nTranslating speech...")

translation = ""

for i in transcription :
    
    translation = translation + " " + Translator().translate(i, dest=t_language_code).text

tts = gTTS(translation, lang=t_language_code)

tts.save("translation.mp3")

print("\nCreating new video...")

audio_duration = float(os.popen('ffmpeg\\bin\\ffprobe.exe -i translation.mp3 -show_entries format=duration -v quiet -of csv="p=0"').read())

new_rate = audio_duration / video_duration

os.system('ffmpeg\\bin\\ffmpeg.exe -i translation.mp3 -filter:a atempo=' + str(new_rate) + ' -vn translation1.mp3 -y -hide_banner -loglevel panic')

os.remove("translation.mp3")

os.rename("translation1.mp3", "translation.mp3")

new_video_name = "test Translated.mp4"

os.system('ffmpeg\\bin\\ffmpeg.exe -i "' + video_path + '" -i translation.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "' + new_video_name + '" -y -hide_banner -loglevel panic')

os.remove("translation.mp3")

os.startfile(new_video_name)

print("\nDone")

input()
