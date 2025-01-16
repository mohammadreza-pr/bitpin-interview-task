# Rating System
Creating a rating system as a part of Bitpin company interview's process. 

# Requirements

A system of users who can post content. The contents have a title and description. Each user can rate content with a score from 0 to 5, but only once. Any repeated rating would be updated with the new score. Each content has a number of rates and average cumulative scores.

# None Functional Requirements
The system should detect and prevent rating manipulation. Because of millions of rates for each content, calculating the average cumulative scores should be lazy and in real-time.

# Entity Relationship Diagram
![ER picture](/pictures/ER-diagram.png)

This is the data model of our entities in this system regarding the entities, relations, and attributes. 

# System Architecture
The following picture shows how different parts of the system interact with each other.

![Arch Diagram](/pictures/Arch-diagram.jpg)
- The Postgersql is used as the DB in this system.

- Kafka is used to handle the thousands of requests for rating a content.

- Redis is used to retrive a popluar content frequently and preventing rate cheating. 

# Endpoints Doc
A complete documentaion of APIs is granted in the `/swagger/` URL. Parameters and possible outputs are described for each endpoint. One sample is like bellow. 
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
        - `201-Created` : User has been created
        - `400-Bad Request`: Missing some parameters

# Rating Maniuplation Prevention

    