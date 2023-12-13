for /f "tokens=1-2 delims=:" %%a in ('ipconfig^|find "IPv4"') do set ip=%%b
set ip=%ip:~1%
echo %ip%
start http://localhost/phpmyadmin
start http://%ip%:5000/get/
