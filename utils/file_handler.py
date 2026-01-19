# This module handles reading the sales data file with multiple encodings

def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                lines = lines[1:]

                clean_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        clean_lines.append(line)

                return clean_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File not found - {filename}")
            return []

    print("Error: Unable to read file with supported encodings")
    return []
