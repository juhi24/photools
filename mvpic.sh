#!/bin/bash
# Organize photos
# usage: mvpic.sh [EXIFTOOL_ARGS] SOURCE
# Use file creation date if capture date is missing.
END_PATH='${ShortModel}/%f.%e'
BY_SOFTWARE='-filename<${FileModifyDate}/${Software}/%f.%e'
DATEORIG='-filename<${DateTimeOriginal}'
BY_MODEL=$DATEORIG/$END_PATH
BY_DATEORIG=$DATEORIG'/%f.%e'
BY_CREATE='-filename<${CreateDate}/%f.%e'
# Process videos and pictures to their own direcrories.
exiftool -if '$MIMEType=~/video/i' -ext+ AVI -d $HOME/Videot/%Y/%m $BY_CREATE $BY_DATEORIG $@
exiftool -if '$MIMEType!~/video/i' -d $HOME/Kuvat/%Y/%m $BY_SOFWARE $BY_MODEL $@
