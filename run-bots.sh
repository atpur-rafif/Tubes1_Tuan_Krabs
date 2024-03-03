#!/bin/bash

python main.py --logic Test --email=test@email.com --name=stima --password=123456 --team etimo &
python main.py --logic Test --email=test1@email.com --name=stima1 --password=123456 --team etimo &
python main.py --logic Test --email=test2@email.com --name=stima2 --password=123456 --team etimo &
python main.py --logic Test --email=test0@email.com --name=stima3 --password=123456 --team etimo &
