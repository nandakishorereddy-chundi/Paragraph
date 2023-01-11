## About the App
 - This app contains 3 functionalities, they are:
    - It has a functionality to get a pragraph which contains 50 sentences, stores it in a persistent Database and also return the paragraph as a response.
    - It has a functionality to search using keywords with `AND` and `OR` operators.
    - It has a functionality to get meanings of top 10 highly occured words.

## Technology and Framework
 - Python
 - Flask
 - MongoDB
 - Docker

## Reason for selecting the Technology and Framework
 - I have opted for Flask framework and MongoDB as the Database because
    - Flask is a lightweight framework which is used to develop small projects and I find this project as a small use case and went with Flask as the framework.
    - The heavy operations involved in the functionalities are:
        - Storing chunks of texts and
        - Searching the texts using the keywords.
    - For both the functionalities MongoDB comes handy because it supports text search of string content very quickly with the help of creating an index called `text index` and search for text using `$text` operator.

## Installation to run unit tests
 - #### Creating a virtual environment
    - Prerequisities:
        - python(>3)
            - If not present, please follow this link to install: **https://www.python.org/downloads/**
        - pip(>20)
            - If not present, please follow this link to install: **https://pip.pypa.io/en/stable/installation/**
        - virtualenv(>20)
            - If not present, please follow this link to install: **https://pypi.org/project/virtualenv/**

    - After the prerequisite step:
        - create a virtual environment:
            - virtualenv <name_of_the_virtual_env>
        - activate virtual environment:
            - source <name_of_the_virtual_env>/bin/activate
 - #### Installing packages from requirments.txt
    - pip3 install -r requirments.txt

## Running Test cases
 - **pytest -s -v**

## Installation to run the server using docker
 - Prerequisities:
    - Docker
        - If not present, please follow this link to install: **https://docs.docker.com/engine/install/**

## Running server
 - docker-compose up --build
 - After executing the above command the server will be started

## API Refference
 - There are 3 APIs for the three described functionalities:
    - To get a new paragraph:
        - #### Request
            ```http
            GET /get
            ```
        - #### Responses
            - For Success case:
                HTTP/1.1 200 OK
                {'paragraph': text}
            - For Failure case:
                HTTP/1.1 500 Internal Server Error
    - To search for a paragraph:
        - #### Request
            ```http
            POST /search
            body: {
                "words": "posit, tulip",
                "operator": "AND"
            }
            ```
        - #### Responses
            - For Success case:
                ```http
                HTTP/1.1 200 OK
                {"paragraphs": [{"paragraph":<text>},{"paragraph":<text>}...]} 
                ```
            - For Failure case:
                ```http
                {'errors':[{'message': 'unsupported operator, supported operators are [OR, AND]'}]}, 422
                HTTP/1.1 500 Internal Server Error
                ```
    - To get meaning of top 10 occuring words:
        - #### Request
            ```http
            GET /dictionary
            ```
        - #### Responses
            - For Success case:
                ```http
                HTTP/1.1 200 OK
                {'meanings': {'word1': <meaning>, 'word2': <meaning>....}}
                ```
            - For Failure case:
                HTTP/1.1 500 Internal Server Error

## Code Structure
 - envs
    - dev.json -> Contains all the environment variables
 - libs
    - db.py -> Class which handles all the DB related stuff
    - env.py -> Helper file to load env variables
    - logger.py -> Class which handles logger and its formatting
    - util.py -> Contains all the common functions
- services
    - get.py -> Service which takes care of all the /get route functionalities
    - search.py -> Service which takes care of all the /search route functionalities
    - dictionary.py -> Service which takes care of all the /dictionary route functionalities
- tests
    - conftest.py -> Which stores all the fixtures which are used by all the unit tests
    - test_get.py -> Contains unit tests related to all the /get route
    - test_search.py -> Contains unit tests related to all the /search route
    - test_dictionary.py -> Contains unit tests related to all the /dictionary route
- docker-compose.yml -> Docker compose file
- DockerFile -> Docker file
- driver.py -> File which exposes the endpoint and encapsulates the logic for implementing the routes
- README.md -> readme file
- requirments.txt -> Contains all the packages used as part of the project
