import os, sys, base64, tempfile, math
from PIL import Image

def obtain_bits(value):
    # Returns a list containing the binary representation of a value
    bits = []
    for i in range(7, -1, -1):
        bits.append((value >> i) & 1)
    
    return bits

def obtain_byte(bits):
    # Given a list of bits calculate the decimal value of the corresponding byte
    if len(bits) != 8:
        print("Provided list is not a byte, length != 8")
        return
    
    value = 0
    for b in bits:
        value = 2*value + b
    
    return value


def hide_bits(bits, byte, hide_pattern_list):
    # Hides in the first n bits, as indicated in hide_pattern_list  into byte.
    # Those first n bits are removed from the bits list provided

    bits_from_byte = obtain_bits(byte) # Obtain the binary representation from the byte to overwritte
    updated_byte = []

    for i in range(8):
        if hide_pattern_list[i] == 1:
            updated_byte.append(bits.pop(0))
        else:
            updated_byte.append(bits_from_byte[i])
    
    return obtain_byte(updated_byte)



# This code is used for hiding the binary the rgb values of a JPEG file
def hide_payload(imgFile, payload, hide_pattern):

    # Hide pattern will correspond to a byte whose binary representation indicates which bits from the source image have to be replaced
    # E.g. 0x03 -> 0 0 0 0 0 0 1 1 -> From each byte replace last two bits

    if hide_pattern == 0x00: # The pattern cannot be 0x00 because no bits would be replaced
        print("Error, the provided pattern does not allow hiding")
        return

    with open(payload, "rb") as pd:
        payload_bytes = pd.read()

    payload_len = len(payload_bytes)

    # Calculate how many bytes are needed to encode the payload using the provided hide_pattern

    hide_pattern_list = obtain_bits(hide_pattern) # Store the hide_pattern binary representation in a list

    bits_amount_to_hide = hide_pattern_list.count(1) # Amount of bits to hide in each byte
    hide_amount_bytes = math.ceil(len(pd) * 8 / bits_amount_to_hide) # How many bytes in total are required to hide the complete payload

    with Image.open(imgFile) as img: 
        img = img.convert("RGB")
        img_bytes = bytearray(img.tobytes()) # Obtain a bytearray of RGB values

    if len(img_bytes) < hide_amount_bytes: # Check if there is enough room for storing the hidden payload
        print("The image is not sufficiently big to hide using the currently selected hide pattern. Select a bigger image or modify hide pattern to overwrite more information.")
        return

    bits = [] # Temp array to store the next bits to be hidden
    count_encoded = 0 # Count how many bytes from the payload have been loaded

    byte_to_update = 0 # Indicates which byte from the image has to be modified
    while (count_encoded < payload_len) or (len(bits) > 0): # Keep writting until we have hidden the whole payload

        if (len(bits) < bits_amount_to_hide) and (count_encoded == payload_len): # When we dont have enough bits to fulfill hide_pattern, but all the bytes from the payload have already been loaded, we truncate the hide_pattern
            
            truncated_pattern = [] # Store as many 1 in the pattern as bits are remaining, truncate the rest
            for b in hide_pattern_list:
                if sum(truncated_pattern) < len(bits):
                    truncated_pattern.append(b)
                else:
                    break

            for i in range (8 - len(truncated_pattern)): # Fill the rest of the pattern with 0
                truncated_pattern.append(0)




        while (len(bits) < bits_amount_to_hide) and (count_encoded < payload_len): # If there are not enough bits loaded from the payload to be hidden in the next byte, load more (we can still load more bytes from the payload)
            
            for b in obtain_bits(payload_bytes[0]):
                bits.append(b)
            
            payload_bytes = payload_bytes[1:] # Once we have read a byte, move the cursor to point to the next one
            count_encoded += 1 # Update the counter because we have processed one more byte

        

        updated_byte = hide_bits(bits, img_bytes[byte_to_update], hide_pattern_list)   # Hide bits in the next image byte
        img_bytes[byte_to_update] = updated_byte
        byte_to_update += 1


    out = Image.frombytes("RGB", img.size, bytes(img_bytes))
    out.save("hidden.png")

    




