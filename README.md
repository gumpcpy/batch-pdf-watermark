# Batch Add Watermark to PDF Watermark (Qt)

## Description
Qt Python App

Usage: When One PDF File Needs To Give To Several Departments. You Want To Put Each Department's Name On That PDF File Before Sending To Them.

Input a TXT file with watermark content,
Input a PDF file needed to add watermark,
Then this app will generate watermark content on PDF file.
For example, if I have 3 names to put to PDF file, 
I will wrtie their names each line put one name,
Ex. name.txt
Andy
Sally
John
And save this file as a txt file.


## Release Date
2023 07 20
Python Version = 3.11.0

## Develope Steps
### 1
Create and cd a folder for your work: Ex. app_PDFwatermark
### 2 
    conda create -n qtwater python=3.11
### 3
    conda activate qtwater
### 4
    pip install pyinstaller
    pip install PyQt5
    pip install PyPDF2
    pip install reportlab


### 5
    Write your main logic not including your Qt first. Makes things easy.
    File Structure suggestion:
    1. test.py => write your logic and can run without error
    2. origin_layout.ui
    3. origin_layout.py
    4. logo.ico
    5. README.md        
    6. main.py => App entry and style sheet for Qt
    7. layout.py => all original_layout will copy to this file and change some structure
    8. core.py => change to class structure from test.py
    9. Settings.ini => To remember the last used path

### 6
Download UI Designer

https://build-system.fman.io/qt-designer-download

Qt Designer.dmg

### 7
Using Qt Designer to create UI

Then Export orig_layout.ui to orig_layout.py by

    pyuic5 orig_layout.ui -o orig_layout.py

### 8
When you finish your coding, put a logo.ico into your folder 

then pack into an app by

    pyinstaller --windowed --onefile --icon=logo.ico --add-data="logo.png:img" --clean --noconfirm main.py  -n BatchWatermarkToPDF
   

### 9
inside the dist folder are your app. 

Copy dist/BatchWatermarkToPDF, STHeiti.ttc, Setting.ini files to Other.

## GitHub
cd to the folder your code located: app_BatchWatermarkToPDF

    git init

edit .gitignore

    git add .
    git commit -m "First Commit"

Create Remote Repository    
https://github.com/gumpcpy/app_BatchWatermarkToPDF.git

Connect Local to Remote
 
    git remote add origin https://github.com/gumpcpy/app_BatchWatermarkToPDF.git
    git branch -M main
### After Change: 
    git push -u origin main 
****
## Screenshots
<img width="644" alt="pic1" src="https://github.com/gumpcpy/app_BatchWatermarkToPDF/blob/main/pic1.png?raw=true">

<img width="656" alt="pic2" src="https://github.com/gumpcpy/app_BatchWatermarkToPDF/blob/main/pic2.png?raw=true">


