USER=projet
IP_ADDR=192.168.0.10

echo "sending files to $IP_ADDR as $USER"

rsync -v -e ssh CarControl/* $USER@$IP_ADDR:~/projet/CarControl/

