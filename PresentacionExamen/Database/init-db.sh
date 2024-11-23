#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  \i /docker-entrypoint-initdb.d/DDL.sql;
  \i /docker-entrypoint-initdb.d/DML.sql;
EOSQL
