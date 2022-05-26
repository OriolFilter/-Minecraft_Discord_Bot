Start DEV container

server port 5555
query  port 5556


# mc

> docker run -p  5555:5555 -p 5556:5556 -e SERVER_PORT=5555 -e ENABLE_QUERY=true -e QUERY_PORT=5556 -e ONLINE_MODE=FALSE -e SERVER_NAME=Doomie -e MAX_TICK_TIME=-1 -e ENABLE_AUTOPAUSE=TRUE -e EULA=TRUE --name mc_testing itzg/minecraft-server


> docker run -p  5555:5555 -p 5556:5556 -e SERVER_PORT=5555 -e ENABLE_QUERY=true -e QUERY_PORT=5556 -e ONLINE_MODE=FALSE -e SERVER_NAME=Doomie -e -e EULA=TRUE --name mc_testing itzg/minecraft-server

> docker run -d -p  5555:5555 -p 5556:5556/udp -e SERVER_PORT=5555 -e ENABLE_QUERY=true -e QUERY_PORT=5556 -e ONLINE_MODE=FALSE -e SERVER_NAME=Doomie -e EULA=TRUE -e MAX_TICK_TIME=-1 -e ENABLE_AUTOPAUSE=TRUE --name mc_testing itzg/minecraft-server

# cached

> docker run -d -e CACHE_SIZE=128 -p 11211:11211 -e MEMCACHED_USERNAME=my_user -e MEMCACHED_PASSWORD=my_password -e MEMCACHED_THREADS=4 -e MEMCACHED_MAX_ITEM_SIZE=8388608 --name memcached_mc_testing bitnami/memcached

Decorators
#### https://stackoverflow.com/questions/14703310/how-can-i-get-a-python-decorator-to-run-after-the-decorated-function-has-complet 

#### https://en.wikipedia.org/wiki/Infinispan

ADD refresh rate

ADD to change the status according to the players

Look for a game invite button

Finish the damm readme

https://readthedocs.org/