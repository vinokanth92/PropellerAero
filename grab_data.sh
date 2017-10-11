# #Shell script for the PropellerAero coding challenge
# Driver shell script
# V Vinokanth
# Last modified 7/10/17

#Terminate upon error
set -e

echo "START OF SCRIPT"

#Check for required number of input arguments
if [[ $# -ne 3 ]]; then
    echo "The script requires 3 arguments to run."
    echo "USAGE: bash ./grab_data.sh <BASE_STATION_ID> <START_TIME> <END_TIME>"
    echo "Please refer to the README file for more information. Aborting script now. Please try again."
    exit 1
fi 

#Defining the 3 command line input parameters
BASE_STATION_ID=$1 
START_TIME=$2
END_TIME=$3

#Make directory to store downloaded files 
mkdir -p $PWD/Downloads

#Get Python execution path
PYTHON_PATH=$(which python3)
$PYTHON_PATH generateOutput.py $BASE_STATION_ID $START_TIME $END_TIME

cd ./Downloads
#teqc=/Users/Vino/Downloads/teqc

if [ "$(ls -A $DIR)" ]; then

    #There are input files. Process them
    for file in "file_*.o"; do 
        teqc $file >> RINEX_OUT.o
    done

    echo "Appending RINEX files"
    echo "Output file RINEX_OUT.o is at ./Downloads/RINEX_OUT.o"

else
    echo "No input files to process. Aborting script."
fi

echo "END OF SCRIPT"

