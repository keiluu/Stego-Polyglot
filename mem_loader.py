import os, tempfile

def load_and_exec(src_bytes):
    # Takes as argument a bytearray containing a binary and executes it
    fd, path = tempfile.mkstemp(prefix="tmp_file_", dir="/tmp") # Create a temp_file in /tmp to store the binary
    os.fchmod(fd, 0o700) # Add execution permissions
    
    view = memoryview(src_bytes) # This section copies the bytes from our bytearray to the newly created file in /tmp
    while view:
        n = os.write(fd, view)
        view = view[n:]

    os.close(fd)

    # Execute the loaded binary
    os.execve(path, ["tmp_file"], os.environ)


