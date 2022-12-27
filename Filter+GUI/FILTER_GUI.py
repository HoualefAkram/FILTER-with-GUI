import shutil
import os
from pathlib import Path
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

sys.setrecursionlimit(999999)

window = Tk()

main_dir, filter_dir, filter_answer = 0, 0, 2


def main_func():
    global main_dir, filter_answer
    main_entry.delete(0, END)
    main_dir = filedialog.askdirectory(title="FILTER")
    main_entry.insert(True, str(main_dir))
    filter_answer = messagebox.askyesno(title="FILTER", message='Deep Filtering?')


def filter_func():
    global filter_dir
    filter_entry.delete(0, END)
    filter_dir = filedialog.askdirectory(title="FILTER")
    filter_entry.insert(True, str(filter_dir))


window.geometry("730x600")
window.config(bg="light yellow")
window.title("FILTER")
photo = PhotoImage(file="image.png")
window.iconphoto(True, photo)
Label(window,
      text="FILTER (by Houalef akram)",  # NOQA
      font=("Ink Free", 30, "bold"),
      bg='light yellow') \
    .place(x=100, y=0)
Label(window,
      text="Main directory",
      bg="light yellow") \
    .place(x=50, y=180)
main_entry = Entry(window,
                   font=('Ariel', 30), )
main_entry.place(y=200, x=50)
find_main = Button(text="Find folder", font=("Ariel", 15), command=main_func)
find_main.place(y=200, x=500)

filter_entry = Entry(window,
                     font=('Ariel', 30))
filter_entry.place(y=300, x=50)
find_filter = Button(text="Find folder", font=('Ariel', 15), command=filter_func)
find_filter.place(y=300, x=500)
Label(window,
      text="Filter directory",
      bg="light yellow") \
    .place(x=50, y=279)
x = IntVar()
radio1 = Radiobutton(text='Copy', variable=x, indicatoron=False, font=("Ariel", 30), value=0)
radio2 = Radiobutton(text='Move', variable=x, indicatoron=False, font=("Ariel", 30), value=1)
radio1.place(x=150, y=370)
radio2.place(x=300, y=370)


def mainfunction():
    global filter_answer, x
    try:
        if main_entry.get().isspace() or main_entry.get() == "":
            messagebox.showerror(title='FILTER', message="Empty Directory!")
            main_func()
        elif filter_entry.get().isspace() or filter_entry.get() == "":
            messagebox.showerror(title='FILTER', message="Empty Directory!")
            filter_func()
        if filter_answer == 2:
            filter_answer = messagebox.askyesno(title="FILTER", message='Deep Filtering?')

        main_directory = str(main_entry.get()).replace("\\", '\\\\')
        filter_directory = str(filter_entry.get()).replace("\\", '\\\\')

        os.mkdir(filter_directory + "/" + "FILTER")
        filter_folder = filter_directory + "/" + "FILTER"

        formats = []
        formats_fold = []
        random_files = []
        random_folder = filter_folder + "/" + "Files Without extension"
        os.mkdir(random_folder)

        if not filter_answer:
            #     quest = input("(copy/move) : ") # quest = radio1/radio2
            for files in os.listdir(main_directory):
                main_main = os.path.join(main_directory, files)
                if os.path.isdir(main_main) is True:
                    formats_fold.append(files)
                if files not in formats_fold and files not in random_files and Path(files).suffix == '':
                    random_files.append(files)
                if files.split('.')[-1] not in formats and files not in formats_fold and Path(
                        files).name not in random_files:
                    formats.append(files.split('.')[-1])
                    os.mkdir(filter_folder + "/" + files.split('.')[-1])
                    os.access(main_directory, os.W_OK)
                final_folder = filter_folder + "/" + files.split('.')[-1]

                if x.get() == 1 and files not in formats_fold and files not in random_files:
                    shutil.move(f"{main_directory}\\{files}", final_folder)

                elif x.get() == 0 and files not in formats_fold and files not in random_files:
                    shutil.copy(f"{main_directory}\\{files}", final_folder)

                if x.get() == 0 and files not in formats_fold and files in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.copy(f"{main_directory}\\{files}", random_folder)
                if x.get() == 1 and files not in formats_fold and files in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.move(f"{main_directory}\\{files}", random_folder)

        if filter_answer:
            for files in Path(main_directory).glob("**/*"):
                if os.path.isdir(Path(files)):
                    formats_fold.append(files.name)
                if os.path.isfile(Path(files)) and Path(files).name not in random_files and Path(files).suffix == '':
                    random_files.append(files.name)

                if files.name not in formats_fold and files.name.split('.')[
                    -1] not in formats and files.name not in random_files:
                    formats.append(files.name.split('.')[-1])
                    os.mkdir(filter_folder + "/" + files.name.split('.')[-1])
                    os.access(main_directory, os.W_OK)
                final_folder = filter_folder + "/" + files.name.split('.')[-1]
                if x.get() == 0 and files.name not in formats_fold and files.name not in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.copy(Path(files), final_folder)
                if x.get() == 1 and files.name not in formats_fold and files.name not in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.move(str(files), str(final_folder))

                if x.get() == 0 and files.name not in formats_fold and files.name in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.copy(str(files), str(random_folder))
                if x.get() == 1 and files.name not in formats_fold and files.name in random_files:
                    os.access(Path(files), os.W_OK)
                    shutil.move(str(files), str(random_folder))

        if not random_files:
            shutil.rmtree(random_folder)
    except FileNotFoundError as err:
        messagebox.showerror(title="FILTER", message=str(err))
    except FileExistsError as err2:
        messagebox.showerror(title="FILTER", message=str(err2))


start_button = Button(text='Start', font=("Ariel", 20, "bold"), command=mainfunction)
start_button.place(x=30, y=480)

window.mainloop()
