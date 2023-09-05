#!/bin/bash
docker exec -i project1-mysql-1 sh -c 'mysql -u project1 -pSuperSicher project1' < ./project1_sampledata.sql