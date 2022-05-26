# Mosscraft

## Description



## Requirements

```bash
docker
docker-compose
git
```

## How to run

### Creating a docker network

First we need to create a docker network for our both containers (minecraft and discord) to communicate. 

```bash
docker network create my_minecraft_network
```

### Join already running container to the network created 

```bash

```

### Join docker-compose container the network created

Where "..." stands for previous existing configuration.

```yaml
networks:
   ...
   my_minecraft_network:
      external: True
...

   minecraft_server:
       ...
       networks:
          ...
          my_minecraft_network
```

## Configuration

### Environments

| Environment          | Default Value                | Description                                                                                                         |
|----------------------|------------------------------|---------------------------------------------------------------------------------------------------------------------|
| MINECRAFT_HOSTNAME   | \<Null\>                     | Hostname/IP to connect to the minecraft server/container.                                                           |
| MINECRAFT_QUERY_PORT | 25565                        | Port to connect to the minecraft server through the RCON protocol (must be enabled on the server).                  |
| MINECRAFT_RCON_PORT  | 25575                        | *Not being used* Port to connect to the minecraft server through the RCON protocol (must be enabled on the server). |
| MEMCACHED_HOSTNAME   | \<Null\>                     | Hostname/IP to connect to the memcached server/container.                                                           |
| MEMCACHED_PORT       | 11211                        | Port to connect to the memcached server.                                                                            |
| MEMCACHED_USERNAME   | \<Null\>                     | Username to authenticate to the minecraft server.                                                                   |
| MEMCACHED_PASSWORD   | \<Null\>                     | Password to authenticate to the minecraft server.                                                                   |
| DISCORD_TOKEN        | \<Null\>                     | Hostname/IP to connect to the minecraft server/container.                                                           |
| DISCORD_PREFIX       | mc.                          | Prefix for the discord bot to read the commands.                                                                    |
| DISCORD_DESCRIPTION  | "Welcome welcome, I'm a bot" | Description for the bot.                                                                                            |
| DISCORD_MC_URL       | \<Null\>                     | Url to display for the users to join the server.                                                                    |

