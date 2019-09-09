# This script enables the heuristica font on the blang/latex docker container
# WARNING This needs to be run from the directory where the fonts are located
# Written by Simon M Mudd
# 24-March-2019

# Figure out where we are
thisdir="$PWD"
echo "We are here:"
echo $thisdir

# Get the destination directory
destdir="/usr/share/fonts/opentype/heuristica/"
echo "Destdir is"
echo $destdir

# Make the directory if it doesnt exist
if [ ! -d "$destdir" ]
then
    echo "Making the font directory"
    mkdir $destdir
else
    echo "Directory exists"
fi



bf="Heuristica-Bold.otf"
bif="Heuristica-BoldItalic.otf"
if="Heuristica-Italic.otf"
rf="Heuristica-Regular.otf"

echo $thisdir/$bf

echo "Copying files"
if [ ! -f "$destdir$bf" ]
then
  cp $thisdir/$bf $destdir$bf
fi
if [ ! -f "$destdir$bif" ]
then
  cp $thisdir/$bif $destdir$bif
fi
if [ ! -f "$destdir$if" ]
then
  cp $thisdir/$if $destdir$if
fi
if [ ! -f "$destdir$rf" ]
then
  cp $thisdir/$rf $destdir$rf
fi

# Now register the fonts
fc-cache -f

# Now check on fonts
fc-list | grep Heuristica
