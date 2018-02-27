sudo nmap -sP 129.130.46.0/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'
