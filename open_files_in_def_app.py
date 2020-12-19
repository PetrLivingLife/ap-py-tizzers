from os import startfile


# complete path + filename
files_to_open = open(r"d:\temporary indement files\open_files.txt").readlines()

# make them unique
files_to_open = set(files_to_open)

for file in files_to_open:
    print(file)
    startfile(file.strip())
    input("Pres Enter to continue.")
