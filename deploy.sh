USER=$1
IP_ADDR=$2

echo "sending files to $IP_ADDR as $USER"

rsync -v -e ssh CarControl/* $USER@$IP_ADDR:~/raspi/CarControl/

