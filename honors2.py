"""
CSE 231 Honors Option Project Part 2

Updated Music Reading Algorithm

    Wave Class
        play()
            Writes a single wave object to a .wav file and plays it
        overtones()
            Layers wave functions of varying frequency and amplitude onto
            original tone
        __init__()
            Initializes wave attributes of amplitude, frequency, tempo, and
            duration, creates array from sine function with those values
            mulitiplication, optionally plays new wave
        __str__()
            Displays wave attributes using print

    Note Class
        Get_beats()
            Uses dict of note beats to match text to number of beats in note
        Get_tempos()
            Displays tempo options, prompts user for speed, uses dict of tempos
            to match text to music speeds
        Get_notes()
            Constructs a list of notes from tuple of attributes in master list
        __init__()
            Initializes note attributes of pitch, octave, beats, and tempo,
            calculates duration from number of beats and tempo
        __str__()
            Displays note attributes using print

    Piano Class
        Play()
            Matches pitch string and octave from a note object with the
            interval distance from middle C, calculates frequency, sets
            amplitude and frequency to 0 for rests
        __init__()
            Makes piano object with pitch dictionary, note to wave conversion
        __str__()
            Displays notes in the piano

    Song Class
        Play()
            Writes the wave array to a .wav file and plays the song
        Read_file()
            Generates master list of note attributes by reading text, dividing
            up note attributes, and appending them to the list as tuples
        __init__()
            Intializes basic attributes, reads file, makes lists of notes and
            waves, then assigns them as an array attribute to song object
        __str__()
        Displays song name using print

    Main()
        Displays header, prompts for user preferences, calls functions to open
        file, initializes and plays selected song objects
"""

import numpy as np
from scipy.io.wavfile import write
import os


class Wave(object):
    '''
    Waves are defined by an amplitude, frequency, tempo, and duration that
    are fed into a sine function to generate an array playable by the scipy.io
    wavfile writer. They can be added/subtracted to generate chords as well as
    multiplied using the operation method.
    '''

    def play_wave(self):
        '''Writes a single wave object to a .wav file and plays it'''
        write('operation.wav', self.samplerate, self.function.astype(np.int16))
        os.system('operation.wav')

    def overtones(self):
        '''Layers wave functions of varying freq and amps onto original tone'''

        func = 0
        # Overtone fractional values
        factor_lst = [0.36046922, 0.50991279, 0.11674297, 0.01287502]
        n = np.arange(0, self.duration, 1/self.samplerate)

        # Combine waves of different frequencies
        for factor in factor_lst:
            func += self.amplitude * factor*np.sin(
                2 * np.pi * self.frequency * n * (1+factor_lst.index(factor)))

        return func

    def __init__(self, amps=4096, freq=261.63, temp=60, dur=3):
        '''Initializes wave attributes, creates array from sine function'''

        self.frequency = freq
        self.tempo = temp
        self.duration = dur
        self.samplerate = 44100

        n = np.arange(0, dur, 1/self.samplerate)

        # Amplitude exponentially decays over time
        self.initial_amplitude = amps
        self.amplitude = amps*np.exp(-(0.25656511+1.64549261*n))
        func = self.amplitude * np.sin(2 * np.pi*freq*n)

        self.function = func + self.overtones()

    def __str__(self):
        '''Displays wave attributes using print'''
        return "Amplitude: {}, Frequency: {}, Tempo: {}, Duration: {}".\
            format(self.initial_amplitude, self.frequency,
                   self.tempo, self.duration)


