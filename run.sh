USER=projet
IP=192.168.0.10
DIR='/home/projet/CarControl'


ssh $USER@$IP "python3 $DIR/__main__.py"
