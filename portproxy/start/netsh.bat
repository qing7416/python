::netsh for windows
::2020-02-15 17:33:16

::在 10.192.98.116 上运行
netsh interface portproxy add v4tov4 listenaddress=* listenport=14331 connectaddress=10.192.114.79 connectport=51433 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14332 connectaddress=10.192.114.80 connectport=51433 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8394 connectaddress=10.192.114.80 connectport=8394 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8585 connectaddress=10.192.114.82 connectport=8585 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=27017 connectaddress=10.192.114.82 connectport=27017 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=10000 connectaddress=11.11.192.31 connectport=10000 protocol=tcp

::在 192.168.18.128 上运行
netsh interface portproxy add v4tov4 listenaddress=* listenport=14331 connectaddress=10.192.98.116 connectport=14331 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14332 connectaddress=10.192.98.116 connectport=14332 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8394 connectaddress=10.192.98.116 connectport=8394 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8585 connectaddress=10.192.98.116 connectport=8585 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=27017 connectaddress=10.192.98.116 connectport=27017 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=10000 connectaddress=10.192.98.116 connectport=10000 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=3690 connectaddress=10.205.8.55 connectport=3690 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8091 connectaddress=10.205.1.79 connectport=8091 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14333 connectaddress=10.205.1.19 connectport=1433 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14334 connectaddress=10.205.1.211 connectport=49805 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=51433 connectaddress=10.196.1.34 connectport=51433 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=51433 connectaddress=10.192.161.97 connectport=51433 protocol=tcp

::在 172.36.63.173 上运行
netsh interface portproxy add v4tov4 listenaddress=* listenport=14331 connectaddress=192.168.18.128 connectport=14331 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14332 connectaddress=192.168.18.128 connectport=14332 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8394 connectaddress=192.168.18.128 connectport=8394 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8585 connectaddress=192.168.18.128 connectport=8585 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=27017 connectaddress=192.168.18.128 connectport=27017 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=10000 connectaddress=192.168.18.128 connectport=10000 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14333 connectaddress=192.168.18.128 connectport=14333 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=14334 connectaddress=192.168.18.128 connectport=14334 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=8091 connectaddress=192.168.18.128 connectport=8091 protocol=tcp
netsh interface portproxy add v4tov4 listenaddress=* listenport=3690 connectaddress=192.168.18.128 connectport=3690 protocol=tcp

