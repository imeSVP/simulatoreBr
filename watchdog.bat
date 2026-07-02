@echo off
chcp 437 >nul



:: 使用WMIC获取标准日期时间
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I

:: 提取并格式化为yyyy-MM-dd
set today=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

set workGroup=1
set date_z=%today%
set heartbeat_file=heartbeat_%workGroup%.txt
set max_idle=240
set check_interval=5
set max_retries=6
set retry_count=0

:START
set /a retry_count=%retry_count%+1
cls
echo ========================================
echo Watchdog Monitor - WorkGroup: %workGroup%
echo ========================================
echo Launch count: %retry_count% / %max_retries%
echo Heartbeat file: %heartbeat_file%
echo ========================================
echo.

:: Check if max retries reached
if %retry_count% gtr %max_retries% (
    echo Max retries reached. Exiting.
    
    exit
)

:: STEP 1: Delete heartbeat file first
echo [Step 1] Deleting heartbeat file...
if exist %heartbeat_file% (
    del %heartbeat_file%
    echo Heartbeat file %heartbeat_file% deleted.
) else (
    echo No heartbeat file %heartbeat_file% found.
)

:: STEP 2: Kill all Python processes
echo [Step 2] Cleaning up all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul

:: STEP 3: Start Python
echo [Step 3] Starting Python with workGroup %workGroup%...
start python main_simularoti.py %workGroup% %date_z%

:: STEP 4: Wait for Python to initialize and heartbeat file
echo [Step 4] Waiting for heartbeat file to appear...
set wait_counter=0
:WAIT_HB
if not exist %heartbeat_file% (
    set /a wait_counter+=1
    if !wait_counter! gtr 30 (
        echo [ERROR] Heartbeat file not created after 30 seconds
        echo [ERROR] Restarting...
        timeout /t 3 /nobreak >nul
        goto START
    )
    timeout /t 1 /nobreak >nul
    goto WAIT_HB
)

:: STEP 5: Get initial heartbeat
echo [Step 5] Reading initial heartbeat from %heartbeat_file%...
set /p last=<%heartbeat_file%
echo Initial heartbeat: %last%
set idle=0

:: STEP 6: Get Python PID (optional, for display only)
echo [Step 6] Getting Python PID...
set pid=
for /f "tokens=2" %%a in ('tasklist ^| find "python.exe" 2^>nul') do (
    set pid=%%a
    goto GOT_PID
)
:GOT_PID
if "%pid%"=="" (
    echo PID: Not found (but program is running)
) else (
    echo PID: %pid%
)

echo.
echo ========================================
echo Monitoring started...
echo ========================================
timeout /t 2 /nobreak >nul

:: Monitoring loop
:MONITOR
cls
echo ========================================
echo Watchdog Monitor - WorkGroup: %workGroup% 
if not "%pid%"=="" echo PID: %pid% - Launch: %retry_count%/%max_retries%
echo Time: %time%
echo Heartbeat file: %heartbeat_file%
echo ========================================

:: Check if heartbeat file exists
if not exist %heartbeat_file% (
    echo [ERROR] Heartbeat file missing - Restarting...
    timeout /t 2 /nobreak >nul
    goto START
)

:: Read current heartbeat
set /p current=<%heartbeat_file%
set current=%current: =%
set last=%last: =%

echo Last heartbeat: %last%
echo Current heartbeat: %current%

:: Compare heartbeats
if "%current%"=="%last%" (
    set /a idle=%idle%+%check_interval%
    echo ----------------------------------------
    echo Status: No heartbeat change
    echo Idle time: %idle% seconds
    echo Threshold: %max_idle% seconds
    
    if %idle% geq %max_idle% (
        echo.
        echo ========================================
        echo [%retry_count%/%max_retries%] HEARTBEAT TIMEOUT!
        echo Killing Python processes...
        echo ========================================
        taskkill /F /IM python.exe 2>nul
        echo.
        echo Restarting in 5 seconds...
        timeout /t 5 /nobreak >nul
        goto START
    )
) else (
    echo ----------------------------------------
    echo Status: Heartbeat updated - Timer reset
    set last=%current%
    set idle=0
)

echo.
echo Next check in %check_interval% seconds...
timeout /t %check_interval% /nobreak >nul
goto MONITOR
curl http://193.70.114.235/finser-sys/downfiles/sincrorcds_segugio_rt_ee_gas.php