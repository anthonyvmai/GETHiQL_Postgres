#!/bin/bash

db=$(cat pgpass.conf | cut -d':' -f3)
user=$(cat pgpass.conf | cut -d':' -f4)
pass=$(cat pgpass.conf | cut -d':' -f5)
passfile=pgpass.conf
create_tables=create_tables.sql

echo "Creating db $db"
createdb $db
echo "Creating tables from $create_tables"
psql -d $db -f $create_tables
echo "Creating psql user $user with password $pass"
psql -c "CREATE USER $user WITH PASSWORD '$pass';"
psql -c "ALTER USER $user WITH SUPERUSER;"
echo "done"
