echo "Stop containers..."
docker stop silvatools-mysql
docker stop silvatools-rabbit
docker stop silvatools-redis

echo "Remove containers..."
docker rm silvatools-mysql
docker rm silvatools-rabbit
docker rm silvatools-redis

echo "Finished"
