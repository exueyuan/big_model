import os


def bytes_to_readable_format(num_bytes):
    """Convert bytes to a more readable format."""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} YB"


def find_largest_files(start_path):
    file_sizes = []

    # Traverse directory and subdirectories
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Get file size and append to list
                size = os.path.getsize(file_path)
                file_sizes.append((file_path, size))
            except OSError as e:
                print(f"Error with file: {file_path}", e)

    # Sort files by size in descending order
    largest_files = sorted(file_sizes, key=lambda x: x[1], reverse=True)

    # Return the top 10 largest files
    return largest_files[:10]


# Specify the directory path here
directory_path = './'

# Find and print the largest files
largest_files = find_largest_files(directory_path)
for file_path, size in largest_files:
    readable_size = bytes_to_readable_format(size)
    print(f"{file_path}: {readable_size}")
