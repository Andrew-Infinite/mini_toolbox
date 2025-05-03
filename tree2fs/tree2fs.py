import os
import sys

one_for_all_debug_flag = True

def print_2(*args, **kwargs):
    if one_for_all_debug_flag:
        print(*args, **kwargs)
    
# Parse the directory tree structure
def parse_tree_structure(text):
    tree = {}
    lines = text.splitlines()
    path_stack = []  # Stack to keep track of the current directory level
    for line in lines:
        if not line.lstrip("│ └ ├ ─ "):
            continue
        
        # Calculate current indentation level, 1-index
        indent_level = 1 + (len(line) - len(line.lstrip("│ └ ├ ─ "))) // 4
        print_2("indent_level: ",indent_level, line)

        # Get the name of the directory/file
        name = line.strip("│ └ ├ ─ ").strip()
        
        # Remove comment after the file/folder name
        name = name.split(" #")[0].strip()
        print_2("name: ",name)
        
        # Skip empty names
        if not name:
            continue
        
        while len(path_stack) >= indent_level:
            path_stack.pop()
            
        # Create a path based on the stack
        current_path = path_stack + [name]
        print_2("current_path:", current_path)
        
        # Build the tree structure
        current_dict = tree
        print_2("current_dict:", current_dict)
        for part in current_path:
            current_dict = current_dict.setdefault(part, {})
            
        path_stack = current_path  # Update stack on subdirectories
        print_2("path_stack:", path_stack)

        print_2(" ")

    return tree


# Create directories and files from tree structure
def create_structure(base_path, tree):
    print_2(" ")
    for name, value in tree.items():
        path = os.path.join(base_path, name)
        print_2( name, value)
        print_2("")
        
        if isinstance(value, dict):
            
            if name.endswith('/'):
                # Create the directory
                os.makedirs(path, exist_ok=True)
            else:
                # Create the file
                open(path, 'a').close()
            # Recurse to create subfolders/files
            create_structure(path, value)


def main(txt_file):
    try:
        # Create the structure in the same directory as the txt file
        root_path = os.getcwd()
        
        # Read the input text file
        with open(txt_file, 'r', encoding='utf-8') as file:
            tree_input = file.read()
        
        # Parse the structure from the text input
        parsed_tree = parse_tree_structure(tree_input)

        # Create the directories and files
        create_structure(root_path, parsed_tree)
        print(f"Project structure created at {root_path}")

    except FileNotFoundError:
        print(f"Error: The file '{txt_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Check if the user provided a file argument
    if len(sys.argv) != 2:
        print("Usage: python create_project_structure_from_txt.py <path_to_txt_file>")
    else:
        # Get the path to the txt file from the command line argument
        txt_file_path = sys.argv[1]
        main(txt_file_path)
