# Auto_GoogleDrive_Downloads
Python Automation script to download file/files from Google drive with the help of file URL(for single file)/ 
link of Spreadsheet on google drive consisting of files URLs in case of multiple files.

### Requirements 
#### -Python3
#### -Modules: webbrowser, logging, argparse,pandas

### Usage
Command line arguments to download Single file from google drive with Link/URL:

python auto_download.py --file_link <file_link>

Example:python auto_download.py --file_link https://drive.google.com/file/d/1ELFoAY5e423yt0PgzzBVlspEDy7TUhke/view?usp=sharing


Command line arguments to download multiple files from google drive, with Link to spreadsheet on drive 
which has files link(The sheet could be genertaed with help of Google Apps Script):

python auto_download.py --spreadsheet <spreadsheet_link>

Example:auto_download.py --spreadsheet https://docs.google.com/spreadsheets/d/1ZmjlFlHx-RY19apRQt1mUUg2i-hSti2iFNxLT96Pxws/edit?usp=sharing

Command line arguments to Run tests on each functionalities of the script: 
python auto_download.py --test True

