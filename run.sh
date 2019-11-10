USER=$1
IP=$2
DIR='~/raspi/CarControl'


ssh $USER@$IP "python3 $DIR/__main__.py"
