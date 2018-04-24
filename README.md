# Coveo Backend Coding Challenge
(inspired by https://github.com/busbud/coding-challenge-backend-c)

## Setup

Create table and populate it with data.
You may need to configure the database name, username, and password
`python server/setup.py`

## Run App

`cd server`
`export FLASK_APP=app.py`
`flask run`

## Requirements Satisfaction

> Design an API endpoint that provides auto-complete suggestions for large cities.

API endpoint is provided at 35.196.219.197:5005/suggestions

> - The endpoint is exposed at `/suggestions`
> - The partial (or complete) search term is passed as a querystring parameter `q`
> - The caller's location can optionally be supplied via querystring parameters `latitude` and `longitude` to help improve relative scores
> - The endpoint returns a JSON response with an array of scored suggested matches
>     - The suggestions are sorted by descending score
>     - Each suggestion has a score between 0 and 1 (inclusive) indicating confidence in the suggestion (1 is most confident)
>     - Each suggestion has a name which can be used to disambiguate between similarly named locations
>     - Each suggestion has a latitude and longitude

## Language and technology

Python - Learned more extensively through this coding challenge. Prior, I have only used it to the extent of programming interview questions. 

PostgreSQL - New to it, tried it, loved it.

Google Compute Engine - I have used the Google Compute Engine to set up an API endpoint for 1 project before. The new aspect from this project was to populate the database instance.

## Scoring algorithm

1. Edit distance
2. Physical distance

### Edit distance

Edit distance is basically the number of character differences between two words. For example, 'snow' and 'know' have only 1 character difference. 'sunny' and 'sunday' have 2. The algorithm is effective for finding the minimal number of character differences between the two words, which may possess an unequal number of characters.

### Physical distance

Physical distance is taken as an optional input parameter to detect whether or not a particular city should be a more accurate result than another. For example, if a user is located near city A than B, then city A will have a higher score than city B on the physical distance category.

### Weighting 

After tweaking and testing, a 80-20 ratio between the two factors are ideal. This supports the case where a user's query will be very different from the city's name while the city is located very close to the user. In cases like these, it doesn't make sense to show entirely different cities just for the sake of being close.

It also covers the case where there are multiple cities with the same name. In such cases, it makes more sense to suggest the city that is closer to the user.

## Further ideas

The following ideas have been considered.

**Using city population as a factor** 
This came from the idea that cities with a higher population are more likely to be searched for than cities with a low population. But when I thought about my everyday use with map searches, I realized this isn't the case. So I scrapped the idea.

**Using the user's lat and long to determine which country they are in, and then prioritizing the cities from that country**
This goes in accordance with the user's lat-long and physical proximity to a city. However, I thought about my experiences with searches and realized this is not an ideal feature. For example, when I search for Paris, I am 99% of the time searching for Paris in France and not Paris in Canada.

**Keeping track of user's searches and the results**
Ideally, it would be great to save the user's searches and chosen results in order to analye the queries. Further recommendations and better suggestions can be provided through this idea. However, I think this is beyond the scope of what I can do for the challenge as it requires client-side implementation on usage and analytics.

## References

- Geonames provides city lists Canada and the USA http://download.geonames.org/export/dump/readme.txt