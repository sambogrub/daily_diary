# import tkinter as tk

# def show_frame1():
#     frame1.tkraise()

# def show_frame2():
#     frame2.tkraise()

# # Create the main window
# root = tk.Tk()
# root.geometry('200x200')

# # Create two frames
# frame1 = tk.Frame(root, borderwidth=2, relief = 'groove')
# frame2 = tk.Frame(root, borderwidth = 2, relief = 'groove')

# # Add some widgets to the frames (for demonstration)
# label1 = tk.Label(frame1, text="This is Frame 1")
# label1.place(x=0, y = 0, relwidth = 1, relheight=1)
# label2 = tk.Label(frame2, text="This is Frame 2")
# label2.place(x = 0, y = 0, relwidth=1, relheight=1)

# # Place the frames in the main window (you might use pack or grid here)
# frame1.place(x = 0, y = 0, relwidth= 1, relheight=.5)
# frame2.place(x = 0, y = 0, relwidth= 1, relheight=.5)

# # Create buttons to switch between frames
# button1 = tk.Button(root, text="Show Frame 1", command=show_frame1)
# button1.place(relx = .1, rely = .55, relwidth=.8, height =35)
# button2 = tk.Button(root, text="Show Frame 2", command=show_frame2)
# button2.place(relx =.1, rely = .75, relwidth = .8, height = 35)

# # Initially show frame1
# show_frame1()

# root.mainloop()




column = 0
row = 0

for i in range(10):
    print(column, row)
    row = row if column < 3 else row +1
    column = column +1 if column < 3 else 0

    