#!/bin/bash
database=$(cat pgpass.conf | cut -d':' -f3)
user=$(cat pgpass.conf | cut -d':' -f4)
export PGPASSFILE=pgpass.conf
psql -U $user -d $database -h localhost -w
