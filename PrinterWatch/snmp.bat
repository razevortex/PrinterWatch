net user administrator /active:yes
snmpwalk -v1 -c public 172.20.20.76 1.3.6.1.2 mgmt > "%~dp0\temp\1.3.6.1.2.txt"
