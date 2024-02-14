import os

# Setup:
# Check that directories exist and create them if they don't
# Directories: videos, metadata

DIRECTORIES = ["metadata", "output"]

def setup():
    
    # Check that the expected directories exist, and create them if they don't
    for directory in DIRECTORIES:
        if not os.path.isdir(directory):
            os.mkdir(directory)
