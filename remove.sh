#!/bin/bash
rm -rf /home/pi/Documents/*
rm -rf /home/pi/Documents/.*
cd /home/pi/Documents
git clone git@github.com:pavelmaks/JagerMachine.git
cd JagerMachine
mv * ../
mv .* ../
cd /home/pi/Documents
rm -rf JagerMachine/*
rm -rf JagerMachine/.*
rmdir JagerMachine
sudo reboot


