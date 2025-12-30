import os, sys, base64, tempfile

def load_and_exec(src_bytes):
    # fd = os.memfd_create("inmem", flags=0) # File descriptor to load into memory
    fd, path = tempfile.mkstemp(prefix="tmp_file_", dir="/tmp")
    os.fchmod(fd, 0o700)
    
    view = memoryview(src_bytes) # This section copies the bytes from the binary into memory
    while view:
        n = os.write(fd, view)
        view = view[n:]

    os.close(fd)

    #os.fexecve(fd, ["inmem"]) # Execute the loaded binary
    os.execve(path, ["tmp_file"], os.environ)


