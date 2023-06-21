#!/bin/bash
lsof -ti:10131 | xargs kill -9
lsof -ti:10132 | xargs kill -9
username=$1
ssh -4 -fNL 10131:itrac1609-v.cern.ch:10121 -L 10132:itrac1601-v.cern.ch:10121 $username@lxplus.cern.ch
