def find_member_offset(file_path, class_name, member_name):
    """
    Finds the offset of a specific member variable within a class.

    Args:
        file_path (str): The path to the file containing class definitions.
        class_name (str): The name of the class to search within.
        member_name (str): The name of the member variable.

    Returns:
        int: The offset of the member variable if found, otherwise None.
    """

    with open(file_path, 'r') as file:
        in_class = False
        for line in file:
            if line.startswith('class ' + class_name):  # Class start
                in_class = True
            elif line.strip() == "-----------":  # Class end
                in_class = False
                break  # Stop parsing once the class ends

            if in_class and line.strip().startswith('//'):  # Member line with comment
                comment = line.split('//')[1]
                if '[Offset:' in comment:
                    offset_str = comment.split('[Offset:')[1].split(',')[0].strip()
                    offset = int(offset_str, 0)  # Convert from hex to integer
                    if member_name in line:  # Check if it's the member we're looking for
                        return offset

    return None  # Member or class not found

# Example Usage
offset = find_member_offset('your_file.txt', 'example', 'example_bool')
if offset is not None:
    print("uintptr_t example = {};".format(offset))
else:
    print("Class or member variable not found.")