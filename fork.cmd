@echo off
color a
title Update the fork 
git remote add original https://github.com/jplight/faultybot.git
git fetch original
git checkout main
git reset --hard original/main
git push