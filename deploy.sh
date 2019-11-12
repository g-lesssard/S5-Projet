USER=projet
IP_ADDR=192.168.0.10
DIR=/home/projet/CarControl/

echo "sending files to $IP_ADDR as $USER"

rsync -rve ssh CarControl/* $USER@$IP_ADDR:$DIR