class Note(object):
    '''
    Notes are defined by pitch, octave, number of beats, and tempo. From tempo
    and number of beats the duration in seconds is calculated.
    '''

    def get_beats(beat_str):
        '''Uses dict of note beats to match text to number of beats in note'''

        beat_dict = {"WN": 4, "DHN": 3, "DDHN": 3.5, "HN": 2, "HNT": 4/3,
                     "QN": 1, "QNT": 2/3, "DQN": 1.5, "DDQN": 1.75, "EN": 0.5,
                     "DEN": 0.75, "ENT": 1/3, "DDEN": 7/8, "SN": 0.25,
                     "DSN": 3/8, "SNT": 1/6, "TN": 1/8, "TNT": 1/12}

        beat_float = beat_dict[beat_str]

        return beat_float

    def get_tempos(tempo_str):
        '''
        Displays tempo options, prompts user for speed, uses dict of tempos
        to match text to music speeds
        '''

        tempo_dict = {'Grave': 30, 'Lento': 40, 'Largo': 50, 'Adagio': 60,
                      'Adagietto': 70, 'Andante': 75, 'Moderato': 90,
                      'Allegretto': 100, 'Allegro': 120, 'Vivace': 135,
                      'Presto': 170, 'Prestissimo': 180}

        # Divide multiple tempo names up if more than one
        tempo_list = tempo_str.split(',')

        while True:
            if len(tempo_list) == 3:

                choice_ch = input(
                    '(a) {}\n(b) {}\n(c) {}\nChoose a tempo: '.format(
                        tempo_list[0], tempo_list[1], tempo_list[2]))

                if choice_ch.lower() == 'a':
                    choice_str = tempo_list[0]

                elif choice_ch.lower() == 'b':
                    choice_str = tempo_list[1]

                elif choice_ch.lower() == 'c':
                    choice_str = tempo_list[2]

                else:
                    print("\nInvalid input. Try again.")
                    continue

                break

            elif len(tempo_list) == 2:

                choice_ch = input(
                    '(a) {}\n(b) {}\nChoose a tempo: '.format(
                        tempo_list[0], tempo_list[1]))

                if choice_ch.lower() == 'a':
                    choice_str = tempo_list[0]

                elif choice_ch.lower() == 'b':
                    choice_str = tempo_list[1]

                else:
                    print("\nInvalid input. Try again.")
                    continue

                break

            elif len(tempo_list) == 1:
                choice_str = tempo_list[0]
                break

        tempo_int = tempo_dict[choice_str]

        return tempo_int

    def get_notes(master_list, tempo_int):
        '''Constructs list of notes from tuple of attributes in master list'''

        note_list = []
        for element in master_list:
            note = Note(pit=element[0], octa=element[1], beats=element[2],
                        temp=tempo_int)
            note_list.append(note)

        return note_list

    def __init__(self, pit="C", octa=4, beats=1, temp=60):
        '''Initializes note attributes, calculates duration'''

        self.pitch = pit
        self.octave = octa
        self.beats = beats
        self.tempo = temp
        self.duration = beats*60/temp

    def __str__(self):
        '''Displays note attributes using print'''
        return "Pitch: {}, Octave: {}, Beats: {}, Tempo: {}, Duration: {}".\
            format(self.pitch, self.octave, self.beats, self.tempo,
                   self.duration)


class Piano(object):
    '''
    The Piano class contains a play function that creates a wave from
    a given note by matching the pitch to the number of half steps from C4 in
    a dictionary.
    '''

    def play_piano(self, note):
        '''
        Matches pitch string and octave with interval, calculates frequency,
        sets amplitude and frequency to 0 for rests, returns wave object
        '''

        try:
            # Scale tone number plus number of half steps in octave
            half_steps = self.pitch_dict[note.pitch] + (note.octave - 4) * 12

            # Frequency using interval from middle C
            frequency = 261.63 * 2**(half_steps/12)
            wave = Wave(freq=frequency, temp=note.tempo, dur=note.duration)

        except KeyError:
            # Rests aren't in pitch_dict, have amplitude and frequency = 0
            wave = Wave(amps=0, freq=0, temp=note.tempo, dur=note.duration)

        return wave

    def __init__(self):
        '''Makes piano object with pitch dictionary, note to wave conversion'''
        # Note names with half step values from middle C (C4)
        self.pitch_dict = {"C": 0, "c": 1, "D": 2, "d": 3, "E": 4, "F": 5,
                           "f": 6, "G": 7, "g": 8, "A": 9, "a": 10, "B": 11}

    def __str__(self):
        '''Displays notes in the piano'''
        pitch_lst = []
        step_lst = []
        for key, value in self.pitch_dict.items():
            step_lst.append(str(value))

            if value > 9:
                pitch_lst.append(key+' ')
            else:
                pitch_lst.append(key)

        pitch_str = '|'.join(pitch_lst)
        step_str = '|'.join(step_lst)

        return 'Notes On Piano: {}\nNote Half Step: {}'.format(
            pitch_str, step_str)


