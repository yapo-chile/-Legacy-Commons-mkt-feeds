# Feeds
App used to parse all active ads in our site to different places for example:
* Facebook
* GoogleAdwords
* Critio

## Installment
### Requires python 3.7 - 3.8
### Requires pip3

```
pip3 install virtualenv
virtualenv --python=python3 mkt-feeds
git clone git@github.mpi-internal.com:Yapo/mkt-feeds.git

cd mkt-feeds
source bin/activate
```

### Build container and get them up
```
make start
```

### Start core app locally (needs to run make start first because docker db is used)
Install needed packages to work
```
make requirements
```
Run app locally
```
make start-local
```

### ENV PARAMS

*SERVER_PORT* <num>
  
*SERVER_DEBUG* <true/false>

### Documentation
For more info about how the software works go to https://confluence.mpi-internal.com/display/YAPO/Product+feed

### More info soon
