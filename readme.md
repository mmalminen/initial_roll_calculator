# Initiative Roller

	A simple GUI application for casting turn sequence in tabletop role-playing games, built with Python and Tkinter.

## Features

	- Add and remove characters dynamically
	- Set modifiers and advantage/disadvantage for each character
	- Roll initiative for all characters simultaneously
	- Resolve ties automatically
	- Display the final initiative order


### How to use:

	1. Enter a tag (name or identifier) for each character.
	2. Set the modifier for each character using the dropdown menu.
	3. Check the advantage (+) or disadvantage (-) box if applicable.
	4. Click "Roll d20" to determine the initiative order. The program will only roll for results that would yield a
	   "Throw value" of 0, allowing you to optionally roll with real dice. Set the result of dice rolls using the "Throw
 	   value" dropdown menu before clicking "Roll d20".
	5. The final sequence will be displayed in the text field at the bottom.
	6. Use "ADD" and "REMOVE" buttons to adjust the number of characters.
	7. Click "Reset" to clear all rolls and prepare for a new round.
