@echo off
start python server.py
ping 127.0.0.1 -n 4
python tests\test_api.py
