import csv
import datetime
import hashlib
import os
import sys
import threading
from pathlib import Path

file_data = []
thread_outputs = []


def file_data_get(file_paths, root, output):
    directory_data = [root]
    print(root)
    for i in file_paths:
        try:
            size = file_sizer(i)
        except OSError:
            return 0
        if size == 0:
            file_data.append([root])
            return 0
        try:
            timestamp = time_stamps(i)
        except OSError:
            timestamp = ""
        try:
            hashed = sha256sum(i)
        except PermissionError:
            hashed = ""
        data = str(hashed) + str(size) + str(timestamp)
        data = str.encode(data)
        data = hashlib.md5(data).hexdigest()
        directory_data.append(i)
        directory_data.append(data)
    output.append(directory_data)
    return file_sizer(root)


def sha256sum(filename):
    BUF_SIZE = 65536  # reads stuff in 64kb chunks for mem management
    hashing_type = hashlib.sha256()  # using sha256 hashing, as recommended by google
    try:
        f = open(filename, 'rb')  # opens the file as a binary for multifile use, and as readable
    except FileNotFoundError or OSError:
        return "Error"
    while True:
        data = f.read(BUF_SIZE)  # this entire while loop reads the file in BUF_SIZE chunks and updates the hashing object with each chunk for mem managing
        if not data:
            break
        hashing_type.update(data)
    f.close()
    return hashing_type.hexdigest()  # converts to hex instead of binary
# stole this from https://stackoverflow.com/questions/22058048/hashing-a-file-in-python ^^^ still gonna explain it, as its pretty smart imp


def file_sizer(filepath):
    try:
        return Path(filepath).stat().st_size  # https://stackoverflow.com/questions/6591931/getting-file-size-in-python like in timestamps, but with size
    except FileNotFoundError or PermissionError:
        return


def time_stamps(filepath):
    try:
        filepath = Path(filepath)
        filetime = datetime.datetime.fromtimestamp(filepath.stat().st_ctime)  # https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python self-explanatory
        return filetime
    except FileNotFoundError or PermissionError:
        return


def write_to_file(usecase, data, data2, save_loc):
    if usecase == "date":
        usecase = datetime.date.today().strftime("%b-%d-%Y")
    else:
        usecase = "current"
    with open(save_loc + "Backup(" + usecase + ").csv", mode="w") as f:
        f_writer = csv.writer(f, delimiter=",", quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for x in data2:
            if len(x) != 0:
                f_writer.writerow(x)
        for x in data:
            if len(x) != 0:
                f_writer.writerow(x)


def thread_function(rootdir, adder, output, user=""):
    for root, dirs, files in os.walk(rootdir):  # change this to whatever directory u want
        index = -1
        breaker = 0
        for x in root:
            index += 1
            if x == user:
                breaker = 1
                break
        index = -1
        if breaker:
            break
        for v in files:
            index += 1
            v = root + adder + v
            files[index] = v
        file_data_get(files, root, output)


def main(save_loc, usage="date"):
    if sys.platform == "win32":
        adder = "\\"
        rootdir = "C:\\"
        userdir = "C:\\Users\\"
    else:
        adder = "/"
        rootdir = adder
        userdir = "/home/"
    thread1 = threading.Thread(target=thread_function, args=(rootdir, adder, thread_outputs, userdir))
    thread2 = threading.Thread(target=thread_function, args=(userdir, adder, file_data, ""))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    write_to_file(usage, file_data, thread_outputs, save_loc)
