name = "main.py"
your = "your id" 
id = "your telegram id" #replacement string

#converting file in array
with open(name, 'r', encoding='UTF-8') as file:
    list_file = file.readlines()

#searching id in file and replace, add in new file array
file_id = []
for line in list_file:
    newline = line.replace(id, your) #replacement takes place here 1 - replacemetn, 2 - replaced by what
    file_id.append(newline)

#replace file on file array
with open(name, 'w', encoding="UTF-8") as new:
    new.writelines(file_id)