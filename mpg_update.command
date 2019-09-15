#!/bin/bash

echo “running mpg_extract.py”
cd Documents/Coding/mpgdata/
python3 mpg_extract.py
git add .
git commit -m 'new fillup'
git push
echo "mpg_update.py complete"
exit