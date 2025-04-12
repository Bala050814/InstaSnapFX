#!/bin/bash
echo "Compiling C code into libgrayscale.so..."
gcc -shared -o libgrayscale.so -fPIC grayscale_filter.c
