from tkinter.filedialog import askopenfilename
import framer
from tkinter import *
from tkinter import messagebox

# Window Characteristics
top = Tk()
top.title("Canny Edge Detection")
top.geometry("700x700")
output_path = ""
input_path = ""

# Button Functionalities
def import_video():
    global input_path
    input_path = askopenfilename()
    print (input_path)

def export_video():
    global output_path
    output_path = filedialog.askdirectory()
    print (output_path)

def detect_edges():
    global output_path
    global input_path
    if (output_path != ""):
        status = Label(top, text="Processing… Please wait… Might take a while…", bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)
        messagebox.showinfo( "Processing", "Your Video is Being Processed! This might take some time")
        framer.execute(input_path, output_path)
        msg  = "You can find your Video in " + output_path
        messagebox.showinfo( "You're Video is Done!", msg)

# UI features
import_button = Button(top, text = "Import Video", command = import_video)
import_button.place(x = 200,y = 75)
export_button = Button(top, text = "Export Directory", command = export_video)
export_button.place(x = 400,y = 75)
canny_button = Button(top, text = "Preform Canny Edge Detection", command = detect_edges)
canny_button.place(x = 250,y = 250)

top.mainloop()
