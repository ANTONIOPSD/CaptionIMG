import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Listbox
from PIL import Image, ImageTk
import re

Image.MAX_IMAGE_PIXELS = None

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key = alphanum_key)

class ImageDescriptor:
    def __init__(self, root):
        
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        #self.root.wm_attributes('-toolwindow', 'True')
        self.root.title("CaptionIMG by ANTONIOPS")
        self.root.geometry(f"{int(screen_width/1.5)}x{int(screen_height/1.5)}")
        self.root.resizable(False,False)
        
        self.frame_list = tk.Frame(self.root)
        self.frame_list.pack(side='left', fill='y')
        
        self.image_list = Listbox(self.frame_list, width=30)
        
        self.image_list.bind('<<ListboxSelect>>', self.load_image)
        
        self.horizontal_scrollbar = tk.Scrollbar(self.frame_list, orient='horizontal')
        self.horizontal_scrollbar.pack(side='bottom', fill='x')
        self.horizontal_scrollbar.config(command=self.image_list.xview)
        self.image_list.config(xscrollcommand=self.horizontal_scrollbar.set)
        
        self.vertical_scrollbar = tk.Scrollbar(self.frame_list, orient='vertical')
        self.vertical_scrollbar.pack(side='right', fill='y')
        self.vertical_scrollbar.config(command=self.image_list.yview)
        self.image_list.config(yscrollcommand=self.vertical_scrollbar.set)
        
        self.image_list.pack(side='left', fill='both')
        self.image_label = tk.Label(self.root)
        self.image_label.pack(side='top', anchor='center', expand=True)
        
        self.text_entry = tk.Text(self.root, height=6, width=85, wrap='word')
        self.text_entry.config(borderwidth=5, relief="groove")
        self.text_entry.pack(side='bottom', fill='both')
        
        self.save_button = tk.Button(self.root, text="Save Captions", command=self.save)
        self.save_button.pack(side='bottom')
        
        self.open_button = tk.Button(self.root, text="Open Images", command=self.open_images)
        self.open_button.pack(side='bottom')
    
    def open_images(self):
        try:
            file_types = "*.bmp *.jpg *.jpeg *.png"
            file_paths = filedialog.askopenfilenames(filetypes=[("Common Image Files", file_types), ("All", "*.*")])
            file_paths = natural_sort(file_paths)
            if file_paths:
                self.image_list.delete('0','end')
                self.file_map = {}
                for file_path in file_paths:
                    file_name = file_path.split("/")[-1]
                    self.file_map[file_name] = file_path
                    self.image_list.insert('end', file_name)
        except:
            pass
    
    def load_image(self, event):
        try:
            selection = self.image_list.curselection()
            if not selection:
                return

            self.text_entry.delete(1.0, 'end')
            index = selection[0]
            file_name = self.image_list.get(index)
            file_path = self.file_map[file_name]
            self.current_image = file_name
            self.current_image_path = file_path
            

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            max_size = int(screen_width/2), int(screen_height/2.1)

            image = Image.open(file_path)

            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            new_width, new_height = max_size

            if original_width > original_height:
                new_height = int(new_width / aspect_ratio)
            else:
                new_width = int(new_height * aspect_ratio)

            if new_width > max_size[0]:
                new_width = max_size[0]
                new_height = int(new_width / aspect_ratio)
            if new_height > max_size[1]:
                new_height = max_size[1]
                new_width = int(new_height * aspect_ratio)

            image = image.resize((new_width, new_height), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image)
            self.image_label.image = image
            self.image_label.config(borderwidth=5, relief="groove")

            description_file = str(self.current_image_path).rsplit('.', 1)[0] + ".txt"
            
            with open(description_file, "r") as file:
                description = file.read()
                self.text_entry.insert(1.0, description)
        except:
            pass

    def save(self):
        try:
            description = self.text_entry.get(1.0, 'end')
            description_file = str(self.current_image_path).rsplit('.', 1)[0] + ".txt"
            with open(description_file, "w") as file:
                file.write(description)
            messagebox.showinfo("Success", f"Captions saved successfully at {description_file}")
        except:
            messagebox.showinfo("Error", f"There was an error while saving the captions")


root = tk.Tk()
app = ImageDescriptor(root)
root.mainloop()
