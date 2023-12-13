for /f "tokens=1-2 delims=:" %%a in ('ipconfig^|find "IPv4"') do set ip=%%b
set ip=%ip:~1%
echo %ip%
cd C:\Users\giuly\Desktop\Sam\App\backend
python -m flask run --host %ip% --debug
pause
