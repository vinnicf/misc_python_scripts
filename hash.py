import hashlib

# Start with the string "CitricSheep"
s = "CitricSheep"

# Use the ASCII values of each character in the string and generate a list of these values
ascii_values = [ord(c) for c in s]

# Multiply each value in the list by the number of characters in the string
multiplied_values = [val * len(s) for val in ascii_values]

# Find the sum of all numbers in the resulting list
total_sum = sum(multiplied_values)

# Use this sum to generate a SHA256 hash
hash_object = hashlib.sha256(str(total_sum).encode())

# Convert this hash to a hexadecimal string
hex_dig = hash_object.hexdigest()

print(hex_dig)
