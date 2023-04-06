DB="DATABASE='$1'"
USER="SQL_UW='$2'"
HOST="HOST='$3'"
PW="PASSWORD='$4'"


echo $DB > src/cred.py
echo $USER >> src/cred.py
echo $HOST >> src/cred.py
echo $PW >> src/cred.py

