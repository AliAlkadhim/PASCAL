#!/bin/bash
lsof -ti:10131 | xargs kill -9
username=$1
ssh $username@lxplus.cern.ch
