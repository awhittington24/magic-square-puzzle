import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json

# Create a 5x5 array filled with placeholders
array = [['-' for _ in range(5)] for _ in range(5)]
array7 = [['-' for _ in range(7)] for _ in range(7)]

undo_stack = []
level = 1
completed = False

# Place '1' randomly in the array
def place_initial_number():
    random_row = random.randint(0, 4)
    random_col = random.randint(0, 4)
    array[random_row][random_col] = '1'
    undo_stack.append((random_row, random_col, '-'))


place_initial_number()


# Function to display the current state of the array in the GUI
def display_array_gui(array, label):
    text = '\n'.join([' '.join(str(cell) for cell in row) for row in array])
    label.config(text=text)
def display_array7_gui(array,array7, label):
    for row in range(7):
        for col in range(7):
            if 1 <= row <= 5 and 1 <= col <= 5:
                array7[row][col] = array[row - 1][col - 1]
            else:
                array7[row][col] = '-'
    text = '\n'.join([' '.join(str(cell) for cell in row) for row in array7])
    label.config(text=text)

# Function to check if the row and column are adjacent to the predecessor of the number to be entered
def is_adjacent(row, col, predecessor):
    prev_row, prev_col, _ = predecessor
    return abs(row - prev_row) <= 1 and abs(col - prev_col) <= 1


# Function to handle user input
def handle_input(entry_widgets, label, current_num_label,root, undo_button):
        global level, completed

        try:
            row = int(entry_widgets[0].get())
            col = int(entry_widgets[1].get())

            if 0 < row < 6 and 0 < col < 6:
                predecessor = undo_stack[-1]
                if array[row-1][col-1] == '-' and is_adjacent(row, col, predecessor):
                    backup_array = [row[:] for row in array]  # Create a deep copy of the array for undo
                    undo_stack.append((row, col, backup_array))

                    array[row-1][col-1] = str(current_num_label.cget("text"))
                    if level == 1:
                        display_array_gui(array, label)  # Display level one grid
                    else:
                        display_array7_gui(array,array, label)  # Display level two grid
                    # Increment the current number and reset the entry fields
                    if int(current_num_label.cget("text")) < 25:
                        current_num_label.config(text=str(int(current_num_label.cget("text")) + 1))
                        reset_entry(entry_widgets)
                    else:
                        level += 1
                        completed = True
                        messagebox.showinfo("Congratulations", "You've completed the game!")
                        handle2(entry_widgets, label, current_num_label, root, undo_button)

                else:
                    messagebox.showinfo("Error", "Invalid spot. The cell must be adjacent to the predecessor of the number to be entered.")
            else:
                messagebox.showinfo("Error", "Invalid coordinates. Please enter row and column values between 1 and 5.")
        except ValueError:
            messagebox.showinfo("Error", "Invalid input. Please enter a number.")
        finally:
            update_undo_button(undo_button)
def handle2(entry_widgets, label, current_num_label, root, undo_button):
        global level, completed
        try:
            row = int(entry_widgets[0].get())
            col = int(entry_widgets[1].get())
            if 0 < row <= 7 and 0 < col <= 7:
                current_num_label.config(text='2')
                predecessor = undo_stack[-1]
                if array7[row-1][col-1] == '-' and is_adjacent(row, col, predecessor):
                    backup_array = [row[:] for row in array7]  # Create a deep copy of the array for undo
                    undo_stack.append((row, col, backup_array))
                    if 1 <= row <= 5 and 1 <= col <= 5:
                        array7[row ][col] = str(current_num_label.cget('text'))
                        display_array7_gui(array,array7, label)

                    # Increment the current number and reset the entry fields
                    if int(current_num_label.cget("text")) < 25:
                        current_num_label.config(text=str(int(current_num_label.cget("text")) + 1))
                        reset_entry(entry_widgets)
                    else:
                        level += 1
                        completed = True
                        messagebox.showinfo("Congratulations", "You've completed the game!")
                        root.quit()
                else:
                    messagebox.showinfo("Error", "Invalid spot. The cell must be adjacent to the predecessor of the number to be entered.")
            else:
                messagebox.showinfo("Error", "Invalid coordinates. Please enter row and column values between 1 and 7.")
        except ValueError:
            messagebox.showinfo("Error", "Invalid input. Please enter a number.")
        finally:
            update_undo_button(undo_button)



# Function to reset the entry fields after each move
def reset_entry(entry_widgets):
    for entry in entry_widgets:
        entry.delete(0, 'end')


# Function to handle the undo operation
def handle_undo(label, undo_button):
    if len(undo_stack) > 1:
        array = undo_stack[-1][2]
        undo_stack.pop()

        display_array_gui(array, label)
    update_undo_button(undo_button)


# Function to update the state of the undo button
def update_undo_button(undo_button):
    if len(undo_stack) > 1:
        undo_button.config(state="active")
    else:
        undo_button.config(state="disabled")


# Function to save the array to a JSON file
# def save_array_to_json(array, filename):
#     with open(filename, 'w') as file:
#         json.dump(array, file)

# Function to save the array to a JSON file in a user-selected directory
def save_array_to_json(array):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(array, file)
            messagebox.showinfo("Success", "Game saved successfully.")
    except Exception as e:
        messagebox.showinfo("Error", f"Error saving game: {e}")


# Function to load the array from a user-selected JSON file
def load_array_from_json():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                loaded_array = json.load(file)
            # Update the array and undo stack with the loaded values
            global array, undo_stack
            array = loaded_array
            undo_stack = [(row, col, '-') for row in range(5) for col in
                          range(5)]  # Adjust the initial undo stack accordingly
            # Update the displayed GUI
            display_array_gui(array, label)
            update_undo_button(undo_button)
            messagebox.showinfo("Success", "Game loaded successfully.")
    except Exception as e:
        messagebox.showinfo("Error", f"Error loading game: {e}")


# Create the GUI
root = tk.Tk()
root.title("Number Placement Game")

label = tk.Label(root, text="", font=("Courier", 20))
label.pack()

row_label = tk.Label(root, text="Row:")
row_label.pack()
row_entry = tk.Entry(root)
row_entry.pack()

col_label = tk.Label(root, text="Column:")
col_label.pack()
col_entry = tk.Entry(root)
col_entry.pack()

current_num_label = tk.Label(root, text="2")
current_num_label.pack()

submit_button = tk.Button(root, text="Submit",
                          command=lambda: handle_input([row_entry, col_entry], label, current_num_label, root,
                                                       undo_button))
submit_button.pack()

undo_button = tk.Button(root, text="Undo", state="disabled", command=lambda: handle_undo(label, undo_button))
undo_button.pack()

# save_button = tk.Button(root, text="Save", command=lambda: save_array_to_json(array, 'saved_array.json'))
# save_button.pack()
# Update the save button command to prompt the user for a file and save the array
save_button = tk.Button(root, text="Save", command=lambda: save_array_to_json(array))
save_button.pack()

# Add a load button to allow the user to load a saved game
load_button = tk.Button(root, text="Load", command=load_array_from_json)
load_button.pack()

display_array_gui(array, label)
root.mainloop()
display_array7_gui(array, array7, label)
root.mainloop()


