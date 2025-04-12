#!/bin/bash

# Print a message indicating the build process has started
echo "Compiling C code into libgrayscale.so..."

# Use GCC to compile the C code into a shared object file (.so)
gcc -shared -o libgrayscale.so -fPIC grayscale_filter.c

# Check if the compilation was successful
if [ $? -eq 0 ]; then
  echo "C code compiled successfully into libgrayscale.so"
else
  echo "Error compiling C code"
  exit 1
fi
