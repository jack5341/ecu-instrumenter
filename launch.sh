#!/bin/sh

echo -ne "\n\n"
echo --------------------------------------------------------------------
echo ":: ECU INSTRUMENTER LAUNCH"
echo --------------------------------------------------------------------

AppDir=$(pwd)
AppExecutable="app.py"
Arguments="$@"
PerformanceMode=1

echo --------------------------------------------------------------------
echo ":: APPLYING ADDITIONAL CONFIGURATION"
echo --------------------------------------------------------------------

if [ "$PerformanceMode" = "1" ]; then 
    echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
fi

cd "$AppDir"
HOME="$AppDir"

# --- PYTHON PATH RESOLUTION ---
# Below we look for Python inside OnionOS. The github link uses Python 2.7 from Parasyte,
# but your application requires Python 3. We attempt to find Python 3 first!

if [ -f "/mnt/SDCARD/.tmp_update/bin/python3" ]; then
    # OnionOS Package Manager Python 3
    PYTHON_BIN="/mnt/SDCARD/.tmp_update/bin/python3"
    export LD_LIBRARY_PATH="/mnt/SDCARD/.tmp_update/lib:$LD_LIBRARY_PATH"

elif [ -f "$AppDir/python3/bin/python3" ]; then
    # Standalone Python 3 bundled inside the ECUInstrumenter folder
    PYTHON_BIN="$AppDir/python3/bin/python3"
    export LD_LIBRARY_PATH="$AppDir/python3/lib:$LD_LIBRARY_PATH"

elif [ -f "/mnt/SDCARD/.tmp_update/bin/parasyte/python3" ]; then
    # Custom OnionOS parasyte Python 3
    ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
    export PYTHONPATH=$ParasytePath/python3:$ParasytePath/python3/site-packages:$ParasytePath/python3/lib-dynload
    export PYTHONHOME=$ParasytePath/python3:$ParasytePath/python3/site-packages:$ParasytePath/python3/lib-dynload
    export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python3/:$ParasytePath/python3/lib-dynload:$LD_LIBRARY_PATH
    PYTHON_BIN="/mnt/SDCARD/.tmp_update/bin/parasyte/python3"

elif command -v python3 >/dev/null 2>&1; then
    # Generic python3 in the PATH
    PYTHON_BIN="python3"

elif [ -f "/mnt/SDCARD/.tmp_update/bin/parasyte/python2" ]; then
    # Fallback to OnionOS built-in Python 2.7 from Parasyte (from the Github script)
    # WARNING: Your code uses Python 3 features (dataclasses) and will crash here!
    ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
    export PYTHONPATH=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
    export PYTHONHOME=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
    export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python2.7/:$ParasytePath/python2.7/lib-dynload:$LD_LIBRARY_PATH
    PYTHON_BIN="/mnt/SDCARD/.tmp_update/bin/parasyte/python2"

else
    PYTHON_BIN="python3"
fi

echo --------------------------------------------------------------------
echo ":: RUNNING THE APP using $PYTHON_BIN"
echo --------------------------------------------------------------------

eval "$PYTHON_BIN" \"$AppExecutable\" $Arguments

echo --------------------------------------------------------------------
echo ":: POST RUNNING TASKS"
echo --------------------------------------------------------------------

unset LD_PRELOAD
echo -ne "\n\n" 
