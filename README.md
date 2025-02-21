# Rating System
Creating a rating system as a part of the Bitpin company interview process. 

# Table Of Contents
- [Requirements](#Requirements)
- [None Functional Requirements](#None-Functional-Requirements)
- [Entity Relationship Diagram](#Entity-Relationship-Diagram)
- [System Architecture](#System-Architecture)
- [Endpoints Doc](#Endpoints-Doc)
- [Rating Manipulation Prevention](#Rating-Manipulation-Prevention)
- [Load Balane](#Load-Balance)


# Requirements

A system of users who can post content. The contents have a title and description. Users can rate content with a score from 0 to 5, but only once. Any repeated rating would be updated with the new score. Each content has several rates and average cumulative scores.

# None Functional Requirements
The system should detect and prevent rating manipulation. Because each content has millions of rates, calculating the average cumulative scores should be lazy and in real-time.

# Entity Relationship Diagram
![ER picture](/pictures/ER-diagram.png)

This is the data model of our entities in this system regarding the entities, relations, and attributes. 

# System Architecture
The following picture shows how different parts of the system interact.

![Arch Diagram](/pictures/Arch-diagram.jpg)
- PostgreSQL is used as the DB in this system.

- Kafka is used to handle the thousands of requests for rating content.

- Redis is used to retrieve popular content frequently and prevent rate cheating. 

# Endpoints Doc
The `/api/schema/swagger-ui/` URL provides complete API documentation. Parameters and possible outputs are described for each endpoint. One sample is below. 
- User Signup
    - Endpoint: `/api/user/signup/`
    - Parameters: 
        - Example :
        
            ```json
            {
                "username": "RandomUser",
                "password": "RandomPassword",
                "email": "random@gmail.com"
            }
            ```
    - Response : 
        - `201-Created`: User has been created
        - `400-Bad Request`: Missing some parameters

# Rating Manipulation Prevention

To prevent any possible fraud in rating contents we used a weighted rating system in which all the rates do not have the same effect. Based on the number of rates a content had in the past hour a new rate would affect the average score differently. It has two main components:
1. Redis Cache: to count how many rates have been submitted for specific content.
2. A function to calculate new rate weight based on the number of previous rates.

# Load Balance
- By using a Kafka queue in front of the API gateway we control the heavy load of rating different contents.
- There is an interface in which the logic of retrieving the list of contents can changed to use the Redis cache for frequent GET requests.


    
