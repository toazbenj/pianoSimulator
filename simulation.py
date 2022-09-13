"""
Music Reading Algorithm

        Displays header, prompts for user preferences, calls functions to open
        file, initializes and plays selected song objects
"""

import musicClasses as music

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
        song = music.Song(name)
        song.play_song()
