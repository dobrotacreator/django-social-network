# Django social network
_An analogue of twitter with its own features._ 

## 📂 Non-functional tools used
### 📌 General:
- UNIX-like system (Ubuntu)
- Work on GitHub Flow
- PostgreSQL as a database for core app
- AWS DynamoDB for microservice
- For file storage - AWS S3  
- To send email - AWS SES
- Two different RabbitMQ queues for microservice and Celery

### 📌 Python:
#### Common:
- Version 3.10.6
- Virtual environment management using pipenv
- PEP 8
- Communication between the microservice and the main app via RabbitMQ
- Interacting with AWS using boto3
- Validation of the JWT token in both applications
> ⏳ TODO
>- All business logic is covered by unit tests, both approaches are used (mock, fixture)
#### Core app:
- Django + Django Rest Framework
- ViewSets + routers
- ModelSerializer
- Celery + RabbitMQ for sending notifications
- The business logic of the application is separated from views into separate services.
- Custom JWT authentication using Middleware (PyJWT)

> ⏳ TODO
>#### Microservice:
>- FastAPI
>- Pydantic

### 📌 Docker + docker-compose:
 - One Dockerfile on Celery and Django, but different input points
 - Separate Dockerfile for microservice
 - The database is deployed in docker-compose

## 📂 Functionality
A user can have one of 3 roles:
- Administrator
- Moderator
- User

1) The administrator has the right to view any pages, block them for any period of time and permanently, delete any posts and block users. The administrator also has access to the admin panel.
2) The moderator has the right to view any pages, block them for any period of time, delete any posts.
3) The user can:
	- register, log in
	- create a page, edit its name, uuid and description, add and remove tags to it, make it private/public
	- subscribe to other people's pages (send a subscription request in the case of private pages)
	- view the list of those who want to subscribe to the page (in the case of private) and confirm/refuse to subscribe (one at a time or all at once)
	- write posts on his pages, edit them, delete them
	- like/unlike posts, respond to them on behalf of his own pages
    - view the posts he has liked
4) Avatars of users and pages are stored in cloud storage.

### System functionality:
1) Sending email notifications to subscribers about new posts.
2) News feed display (all new posts of subscribed and own pages)
3) Automatic blocking of all user pages if the user is blocked
4) Providing search pages by name/uuid/tag and users by username/name (using one endpoint)
5) Checking the extensions of downloaded files
6) Showing page statistics (number of posts, subscribers, likes, etc.), which is generated on the microservice, only to users who own pages