# CS50W Capstone: Newswordy

## Introduction
For my capstone project, I designed Newswordy, a web application that allows users to view trending headlines from roughly 150 news sources across the web. 

In all, users can view trending headlines within their country, predetermined categories, or categories of their creation. 

The project was created using Django, Bootstrap, JavaScript, and SQLite. 


## Distinctiveness and Complexity
For organization's sake, it is best to break down the project's main features and explain the technology behind each of them. 

### Trending Headlines
Newswordy's home page displays trending headlines within a user's country using IP geolocation. Luckily, Django comes with a pre-installed way to retrieve the user's IP address. 

Once retrieved, the application calls ipinfo.io's API to retrieve information on the user's location. After parsing the JSON response, the application extracts the user's country. Afterward, the application calls the News API with the user's country as a URL parameter and extracts an array of trending articles from the JSON response. 

### Categories
The categories feature allows authenticated users to narrow their search to predetermined themes, such as "science", "business", or "technology." This feature also uses IP geolocation to pull trending headlines within a user's country. 

### Search
The search feature allows users to search for articles on topics of their choice. Unlike the trending headlines or categories sections, the search section searches globally without using IP geolocation. However, if the user's query matches a category within the accepted categories, then the user will be redirected to the category of their choice.

### Saved Articles
On the trending headlines, categories, and search sections, authenticated users can save article to their "Saved Articles" section. This was achieve by using JavaScript and custom API routes to add a post to a SQLite database and using a many-to-many relationship between users and articles. 

Users can also unsave articles on all of the sections, and the webpage will remember if the user has saved the article or not upon a webpage reload. 

### Login/Registration
The login and registration features were achieved with Django's built-in authentication and hashing features. 

### Account Page
The account section of the web application allows users to view basic information tied to their account, such as their email, username, date joined, and other fields within the Django default User class. 

## Additional Information
I'd like to sincerely thank the CS50 team for helping me along with my programmign journey. Although I know I have much left to learn, programming has totally changed my life! I started programming last December during winter break through online courses. I'm now a teaching assistant for two programming courses at UT Austin, and I even traveled to MIT for their most-recent hackathon! Keep up the amazing work! :)

## Third-Party Libraries
This makes use of the following third-party libraries:
- django
- newsapi-python
- python-dateutil
- requests