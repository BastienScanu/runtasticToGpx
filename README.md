# runtasticToGpx
 A simple script to convert the .json files exported from Runtastic to .gpx files

## Requirements
You need to have [Python3](https://www.python.org/download/releases/3.0/) installed on your computer

## Setup
First you have to download all your data from Runtastic website, and unzip it.
When the folder `export-YYYYMMDD-000` is extracted, rename it `data`, and paste it in the same directory as the `toGpx.py` file.
Finally run the command:

```
python3 toGpx.py
```
The script will create all the gpx files in the same folder.
