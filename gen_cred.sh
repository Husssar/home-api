DB="DATABASE='$1'"
USER="USER_SQL='$2'"
HOST="HOST='$3'"
PW="PASSWORD_SQL='$4'"
TEST_HOST="TEST_URL='192.168.9.8:5000'"

echo $DB > src/cred.py
echo $USER >> src/cred.py
echo $HOST >> src/cred.py
echo $PW >> src/cred.py
echo $TEST_HOST >> src/cred.py
