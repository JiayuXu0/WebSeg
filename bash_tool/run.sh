docker  stop webseg
docker container rm webseg
docker run -d -p 5000:5000  --name webseg webseg:v0.0.1 sh /home/jiayuxu/source/bash_tool/start.sh