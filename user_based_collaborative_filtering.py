##########################
# 1. Data Preprocessing
##########################

# imports and display settings
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

# uploading data
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")

# creating user-movie df as in item-based
def create_user_movie_df(df):
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df(df)

# random user selection
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values)

##########################
# 2. Determining the Movies Watched by the User to be Recommended
##########################

user_movie_df

# reduction of dataset by random_user
random_user_df = user_movie_df[user_movie_df.index == random_user]

# movies watched by random_user
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
movies_watched

# number of the movies watched by random_user
len(movies_watched)

##########################
# 3. Accessing the Other Users Watching the Same Movies with Random User
##########################

movies_watched_df = user_movie_df[movies_watched]

# how many movies each user has watched
user_movie_count = movies_watched_df.T.notnull().sum()

# converting user_id to variable which is in the index
user_movie_count = user_movie_count.reset_index()

# renaming the variables
user_movie_count.columns = ["userId", "movie_count"]

user_movie_count

perc = len(movies_watched) * 60/100

#Reducing the data to users who watched at least 60% of the movies that the random_user watched
user_movie_count[user_movie_count["movie_count"] > perc].sort_values("movie_count", ascending=False)

# User ID of these users
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
users_same_movies

# users watched all the movies that random_user watched
user_movie_count[user_movie_count["movie_count"] == len(movies_watched)]

##########################
# 4. Identifying Users with the Most Similar Behaviors with the User to Suggest
##########################

"""
This will take 3 steps
  1. aggregate data of random_user and other users
  2. Creating the correlation df
  3. Finding the most similar users (top Users)
"""

# creating final df to recommendation
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      random_user_df[movies_watched]])

# calculation of correlations for all users
corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()

# make corr_df more readable
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()

rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')

# Users with similar behavior as random user
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)

top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

# The ratings given to movies by users with a high correlation with random_user
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')

#Removing random user from dataframe because its correlation with itself is 1
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]

##########################
# 5. Calculating Weighted Average Recommendation Score
##########################

top_users_ratings["weighted_rating"] = top_users_ratings["corr"] * top_users_ratings["rating"]

# creating recommendation dataframe
recommendation_df = top_users_ratings.groupby("movieId").agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()

# Keeping the ids and ratings of movies with a weighted_rating greater than 3.5 to be recommended
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5]. \
    sort_values("weighted_rating", ascending=False)

movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')

# title of the movies to be recommended
movies_to_be_recommend.merge(movie[["movieId", "title"]])
