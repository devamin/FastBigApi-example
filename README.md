# FastBigAPI architecture example for HRFLOW(simple management of jobposts and applications)

This is a template example for the FastBigAPI architecture, HRFlow contains 2 sub applications to manage authentication, jobposts, and application.  
We use Poetry as package manager(https://python-poetry.org/docs/#installation)

## Architecture
![alt FastBigApi architecture](assets/architecture.png)

## Features
* Global dependency injection and inversion of control
* Authentication with JWT
* Authorization with novel privilege decorators
* Modular subapp based architecture

## Hrflow Api Documentation 
This project uses openapi to document the REST api communication interface consider using: 
* `/auth/docs` to access the openapi interface to create accounts and login. 
* `/job/docs` to access the open api interface of job subapp with jobpost controller and application controller.

### How to ?

#### Install

make install

#### Test
make test

#### Run
make run