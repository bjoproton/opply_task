# Opply Task

## Introduction and set up

I have provided a django instance intended to be used with postgres. 

The first step is to create a .env file to hold the value:

```bash
POSTGRES_PASSWORD=ASuperSecurePassword
```

The apps are containerised, so you can run the following:

```bash
docker compose build
docker compose -f docker-compose.yaml up
```

This will create two containers named backend and database. 

Alternatively, if you prefer a local install of python/django, there is an option just to build a test postgres db

```bash
docker compose -f docker-compose-pg.yaml up
```

Which will create a container called test-db and expose forward localhost:5432. If you choose this approach, you'll have to modify your django settings file, but I've left commentary near the DATABASES dictionary.

There are some tests available that can be run with the following commands, depending on whether you're running locally or in containerised mode.

Containerised:
```bash
docker exec -it backend bash -c "pytest"
```

Local:
```bash
pytest
```

## Time limitations

Generally, the time allocation was okay. However, I would like to have written many more unit tests, and get good coverage of the endpoints for making orders and the logic around the decrementing of the quantity. 

## Possible improvements

A better process for stock management. A way for a number of stock units to be added without having to look how many are remaining and add them together. A better approach to decrementing the stock, based on how many units were available and how many have been used (but not built dynamically every time the model loads).

A custom management command to report, perhaps trigger an email, when stock is getting low.

## Deployment instructions

At the beginning of this readme file I included instructions on how to run the containerised versions of the apps, so that's a decent start and of course this approach could be done on production too. 

However, a better approach would be to have the containers managed by a process too, Kubernetes would be a good option.

In terms of infrastructure, let's take AWS as an example:

Instead of deploying the database like we have in this example, we'd use an RDS instance. This would provide persistent storage and optimised access. 

We could run our containers on EC2 instances. We would not run with the development server provided using the runserver command, rather we'd have another containerised nginx instance.

We could manage our secrets not through a .env file, but rather through AWS Param Store. 

And all of this would be inside a VPC with a public facing load balancer. 
