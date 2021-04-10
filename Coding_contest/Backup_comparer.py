import csv


def find_row_diff(row, row2):
    inder = -1
    row.append(0)
    row2.append(0)
    if len(row) > len(row2):
        length = row
        while len(row2) < len(row):
            row2.append("0")
    else:
        length = row2
        while len(row) < len(row2):
            row.append("0")
    adds = []
    dels = []
    mods = []
    while inder < len(length):
        inder += 1
        try:
            row[inder] = row[inder]
        except IndexError:
            break
        if length[inder] == 0:
            break
        if length[inder].startswith(length[0]):
            print("checking...")
            try:
                if row2[inder] not in row:
                    adds.append(row2[inder])
                    print("added " + str(row2[inder]))
                    if row2[inder] not in adds:
                        adds.append(row2[inder])
            except TypeError:
                pass
            try:
                if row[inder] not in row2:
                    dels.append(row[inder])
                    print("deleted " + str(row[inder]))
                    if row[inder] not in dels:
                        dels.append(row[inder])
            except TypeError:
                pass
            if row[inder + 1] != row2[inder + 1] and row[inder] == row2[inder]:
                mods.append(row[inder])
                print(str(row[inder]) + " was modded")
    return adds, dels, mods


def find_subdirs(data, i):
    height = 0
    v = 2
    while 1:
        if data[i + v][0].startswith(data[i][0]):
            height += 1
            v += 2
        else:
            return height


def open_files(file1, file2):  # this is a giant mess
    adds = []
    mods = []
    dels = []
    file1opend = open(file1, mode='r')
    file2opend = open(file2, mode='r')
    file1_reader = csv.reader(file1opend, delimiter=",", quotechar="'")
    file2_reader = csv.reader(file2opend, delimiter=",", quotechar="'")
    index = -2
    index2 = -2
    data1 = list(file1_reader)
    data2 = list(file2_reader)
    max_check = 0
    while max_check != 2 and index < (len(data1) - 2) or index2 < (len(data2) - 2):
        index += 2
        index2 += 2
        try:  # the try statement makes it so that I don't have to manually make it
            row1 = data1[index]
            row2 = data2[index2]
        except IndexError:
            print("error")
            break
        print(row1)
        print(row2)
        if row1[0] == row2[0]:  # this is where stuff gets hard
            print("dirs match")
            max_check = 0
            adder, modder, deller = find_row_diff(row1, row2)
            adds.extend(adder)
            mods.extend(modder)
            dels.extend(deller)
        else:
            if row1 not in data2:
                print("Stuff deleted")
                dels.append(row1[0])
                if data1[index + 2][0].startswith(row1[0]):
                    subdirs = find_subdirs(data1, index)
                    print(str(subdirs) + " subdirs")
                    index += subdirs * 2
                    index2 -= 2
                else:
                    index += 2
            if row2 not in data1:
                print("Stuff added")
                adds.append(row2[0])
                if data2[index2 + 2][0].startswith(row2[0]):
                    subdirs = find_subdirs(data2, index2)
                    print(str(subdirs) + " subdirs")
                    index2 += subdirs * 2
                    index -= 2
                else:
                    index2 += 2
    file1opend.close()
    file2opend.close()
    return adds, dels, mods


def write_to_file(adds, dels, mods, save_loc):
    with open(save_loc + "Comparison.txt", mode="w") as f:
        f.writelines("Added files seen below:\n")
        adds = "\n+ ".join(adds)
        f.write(adds)
        f.write("\n*********************************\nDeleted files:\n")
        dels = "\n- ".join(dels)
        f.write(dels)
        f.write("\n*********************************\nModified files:\n")
        mods = "\n+- ".join(mods)
        f.write(mods)
