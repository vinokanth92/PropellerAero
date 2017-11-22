# #Shell script for the PropellerAero coding challenge
# Wrapper shell script
# V Vinokanth

set -e

echo "START OF SCRIPT"

if [[ $# -ne 3 ]]; then
    echo "The script requires 3 arguments to run."
    echo "USAGE: bash ./grab_data.sh <BASE_STATION_ID> <START_TIME> <END_TIME>"
    echo "Please refer to the README file for more information. Aborting script now. Please try again."
    exit 1
fi

BASE_STATION_ID=$1
START_TIME=$2
END_TIME=$3

mkdir -p $PWD/Downloads

PYTHON_PATH=$(which python3)
$PYTHON_PATH generat_output.py $BASE_STATION_ID $START_TIME $END_TIME

cd ./Downloads

if [ "$(ls -A $DIR)" ]; then

    for file in "file_*.o"; do
        teqc $file >> RINEX_OUT.o
    done

    echo "Appending RINEX files"
    echo "Output file RINEX_OUT.o is at ./Downloads/RINEX_OUT.o"

else
    echo "No input files to process. Aborting script."
fi

echo "END OF SCRIPT"

