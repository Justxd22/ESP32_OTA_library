#!/usr/bin/python3

import platform
import sys
import ctypes
import sys
import crccheck

### directly take WPver31.ino.bin
# if len(sys.argv) != 2:
#     print ("Usage: lzss.py infile")
#     sys.exit()

lzss_functions = ctypes.CDLL("./lzss.so")

ifile  = "./WPver31/build/esp32.esp32.esp32/WPver31.ino.bin"
name = "WPver31"
ofile  = "t.lzss"

b_ifile = ifile.encode('utf-8')
b_ofile = ofile.encode('utf-8')

lzss_functions.encode_file.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lzss_functions.encode_file(b_ifile, b_ofile)




ifile = "t.lzss"
ofile = f"{name}.ota"
print(ofile)

# Read the binary file
in_file = open(ifile, "rb")
bin_data = bytearray(in_file.read())
in_file.close()

magic_number = 0x45535033.to_bytes(4,byteorder='little')

version = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40])

# Prepend magic number and version field to payload
bin_data_complete = magic_number + version + bin_data

# Calculate length and CRC32
bin_data_len = len(bin_data_complete)
bin_data_crc = crccheck.crc.Crc32.calc(bin_data_complete)

# Write to outfile
out_file = open(ofile, "wb")
out_file.write((bin_data_len).to_bytes(4,byteorder='little'))
out_file.write((bin_data_crc).to_bytes(4,byteorder='little'))
out_file.write(bin_data_complete)
out_file.close()

