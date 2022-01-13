#!/bin/bash

working_dir=/config/www/version.php

echo `cat $working_dir`

#wget --mirror --no-directories  --no-verbose --directory-prefix=/config/www/`cat $working_dir` --input-file=/config/www/input.txt
aria2c --file-allocation=none --allow-overwrite -c -x 10 -s 10 -d "/config/www/`cat $working_dir`" -i "/config/www/input.txt"
