#!/usr/bin/env python3
"""

NAME
mpg321 — Simple and lightweight command line MP3 player
SYNOPSIS
mpg321 [options] file(s) | URL(s) | -
DESCRIPTION
mpg321 is a free command-line mp3 player, which uses the mad audio decoding library. mpg321 was written to be a drop-in replacement for the (by-then) non-free mpg123 player. Some functions remain unimplemented, but mpg321 should function as a basic drop-in replacement for mpg123 front-ends such as gqmpeg, and those programs which use mpg123 to decode mp3 files (like gtoaster, and other CD-recording software).
OPTIONS
-o devicetype
Set the output device type to devicetype. devicetype can be one of:
oss - the Linux Open Sound System;
sun - the Sun audio system;
alsa - the Advanced Linux Sound Architecture;
alsa09 - the Advanced Linux Sound Architecture, version 0.9;
esd - the Enlightened Sound Daemon;
arts - the analog real-time synthesiser
See -a device, below.
-a device, --audiodevice device
Use device for audio-out instead of the default device, depending on the output device you've chosen (via -o devicetype). By default this is the native sound device. Generally this is the device for devicetype (or the default system device) to use for output (i.e. /dev/sound/dsp1).
This option has no effect with -o arts.
For -o esd, specify the host on which esd is running; defaults to localhost.
For -o alsa, specify audio device using the hw:x,y syntax, where x and y are numbers, default is hw:0,0. For example, if there is only one device installed, in most cases, the device should be named hw:0,0. When there is only one device, the device should always have the same name and numbers.
-g N, --gain N
Set gain (volume) to N (1-100).
-k N, --skip N
Skip N frames into the file being played.
-n N, --frames N
Decode only the first N frames of the stream. By default, the entire stream is decoded.
-@ list, --list list
Use the file list for a playlist. The list should be in a format of filenames followed by a line feed. Multiple -@ or --list specifiers will be ignored; only the last -@ or --list option will be used. The playlist is concatenated with filenames specified on the command-line to produce one master playlist. A filename of '-' will cause standard input to be read as a playlist.
-z, --shuffle
Shuffle playlists and files specified on the command-line. Produces a randomly-sorted playlist which is then played through once.
-Z, --random
Randomise playlists and files specified on the command-line. Files are played through, choosing at random; this means that random files will be played for as long as mpg321 is running.
-v, --verbose
Be more verbose. Show current byte, bytes remaining, time, and time remaining, as well as more information about the mp3 file.
-s, --stdout
Use standard output instead of an audio device for output. Output is in 16-bit PCM, little-endian.
-w N, --wav N
Write to wav file N instead of using the audio device. This option will be preferred if --cdr or --au are specified too. Specifying '-' for N will cause the file to be written to standard output.
--cdr N
Write to cdr file N instead of using the audio device. Specifying '-' for N will cause the file to be written to standard output.
--au N
Write to au file N instead of using the audio device. Specifying '-' for N will cause the file to be written to standard output.
-t, --test
Test mode; do no output at all.
-q, --quiet
Quiet mode; suppress output of mpg123 boilerplate and file and song name.
-B
Read recursively the given directories. Allows you to define only the directory or directories and then mpg321 recursively plays all the songs.
-F
Turn on FFT analysis on PCM data. Remote mode only
-S
Report song to AudioScrobbler (last.fm).
-x
Set xterm title setting
-b
Number of decoded frames for the output buffer.
-K
Enable Basic Keys.
-R
"Remote control" mode. Useful for front-ends. Allows seeking and pausing of mp3 files. See README.remote (in /usr/share/doc/mpg321 on Debian and some other systems.)
-3, --restart
Restart "remote shell". Used only when in "Remote control" mode.
--stereo
Force stereo output: duplicates mono stream on second output channel. Useful for output for devices that don't understand mono, such as some CD players.
--aggressive
Aggressive mode; try to get higher priority on the system. Needs root permissions.
--skip-printing-frames=N
Skip N frames between printing a frame status update, in both Remote Control (-R) and verbose (-v) mode. Can help CPU utilisation on slower machines. This is an mpg321-specific option.
-l N, --loop N
Loop song or playlist N times.If N is 0 means infinite times.
--help, --longhelp
Show summary of options.
-V, --version
Show version of program.

class P(Process):
        super(P, self).__init__()
        self.filename = filename

    def run(self):
        
        from playsound import playsound
        playsound( self.filename, block = True)

        p = Popen(args=['mpg321', '-q', self.filename], shell=False, stdout=PIPE, stderr=PIPE)
        while p.poll() != 0 or p.returncode != 0:
            if TTSEngine.stop_speaking == True:
                p.terminate()
                break
            time.sleep(0.5)

        
        music = AudioSegment.from_mp3(self.filename)
        play(music)
        

class MyClass(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        try:
            print(os.getpid())
            self.raise_exception()
            
            print(111111)
            from playsound import playsound
            playsound( self.filename, block = True)
            
        except Exception as e:
            print(e)
        
    def get_id(self):
        
        print(threading.current_thread().name)
        print(threading.get_ident())
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id """

