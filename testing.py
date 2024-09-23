import tkinter as tk

# Toggle button callback function
def toggle_button():
    # Toggle the state variable
    state.set(not state.get())
    # Update button appearance based on the state
    if state.get():
        button.config(text="Active", bg="green")
    else:
        button.config(text="Inactive", bg="red")

# Create the main window
root = tk.Tk()
root.title("Toggle Button Example")

# Define a BooleanVar to keep track of the button state
state = tk.BooleanVar(value=False)

# Create the toggle button
button = tk.Button(root, text="Inactive", bg="red", command=toggle_button)
button.pack(pady=20)

# Run the application
root.mainloop()

    