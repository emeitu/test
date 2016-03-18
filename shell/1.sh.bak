#!/bin/bash
awk -F '=' '/\[com1\]/{a=1}a==1&&$1~/key/{print $2;exit}' config.ini
