#!/bin/bash

user=gethiql_user
pass=foobar123
passfile=pgpass.conf
db=gethiql_db
create_tables=create_tables.sql

echo "Creating db $db"
sudo -u postgres bash -c "createdb $db"
echo "Creating tables from $create_tables"
sudo -u postgres bash -c "psql -d $db -f $create_tables"
echo "Creating psql user $user with password $pass"
sudo -u postgres bash -c "psql -c \"CREATE USER $user WITH PASSWORD '$pass';\""
echo "Creating $passfile"
echo "*:*:$db:$user:$pass" > $passfile
chmod 600 $passfile
echo "done"
