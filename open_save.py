from tkinter import *
from tkinter.simpledialog import askstring, askinteger, askfloat
import numpy as np
import os
from tkinter import filedialog
from tkinter import messagebox
from spectral.io.envi import *
import spectral.io.envi as envi
from spectral import imshow
import os
import functools
import Hyspeclib.hyspeclib as hy

# Check if the function is called

def calltracker(func):
    @functools.wraps(func)
    def wrapper(*args):
        wrapper.has_been_called = True
        return func(*args)
    wrapper.has_been_called = False
    return wrapper


@calltracker

# Open a file by browsing

def open_file():
    open_file.has_been_called = True
    filedialog.askopenfilename.has_been_called = True
    file_name = filedialog.askopenfilename(initialdir=os.path.expanduser("/"), filetypes=(("ENVI", "*.envi"), ("All files", "*")))
    if str(file_name).endswith(".envi"):
        img = envi.open(file_name + ".hdr", file_name + ".envi")
    else:
        img = envi.open(file_name + ".hdr", file_name)
    file_save = file_name.split('/')
    file_save = file_save[:-1]
    save_dir = ""
    for string in file_save:
        save_dir = save_dir + string + "/"
    print(save_dir)
    filedialog.askopenfilename.has_been_called = False
    imshow.has_been_called = True
    imshow(img, bands=(55, 32, 20), aspect=0.45, stretch=0.25)
    print(img)
    print(file_name)
    noisy_bands_info = hy.noise_removal(file_name, min_threshold=0, max_threshold=0.55)
    noisy_bands_info.reflectance_plot()
    print("--------- List of noisy bands ---------")
    x = noisy_bands_info.show_noisy_bands_with_min_max()
    print(len(x))
    for values in x:
        print(values)
    nb = noisy_bands_info.show_noisy_bands()
    pre = hy.preprocessing(img_path=file_name.split(".")[0] + ".hdr", save_directory=save_dir, available_memory_gb=8)
    pre.perform(ndvi_threshold=125, data_ignore_value=-9999.0, NIR=90, RED=55, min_threshold=0, max_threshold=0.55, noisy_bands=nb)
    file2_header = file_name + "_part_1"
    pre_image = envi.open(file2_header+".hdr",file2_header)
    imshow(pre_image, bands=(55, 32, 20), aspect=0.45, stretch=0.25)
    imshow.has_been_called = True
    print(pre_image)
    if imshow.has_been_called == False and filedialog.askopenfilename.has_been_called == False:
        open_file.has_been_called = False





def open_band():
    file_name = filedialog.askopenfilename(initialdir=os.path.expanduser("/"), filetypes=(("ENVI", "*.envi"), ("All files", "*")))
    if str(file_name).endswith(".envi"):
        img = envi.open(file_name + ".hdr", file_name + ".envi")
    else:
        img = envi.open(file_name + ".hdr", file_name)

    def ret(x, y, z, s, a):
        return x, y, z, s, a

    x, y, z, stretch, aspect = ret(int(input("x: ")), int(input("y: ")), int(input("z: ")), int(input("stretch:")), int(input("aspect: ")))

    open_band.has_been_called = True
    imshow(img, bands=(x, y, z), aspect=aspect, stretch=stretch)
    print(img)

# Save an opened file

def save():
    file_name = filedialog.askopenfilename(initialdir=os.path.expanduser("/"), filetypes=(("ENVI", "*.envi"), ("All files", "*")))
    save_dir = filedialog.askdirectory()
    myfile = envi.open(file_name + ".hdr")
    imageArray = 10000 * myfile[:, :, :]
    save_file = envi.save_image(save_dir + file_name.split("/")[-1] + ".hdr", imageArray, dtype=np.int16, metadata=myfile.metadata, force=True)
    return save_file

