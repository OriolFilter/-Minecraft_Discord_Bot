FROM python:alpine
LABEL "author"="Oriol Filter Anson"
LABEL "version"="1.0"
LABEL "description"="Discord bot for minecraft server through Query connection"
LABEL "repository"="https://github.com/OriolFilter/Minecraft_Discord_Bot"

ENV MINECRAFT_HOSTNAME=
ENV MINECRAFT_QUERY_PORT=25565
ENV MINECRAFT_RCON_PORT=25575

ENV MEMCACHED_HOSTNAME=
ENV MEMCACHED_PORT=11211
ENV MEMCACHED_USERNAME=
ENV MEMCACHED_PASSWORD=

ENV DISCORD_TOKEN=
ENV DISCORD_PREFIX="mc."
ENV DISCORD_DESCRIPTION="Hi, I'm a Bot! My function is to help you!"
ENV DISCORD_MC_URL="url.domain.com:port"


ADD ./code /main
WORKDIR /main
RUN pip3 install -r ./requirements.txt --user
WORKDIR /main
RUN chmod +x ./main.py
CMD ["python3","-u","/main/main.py"]
