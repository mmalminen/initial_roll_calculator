import tkinter as tk
from tkinter import font, Entry, OptionMenu, Label, Checkbutton, Button
import random

# create a tkinter window
root = tk.Tk()
root.title("")
window_width = 275
window_height = 300
custom_font = font.Font(family="Helvetica", size=13)
custom_bold_font = font.Font(family="Helvetica", size=14, weight="bold")
sequence_field_width = 14
sequence = []

# function to center the window on the screen
def center_window(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

center_window(window_width, window_height)

class Character:
    def __init__(self):
        self.tag = tk.StringVar(root)
        self.modifier = tk.StringVar(root)
        self.advantage = False
        self.advantage_state = tk.IntVar()
        self.disadvantage = False
        self.disadvantage_state = tk.IntVar()
        self.throw = tk.StringVar(root)
        
        # tag field for input
        self.tag_field = Entry(root, bd=4, width=3, font=custom_bold_font)
        self.tag_field.place(x=110, y=10)
        # modifier menu
        self.modifier.set('0')
        self.modifier_values = [i for i in range(-5, 11)]
        self.modifier_menu = OptionMenu(root, self.modifier, *self.modifier_values)
        self.modifier_menu.place(x=100, y=45)
        # advantage and disadvantage checkboxes
        self.advantage_label = Label(root, text="     ADV", fg='black')
        self.advantage_label.place(x=100, y=80)
        self.advantage_check_label = Label(root, text="+", fg='black', font=custom_font)
        self.advantage_check_label.place(x=132.5, y=95)
        self.advantage_check = Checkbutton(root, variable=self.advantage_state, command=self.update_advantage)
        self.advantage_check.place(x=127.5, y=115)
        self.disadvantage_check_label = Label(root, text="-", fg='black', font=custom_font)
        self.disadvantage_check_label.place(x=112.5, y=95)
        self.disadvantage_check = Checkbutton(root, variable=self.disadvantage_state, command=self.update_disadvantage)
        self.disadvantage_check.place(x=107.5, y=115)
        # throw menu
        self.throw.set('0')
        self.throw_values = [str(i) for i in range(0, 21)]
        self.throw_menu = OptionMenu(root, self.throw, *self.throw_values)
        self.throw_menu.place(x=100, y=150)

        # bind the function to update tag whenever the entry changes
        self.tag_field.bind("<KeyRelease>", self.update_tag)

    def update_advantage(self):
        if self.advantage_state.get():
            self.advantage = True
            self.disadvantage = False
            self.disadvantage_state.set(0)
            print(f"Tag: {self.tag.get()} advantage = {self.advantage}")
        else:
            self.advantage = False
            print(f"Tag: {self.tag.get()} advantage = {self.advantage}")
    
    def update_disadvantage(self):
        if self.disadvantage_state.get():
            self.disadvantage = True
            self.advantage = False
            self.advantage_state.set(0)
            print(f"Tag: {self.tag.get()} disadvantage = {self.disadvantage}")
        else:
            self.disadvantage = False
            print(f"Tag: {self.tag.get()} disadvantage = {self.disadvantage}")

    def update_tag(self, event=None):
        self.tag.set(self.tag_field.get())
    
    # adding the update_throw_value method
    def update_throw_value(self, value):
        self.throw.set(str(value))
    
# create two Character objects
characters = [Character(), Character()]

characters[1].tag_field.place(x=110 + 60, y=10)
characters[1].modifier_menu.place(x=107.5 + 60, y=45)
characters[1].advantage_label.place(x=100 + 60, y=80)
characters[1].advantage_check_label.place(x=132.5 + 60, y=95)
characters[1].advantage_check.place(x=127.5 + 60, y=115)
characters[1].disadvantage_check_label.place(x=112.5 + 60, y=95)
characters[1].disadvantage_check.place(x=107.5 + 60, y=115)
characters[1].throw_menu.place(x=102.5 + 60, y=150)

def position_characters():
    global characters
    x_offset = 0
    for i, character in enumerate(characters):
        character.tag_field.place(x=110 + x_offset, y=10)
        x_offset += 60

def roll():
    for character in characters:
        tag_value = character.tag.get()
        modifier_value = int(character.modifier.get())
        throw_value = int(character.throw.get())
        
        if throw_value == 0:
            throw_value = random.randint(1, 20)
            if character.advantage:
                throw_value = max(random.randint(1, 20), random.randint(1, 20))
            elif character.disadvantage:
                throw_value = min(random.randint(1, 20), random.randint(1, 20))
        character.update_throw_value(throw_value)
        
        result = modifier_value + throw_value
        sequence.append([result, tag_value])
        
        print("Rolling for tag:", tag_value," / modifier:", modifier_value, " / Throwing with value:", throw_value, " / Result: ", result)

    def resolve_all_ties(sequence):
        i = 0
        while i < len(sequence) - 1:
            start_of_tie = i
            # move i to the end of this tie sequence
            while i + 1 < len(sequence) and sequence[i][0] == sequence[i + 1][0]:
                i += 1
            end_of_tie = i

            # if a tie is detected, resolve it
            if start_of_tie < end_of_tie:
                tied_characters = sequence[start_of_tie:end_of_tie + 1]
                # corrected print statement to show tied characters before reroll
                print(f"Initial tie: {[character[1] for character in tied_characters]}")
            
                # create a new list to store reroll results
                reroll_results = [[random.randint(1, 20), character[1]] for character in tied_characters]
            
                # sort based on reroll results
                reroll_results.sort(reverse=True)
                print(f"Rerolling: {[(character[1], character[0]) for character in reroll_results]}")
            
                # update tied characters with reroll results
                sequence[start_of_tie:end_of_tie + 1] = reroll_results

                # move index back to the start of this tie sequence
                i = start_of_tie
            else:
                i += 1

    # sort initial sequence highest to lowest
    sequence.sort(reverse=True, key=lambda x: x[0])
    print("Sequence by Result:")
    for score, character in sequence:
        print(f"{character}: {score}")

    resolve_all_ties(sequence)

    # display the final sequence order by names only
    print("\nFinal sequence after resolving ties:")
    for _, character in sequence:
        print(character)
    
    sequence_string = ""
    for _, character in sequence:
        sequence_string += character + " , "
    sequence_field.insert(0, sequence_string)
    
def add_character():
    global window_width, characters, sequence_field_width
    if len(characters) < 27:
        for i in range(0, 3):
            window_width += 60
            sequence_field_width += 5  # increase by 5 when adding a character
            sequence_field.config(width=sequence_field_width)
            # create a new character object and position elements 60 units to the right
            new_character = Character()
            new_character.tag_field.place(x=110 + len(characters) * 60, y=10)
            new_character.modifier_menu.place(x=107.5 + len(characters) * 60, y=45)
            new_character.advantage_label.place(x=100 + len(characters) * 60, y=80)
            new_character.advantage_check_label.place(x=132.5 + len(characters) * 60, y=95)
            new_character.advantage_check.place(x=127.5 + len(characters) * 60, y=115)
            new_character.disadvantage_check_label.place(x=112.5 + len(characters) * 60, y=95)
            new_character.disadvantage_check.place(x=107.5 + len(characters) * 60, y=115)
            new_character.throw_menu.place(x=102.5 + len(characters) * 60, y=150)
            characters.append(new_character)

    elif len(characters) >= 27 and len(characters) < 29:
        window_width += 60
        sequence_field_width += 5
        sequence_field.config(width=sequence_field_width)
        new_character = Character()
        new_character.tag_field.place(x=110 + len(characters) * 60, y=10)
        new_character.modifier_menu.place(x=107.5 + len(characters) * 60, y=45)
        new_character.advantage_label.place(x=100 + len(characters) * 60, y=80)
        new_character.advantage_check_label.place(x=132.5 + len(characters) * 60, y=95)
        new_character.advantage_check.place(x=127.5 + len(characters) * 60, y=115)
        new_character.disadvantage_check_label.place(x=112.5 + len(characters) * 60, y=95)
        new_character.disadvantage_check.place(x=107.5 + len(characters) * 60, y=115)
        new_character.throw_menu.place(x=102.5 + len(characters) * 60, y=150)
        characters.append(new_character)
            
    position_characters()
    print("Characters: ", len(characters))   
    center_window(window_width, window_height)

def remove_character():
    global window_width, characters, sequence_field_width
    if len(characters) > 2:
        window_width -= 60
        sequence_field_width = max(5, sequence_field_width - 5)  # decrease by 5 but minimum width is 5
        sequence_field.config(width=sequence_field_width)
        # remove the latest Character object and adjust positions
        characters[-1].tag_field.place_forget()
        characters[-1].modifier_menu.place_forget()
        characters[-1].advantage_label.place_forget()
        characters[-1].advantage_check_label.place_forget()
        characters[-1].advantage_check.place_forget()
        characters[-1].disadvantage_check_label.place_forget()
        characters[-1].disadvantage_check.place_forget()
        characters[-1].throw_menu.place_forget()
        
        characters.pop()
        position_characters()
        print("Characters: ", len(characters)) 
        center_window(window_width, window_height)
    else:
        print("Cannot remove more characters, there are only 2 characters present.")

def reset():
    for character in characters:
        #character.tag_field.delete(0, tk.END)
        #character.modifier.set('0')
        character.throw.set('0')
        #character.advantage = False
        #character.disadvantage = False
        #character.advantage_check.deselect()
        #character.disadvantage_check.deselect()
        sequence_field.delete(0, tk.END)
        sequence.clear()
    print("Reset done for all characters!")

    
# global labels, buttons, and input field in the GUI
tag_label = tk.Label(root, text="      TAG     ", fg='black')
tag_label.place(x=5, y=15)

modifier_label = tk.Label(root, text="      MOD     ", fg='black')
modifier_label.place(x=5, y=50)

throw_label = tk.Label(root, text="     THROW    ", fg='black')
throw_label.place(x=2.5, y=157.5)

roll_button = Button(root, text = "     ROLL     ", command=roll)
roll_button.place(x = 2.5, y = 205)

add_button = Button(root, text = "      ADD     ", command=add_character)
add_button.place(x = 95, y = 250)

add_button = Button(root, text = "    REMOVE    ", command=remove_character)
add_button.place(x = 185, y = 250)

close_button = Button(root, text = "     Reset    ", command=reset)
close_button.place(x = 2.5, y = 250)

sequence_field = Entry(root, bd = 5, width = sequence_field_width, font=custom_bold_font)
sequence_field.place(x = 100, y = 200)

root.mainloop()