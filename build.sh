#! /bin/bash

version=1.18.1P
ram=6

# show build server info
echo -------------------------------
echo Build server info
echo
echo -e "Version\t =" $version
echo -e "RAM\t =" $ram "GB"
echo -------------------------------

# set CPU frequency max
sudo cpufreq-set -g performance

# Build
cd /home/pi/minecraft/servers/${version}
sudo screen -S minecraft nice -n -15 java -Xms${ram}G -Xmx${ram}G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:InitiatingHeapOccupancyPercent=20 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui

# set CPU frequency ondemand
sudo cpufreq-set -g ondemand

# Backup To Google Drive
echo
echo "Starting Backup To Google Drive. "
echo
cd /home/pi/minecraft/servers
rclone sync -P $version GoogleDrive:RaspberryPi/Minecraft/$version

echo
read -p "Exit to press Enter."
cd