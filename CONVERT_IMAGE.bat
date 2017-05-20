@echo off


if [%1]==[] goto :eof
set n=0
:loop
call C:\Python27\python "C:\Users\Wim\Desktop\EASY UPLOAD\auto_upload.py" --input_file %1
shift
set /a n+=1
if not [%1]==[] goto loop

pause

