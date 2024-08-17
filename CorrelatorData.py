import matplotlib . pyplot as plt
import numpy as np
import pandas as pd
import struct
#f = 2500000
#a = 127
f = 2500000
a = 63
sample = 720
theta = 0.00 # np . pi / 2
x = np . arange (0 , sample , 1 )
y_1 = a*np . sin ( 2*np.pi *f*x*( 10**(-9 ) ) + theta )+64#+127
##print ( y_1 )
theta = 0.05
y_2 = a*np . sin ( 2 * np.pi*f*x*(10**(-9)) + theta )+64#+127
#print ( " y_2 data : \n " )
#print ( y_2 )
# print ( y_1 ) # To print the y values
plt . stem (x , y_1 , 'b' , markerfmt = 'bo' , label = " Original " )
plt . stem (x , y_2 , 'g' , markerfmt = 'go' , label = " With delay " )
plt . xlabel ( 'Time ( ns )')
plt . ylabel ( 'Voltage ( V )')
plt . show ()

#np . savetxt ( " y_1.txt " , ( y_1 ) , fmt = " %.0f " ) # two decimal places
#np . savetxt ( " y_2.txt " , ( y_2 ) , fmt = " %.0f " )

#saving into binary, y_1 and y_2

y_1int = y_1.astype(int)
y_2int = y_2.astype(int)

def convert_to_binary_formatted(integer_array, length):
	binary_strings = []
	for integer in integer_array:
	# Convert integer to binary string with zeros up to 'length'
		binary_string = format(abs(integer), f"0{length}b")
		if integer >= 0:			
			binary_string = str(0) + binary_string 
		if integer < 0:
			binary_string = str(1) + binary_string
			
		binary_strings.append(binary_string)

	return binary_strings
	
def save_binary_strings(filename, binary_strings):
  with open(filename, "w") as f:
    for string in binary_strings:
      f.write(string + "\n")
      
def save_array_to_binary_file(array, filename):
	nine_bit_array = array & 0b11111111
	binary_data = struct.pack('>' + 'H' * len(nine_bit_array), *nine_bit_array)
	with open(filename, 'wb') as binary_file:
		binary_file.write(binary_data)
		
		
def floats_to_binary_and_save(array, output_file):
    # Convert floats to integers
    integer_array = array.astype(int)

    # Convert integers to 8-bit binary representation
    binary_array = np.unpackbits(integer_array.view(np.uint8)).reshape(-1, 8)

    # Save binary data to a text file
    with open(output_file, 'w') as file:
        for row in binary_array:
            binary_string = ''.join(map(str, row))
            file.write(binary_string + '\n')

def floats_to_binary_and_save_16bit(array, output_file):
  # Convert floats to 16-bit integers (to ensure 14 bits of precision)
  integer_array = array.astype(np.uint16)

  # Pad with zeros to 16 bits if necessary
  integer_array = np.right_shift(integer_array, 2)  # Shift 2 bits to align with 14 bits

  # Convert integers to 16-bit binary representation
  binary_array = np.unpackbits(integer_array.view(np.uint8)).reshape(-1, 16)

  # Extract only the first 14 bits of each row
  binary_array = binary_array[:, :16]

  # Save binary data to a text file without spaces
  with open(output_file, 'w') as file:
    for row in binary_array:
      binary_string = ''.join(map(str, row))  # Join binary digits without separators
      file.write(binary_string + '\n')
      
def convert_to_binary_and_save(arr, output_file):
    """
    Converts an array of integers to 8-bit binary characters and saves the result in a text file.

    Args:
        arr (list[int]): List of integers to convert.
        output_file (str): Path to the output text file.

    Returns:
        None
    """
    with open(output_file, 'w') as f:
        for num in arr:
            # Convert the number to an integer (if it's a float)
            num = int(num)
            # Handle negative numbers by adding a leading zero
            if num < 0:
                binary_str = format(256 + num, '08b')
            else:
                binary_str = format(num, '08b')
            # Write the binary string to the file
            f.write(binary_str + '\n')
            
def binary_to_hex_and_save(input_file, output_file):
    """
    Reads binary numbers from an input file, converts them to hexadecimal,
    and saves the result in an output text file.

    Args:
        input_file (str): Path to the input text file containing binary numbers.
        output_file (str): Path to the output text file.

    Returns:
        None
    """
    with open(input_file, 'r') as f:
        binary_numbers = f.read().splitlines()

    # Convert binary numbers to hexadecimal
    hex_numbers = [hex(int(num, 2)) for num in binary_numbers]

    # Join the hexadecimal numbers with commas
    result = ', '.join(hex_numbers)

    # Save the result to the output file
    with open(output_file, 'w') as f:
        f.write(result)       
 
convert_to_binary_and_save(y_1, 'y1NEW.txt')
convert_to_binary_and_save(y_2, 'y2NEW.txt')       
binary_to_hex_and_save("y1NEW.txt", "y1HEX.txt")
binary_to_hex_and_save("y2NEW.txt", "y2HEX.txt")          	
#convert_to_binary_and_save(y_1, 'y1NEW.txt')
#convert_to_binary_and_save(y_2, 'y2NEW.txt')

#save_array_to_binary_file(y_1int, 'y1.bin')
#save_array_to_binary_file(y_2int, 'y2.bin')
#y_1_bin = convert_to_binary_formatted(y_1int, 8)
#save_binary_strings("y_1bin.txt", y_1_bin)

#y_2_bin = convert_to_binary_formatted(y_2int, 8)
#save_binary_strings("y_2bin.txt", y_2_bin)
