# Rating System
Creating a rating system as a part of Bitpin company interview's process. 

# Requirements

A system of users who can post content. The contents have a title and description. Each user can rate content with a score from 0 to 5, but only once. Any repeated rating would be updated with the new score. Each content has a number of rates and average cumulative scores.

# None Functional Requirements
The system should detect and prevent rating manipulation. Because of millions of rates for each content, calculating the average cumulative scores should be lazy and in real-time.

# Entity Relationship Diagram
![ER picture](/pictures/ER-diagram.png)

This is the data model of our entities in this system regarding the entities, relations, and attributes. 