from gtts import gTTS
import time
import os
from subprocess import Popen, PIPE
from utils.dir import get_ouput_audio

class TTSEngine(object):

    stop_speaking = False
    dir_path = get_ouput_audio()
    p = None
    p_song = None
    next_song = False
    
    @staticmethod
    def _build_audio(message, slow=False):
        if message:
            myobj = gTTS(text=message, lang="es", slow=slow)
            filename = os.path.join(TTSEngine.dir_path, "speek.mp3")
            myobj.save(filename)
            return filename
        return None

    @staticmethod
    def _play_audio(filename, asyncx = False):
        TTSEngine.p = Popen(args=['mpg321', '--stereo' ,'-q', filename], stdout=PIPE)
        #p.wait()
        if asyncx == False:
            TTSEngine.wait_audio()

    @staticmethod
    def wait_audio():
        while TTSEngine.p.poll() is None or TTSEngine.p.returncode  is None:
            if TTSEngine.stop_speaking == True:
                TTSEngine.stop_audio()
                break
            time.sleep(0.5)
        TTSEngine.stop_audio()

    @staticmethod
    def stop_audio():
        if TTSEngine.p and (TTSEngine.p.poll() is None or TTSEngine.p.returncode is None):
            TTSEngine.p.terminate()
        time.sleep(0.8)

    @staticmethod
    def play_text(message=None, slow=False, asyncx = False):
        print(message)
        if message:
            TTSEngine.set_stop_speaking(False)
            if TTSEngine.p and (TTSEngine.p.poll() is None or TTSEngine.p.returncode is None):
                #TTSEngine.wait_audio()
                TTSEngine.p.terminate()
            f = TTSEngine._build_audio(message, slow)
            TTSEngine._play_audio(f, asyncx)


    @staticmethod
    def _play_song(filename, asyncx = False):
        TTSEngine.p_song = Popen(args=['mpg321', '--stereo' ,'-q', filename], stdout=PIPE)
        #p.wait()
        if asyncx == False:
            TTSEngine.wait_song()

    @staticmethod
    def set_stop_speaking(stop_speaking=False):
        TTSEngine.stop_speaking = stop_speaking

    @staticmethod
    def wait_song():
        while TTSEngine.p_song.poll() is None or TTSEngine.p_song.returncode is None:
            if TTSEngine.stop_speaking == True:
                TTSEngine.stop_song()
                break
            time.sleep(0.5)
        TTSEngine.stop_song()

    @staticmethod
    def stop_song():
        if TTSEngine.p_song and (TTSEngine.p_song.poll() is None or TTSEngine.p_song.returncode is None):
            TTSEngine.p_song.terminate()
        time.sleep(0.8)

    @staticmethod
    def play_sound(filename=None, asyncx = False):
        print(filename)
        if filename:
            TTSEngine.set_stop_speaking(False)
            if TTSEngine.p_song and (TTSEngine.p_song.poll() is None or TTSEngine.p_song.returncode is None):
                #TTSEngine.wait_song()
                TTSEngine.stop_song()
            TTSEngine._play_song(filename, asyncx)