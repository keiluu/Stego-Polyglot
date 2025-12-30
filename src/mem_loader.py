import os, sys, base64

def load_and_exec(src_bytes):
    fd = os.memfd_create("inmem", flags=0) # File descriptor to load into memory
    
    view = memoryview(src_bytes) # This section copies the bytes from the binary into memory
    while view:
        n = os.write(fd, view)
        view = view[n:]

    os.fexecve(fd, ["inmem"], os.environ) # Execute the loaded binary



