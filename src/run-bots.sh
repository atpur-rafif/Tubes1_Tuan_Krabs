#!/bin/bash

python main.py --logic Nearest --email=nearest@email.com --name=nearest --password=123456 --team etimo &
python main.py --logic Biggest --email=biggest@email.com --name=biggest --password=123456 --team etimo &
python main.py --logic Gradient --email=gradient@email.com --name=gradient --password=123456 --team etimo &
python main.py --logic Random --email=random@email.com --name=random --password=123456 --team etimo &
