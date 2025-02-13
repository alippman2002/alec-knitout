# Update knitout file header
def write_header():
    command_list = []
    command_list.append(';!knitout-2')
    command_list.append(';;Machine: SWGN2')
    command_list.append(';;Carriers: 1 2 3 4 5 6 7 8 9 10')
    command_list.append(';;Positiion: Right')
    # Add Code For Knitout Headers!
    return command_list

# Write knitout operations
def commands(command_list):
    # Insert Code Writing Commands!
    command_list.append('knit + f30 2')
    command_list.append('knit + b31 2')
    return command_list

#Write knitout file name
def setup():
    file = input("Enter the base name for your file (without extension): ")
    file = file + ".k"
    return file

# Write operations to new file
def main():
    file_str = setup()
    command_list = write_header()
    commands(command_list)    
    # Iterate through command list to write to .k file
    with open(file_str, 'w') as f:
        for operation in command_list:
            f.write(operation + "\n")

if __name__ == "__main__":
    main()
