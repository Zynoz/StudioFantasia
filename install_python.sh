#!/bin/bash
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo appt-get install python3.8
sudo pip3 install -r requirements.txt