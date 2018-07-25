# Conduktor

Conduktor is a collaborative URL shortener designed for teams that rely on Gsuite as their primary authentication provider.

It allows anyone with a valid Google login in a whitelisted set of domains to create expressive HTTP redirects to arbitrary URLs, both internal and external. 

Conduktor does not provide any form of authorization, allowing instead all users equal access to its entire functionality; however, it keeps an audit trail of all changes made to each URL redirect so that they can be traced to their author.

Conduktor also keeps basic statistics on usage for each redirect, so that stale URLs can be periodically purged from the system.

## Installation

Before installing Conduktor, you need to obtain a set of properly-configured oAuth2 credentials as explained in the [Google Sign-in documentation](https://developers.google.com/identity/sign-in/web/sign-in).

Conduktor can be easily stood up using `docker-compose`. The `docker-compose-production.yml` file sets up a complete environment that also includes a persistent PostgreSQL installation.

The app relies on environment variables to provide several bits of essential context:

- `GOOGLE_OAUTH_CLIENT_ID`: the Client ID of your oAuth credentials
- `AUTHORIZED_DOMAINS`: a comma-separated list of domains whose users are allowed to access Conduktor's management interface
- `API_URL`: the base URL of the server as visible from the browsers where the management interface runs
- `BASE_URL`: the base URL of the server as visible from browser that are attempting to use the redirect service
- `APP_TITLE`: the title of the app (defaults to `Conduktor`)
- `DB_DSN`: the DSN used to connect to the database

Typically, `BASE_URL` and `API_URL` will be the same value, but they could be different if, for example, you wish to use an application firewall to only make the API accessible from inside a private network.

(If you're using the provided Docker Compose configurations, the `DB_DSN` variable is ignored, and each of the remaining variables should be prefixed with `CONDUKTOR_`—e.g., `CONDUKTOR_API_URL`, etc.)

### Setup

Before running the app for the first time, you should run migrations to ensure that the database is properly set up. If you're using the provided Docker Compose infrastructure, this should do the trick:

    docker-compose --file ./docker-compose-production.yml run server migrate

## Use

New redirections can be created by pointing your browser to the app's root. This will cause the admin interface to be loaded; from there on, usage should be self-explanatory.

## Structure

Conduktor is a very simple app. It is made up of a REST API server, written in Python using Tornado, and a frontend app written in Vue.js.

At build time, the frontend app is compiled and stored inside the API server's directory structure, from where it is then served. Navigating to the server's main page causes a redirection to `/_/index.html`, which is where the client app resides. Because Conduktor forbids the creation of redirect slugs that start with an underbar, the app will not interfere with the redirection functionality.

Access to any endpoint that doesn't start with an underbar is taken to be a request for a redirection. The API server looks for the corresponding slug in the database, and acts accordingly.

### Setting up for development

The `docker-compose-development.yml` file provides everything you need to stand up a development environment. Changes to any of the Python or JS files will immediately be reflected in the running servers. You can access the client at `localhost:3001`, and the API server at `localhost:3000` (unlike what happens with a production environment, client and server run separately in development mode for compatibility with the way Webpack works).