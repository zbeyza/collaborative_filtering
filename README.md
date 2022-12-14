# Collaborative Filtering

![Ekran görüntüsü 2022-12-12 154841](https://user-images.githubusercontent.com/81737980/207726484-ef0efd4d-e0e3-4a7c-aabf-e91b03162b4d.jpg)

Collaborative Filtering is a method that offers suggestions using similarities between users and products. Collaborative Filtering analyzes similar users or similarly rated products and recommends users based on this analysis.

Collaborative filtering is divided into 3 subheadings:

- Item-Based Collaborative Filtering
- User-Based Collaborative Filtering
- Model-Based Collaborative Filtering

### Item-Based Collaborative Filtering:
It is a method that analyzes the product similarity or the ratings given by the users to the products and makes suggestions according to the analysis result.

### User-Based Collaborative Filtering:
It is a method that analyzes the behaviour (liking) of users and offers suggestions according to the likes of users who exhibit similar behaviour.

### Model-Based Collaborative Filtering:
In Model-Based Collaborative Filtering, the problem is approached more holistically. It is assumed that there is a problem that needs to be optimized.


###### You can find the detailed explanation of the projects from following link:
##### https://medium.com/@zbeyza/recommendation-systems-collaborative-filtering-75121f19dd03


## About Dataset:
MovieLens 20M movie ratings. Stable benchmark dataset. 20 million ratings and 465,000 tag applications applied to 27,000 movies by 138,000 users. Includes tag genome data with 12 million relevance scores across 1,100 tags. Released 4/2015; updated 10/2016 to update links.csv and add tag genome data.

###### link for the dataset:
##### https://grouplens.org/datasets/movielens/20m/

#### Movie:
- movieId: id of the movie
- title: title of the movie

#### Rating:
- userId: id of the user
- movieId: id of the movie
- rating: the user’s rating for the movie
- timestamp: timestamp of the rating
