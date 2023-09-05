docker cp project1_sampledata.sql project1-mysql-1:/tmp/sample-data.sql
docker exec -it project1-mysql-1 mysql -u project1 -pSuperSicher project1 < /tmp/sample-data.sql