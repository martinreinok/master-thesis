import re

# Define the pattern to search for
pattern = r"Prediction: (\d+\.\d+) seconds"

# Open the input file in read mode
with open("cnn-manual-evaluation.ipynb", "r") as input_file:
    # Read all lines from the input file
    lines = input_file.readlines()

# Open the output file in write mode
with open("output_file.txt", "w") as output_file:
    # Iterate through each line
    for line in lines:
        # Search for the pattern in the line
        match = re.search(pattern, line)
        # If a match is found
        if match:
            # Extract the time from the match
            time = match.group(1)
            # Write the time to the output file
            output_file.write(time + "\n")

print("Extraction completed. Times saved to output_file.txt")