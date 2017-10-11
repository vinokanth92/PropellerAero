# Table Of Contents
- 1.0 Introduction
- 2.0 Prerequisite to run the script
- 3.0 Running the script
- 4.0 Outputs

##  1.0 Introduction
This project consists of a set of Bash and Python scripts as a solution to the PropellerAero coding challenge. As defined in the problem statement, the aforementioned scripts achieve the followings;

- Based on the user input, communicate with the NGS/NOAA FTP server to download available hour-based or day-based compressed data files.
- Decompress and append the downloaded data files to generate a RINEX formatted observation file using TEQC command line tool. 

##  2.0 Prerequisite to run the script
- OS requirement: MacOS (tested on macOS Seirra, v10.12 )
- Python 3
- [TEQC](https://www.unavco.org/software/data-processing/teqc/teqc.html), command line tool. **It is imperative that TEQC is in PATH, else the script will fail.**

## 3.0 Running the script

- Clone the git repository
    - `git clone <REPOSITORY_URL>`
- Navigate to the repository
    - `cd PropellerAero`
- Execute the Bash script with the required arguments
    - `bash grab_data.sh <BASE_STATION_ID> <START_TIME> <END_TIME>`
    - Input arguments format
        - `BASE_STATION_ID`, all lowercase string
            - Example, `nybp`
        - `START_TIME` should be of the format `yyyy-mm-ddTh:m:ssZ`
            - Example, `2017-09-14T23:11:22Z`
        - `END_TIME` should be of the format `yyyy-mm-ddTh:m:ssZ`
            - Example, `2017-09-15T01:33:44Z`
    - For example, the script could be run as follows;
        - `bash grab_data nybp 2017-09-14T23:11:22Z 2017-09-15T01:33:44Z`

## 4.0 Outputs
The script outputs a RINEX formatted observation file called *RINEX_OUT.o* at the location `PropellerAero/Downloads` along with other downloaded compressed .gz and uncompressed obsercations files.






