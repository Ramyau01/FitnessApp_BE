#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE FitnessAppDatabase"

psql FitnessAppDatabase -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"