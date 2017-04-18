#!/bin/bash

FILENAME=docword.nytimes.txt
echo "Selecting only the first three thousand documents..."
# Deletes the first three lines and from line 3001 to
# the end of the file
sed -e '1,3 d' -e '/^3001 /,$ d' ${FILENAME} > ${FILENAME}_preprocessed.txt

echo "Done!"
