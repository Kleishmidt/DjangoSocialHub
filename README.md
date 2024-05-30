# DjangoSocialHub

DjangoSocialHub is a instagram-like social network where users can create accounts, make posts, 
like and comment on posts, follow other users, and search posts by tags and other users.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Kleishmidt/DjangoSocialHub.git
```

2. Make a copy of the `.env.web.example`,`.env.db.example`, `config_template.json` and rename it to 
`.env.web`, `.env.db`, `config.json` accordingly.
   Modify the values in the files according to your specific environment and requirements.


3. Build the docker containers:

```sh
   docker-compose up --build --remove-orphans
```

4.Once the containers are up and running, you can access the DjangoSocialHub application in your web browser at:
```sh
   http://localhost:8000
```
