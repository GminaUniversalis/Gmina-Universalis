import os

# Function to read file content
def read_file(file_name, encoding='utf-8'):
    try:
        with open(file_name, 'r', encoding=encoding) as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"Could not read file {file_name} as {encoding}. Trying to read as latin-1.")
        with open(file_name, 'r', encoding='latin-1') as file:
            content = file.read()
    return content

# Function to save content to a new file
def save_file(file_name, content, encoding='windows-1252'):
    with open(file_name, 'w', encoding=encoding, errors='ignore') as file:
        file.write(content)

# Function to reread file content
def reread_file(file_name, encoding='windows-1252'):
    with open(file_name, 'r', encoding=encoding) as file:
        content = file.read()
    return content

# List all files in the current directory
files = os.listdir()

for file_name in files:
    if os.path.isfile(file_name) and not file_name.endswith('.py'):  
        new_file_name = "nowy_" + file_name
        
        save_file(new_file_name, "", encoding='windows-1252')
        print("New file", new_file_name, "created.")

        new_content = reread_file(new_file_name)
        print("New file", new_file_name, "read.")
        
        old_content = read_file(file_name)
        print("Old file", file_name, "read.")
        
        save_file(new_file_name, old_content + new_content, encoding='windows-1252')
        print("New file", new_file_name, "updated with content from", file_name)
        
        os.remove(file_name)
        print("Old file", file_name, "removed.")

# Change file names, remove "nowy_" prefix
for file_name in os.listdir():
    if file_name.startswith("nowy_"):
        new_file_name = file_name.replace("nowy_", "")
        os.rename(file_name, new_file_name)
        print("Changed file name from", file_name, "to", new_file_name)

print("Process completed. Old files have been replaced with new ones.")