class Song(object):
    '''
    The song class reads text files, converts it to notes and then waves, then
    writes the waves to a .wav file in an array.
    '''

    def play_song(self):
        '''Writes the wave array to a .wav file and plays the song'''

        write(self.name + '.wav', self.samplerate, self.music_arr.astype(
            np.int16))
        os.system(self.name + '.wav')

    def read_file(fp):
        '''
        Generates master list of note attributes by reading file, dividing up
        attributes, and appending them to the list as tuples
        '''

        part1_list = []
        part2_list = []
        note_list = []
        line_count = 1
        tempo_str = ""

        for line in fp:

            # Extract tempo on first line
            if line_count == 1:
                tempo_str = line.strip()
                tempo_list = Note.get_tempos(tempo_str)

            # On lines without lyrics
            elif line[0] != '"':

                # Seperate each note into a list
                note_list = line.split("-")

                for note in note_list:

                    # Split each note into pitch, octave, then beats
                    try:
                        pitch_octave_str, beats_str = note.split(",")
                    except ValueError:
                        # For rests with no pitch or octave
                        pitch_octave_str, beats_str = "", note

                    # Separate out pitch, octave, beats
                    if pitch_octave_str != "":
                        note_tup = pitch_octave_str[0].upper(),\
                            int(pitch_octave_str[1]), Note.get_beats(
                                beats_str.strip())
                    else:
                        # If it's a rest, no pitch, just duration
                        note_tup = "", 4, Note.get_beats(beats_str.strip())

                    if line_count % 3 == 0:
                        part1_list.append(note_tup)
                    else:
                        part2_list.append(note_tup)

            line_count += 1

        # Return notes in a list of tuples with pitch, octave, and beats
        # Also list of tempos
        return tempo_list, part1_list, part2_list

    def __init__(self, name="alouette"):
        '''
        Intializes basic attributes, reads file, makes lists of notes and
        waves, then assigns them as an array attribute to song object
        '''

        self.name = name+'2'
        self.file = open(self.name+".txt", "r")
        self.samplerate = 44100

        # Read File
        tempo_int, part1_list, part2_list = Song.read_file(self.file)

        # Make list of note objects from file,
        note_list1 = []
        note_list2 = []

        # For each time through the song at each tempo
        part1 = Note.get_notes(part1_list, tempo_int)
        part2 = Note.get_notes(part2_list, tempo_int)

        # Append individually to list of all the notes
        for note in part1:
            note_list1.append(note)
            note_list2.append(note)

        # Make list of waves for each note
        wave_arr1 = np.empty(0, dtype=object)
        piano = Piano()
        for note in part1:
            wave = piano.play_piano(note)
            wave_arr1 = np.concatenate((wave_arr1, wave.function))

        wave_arr2 = np.empty(0, dtype=object)
        for note in part2:
            wave = piano.play_piano(note)
            wave_arr2 = np.concatenate((wave_arr2, wave.function))

        self.music_arr = wave_arr1 + wave_arr2

    def __str__(self):
        '''Displays song name using print'''
        return "Song Name: {}".format(self.name.title())


def main():

    # Header
    LENGTH = 38
    print(">"*LENGTH)
    print()
    print("{:^38s}".format("CSE 231 Honors Option Project Part 2"))
    print("{:^38s}".format("Updated Music Reading Algorithm"))
    print()
    print("<"*LENGTH)
    print()

    # Main program loop
    while True:
        # Call to open data files

        MENU_STR = "Choose a song to play:\n(a) Alouette\n\
(b) Twinkle, Twinkle, Little Star\n(c) Row, Row, Row, Your Boat\n\
(d) All\n(e) Quit"

        # Song choice input loop
        while True:
            print()
            print(MENU_STR)
            file_str = input("Selection: ")

            file_name_list = []

            # Input Decision Tree
            if file_str.lower() == "a":
                # Honors 1 file for testing
                file_name = "alouette"
                file_name_list.append(file_name)
                break

            elif file_str.lower() == "b":
                file_name = "twinkle_twinkle"
                file_name_list.append(file_name)
                break

            elif file_str.lower() == "c":
                file_name = "row_row"
                file_name_list.append(file_name)
                break

            elif file_str.lower() == "d":
                file_name1 = "alouette"
                file_name2 = "twinkle_twinkle"
                file_name3 = "row_row"
                file_name_list = [file_name1, file_name2, file_name3]
                break

            elif file_str.lower() == "e":
                file_name_list.append('')
                break

            else:
                print("\nInvalid input. Try again.")

        # Checks for quit input instead of file name, stops infinite loop
        if file_name_list[0] == '':
            print('\nIf you sing a song a day, you will make a better way.')
            print('Go in peace.')
            break

        # Plays the desired song(s), call to get_tempo prompts user again
        for name in file_name_list:
            song = Song(name)
            song.play_song()


main()
