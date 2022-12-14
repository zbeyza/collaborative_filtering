#########################
# 1. Data Preprocessing
#########################

# imports and display settings
import pandas as pd
from surprise import Reader, SVD, Dataset, accuracy
from surprise.model_selection import GridSearchCV, train_test_split, cross_validate
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

# uploading datasets
movie = pd.read_csv("datasets/movie_lens_dataset/movie.csv")
rating = pd.read_csv("datasets/movie_lens_dataset/rating.csv")
df = movie.merge(rating, how="left", on="movieId")
df.head()

# names and ids of 4 movies in terms of traceability
movie_ids = [130219, 356, 4422, 541]
movies = ["The Dark Knight (2011)",
          "Cries and Whispers (Viskningar och rop) (1972)",
          "Forrest Gump (1994)",
          "Blade Runner (1982)"]

# reduction of the dataset according to these movies
sample_df = df[df.movieId.isin(movie_ids)]
sample_df.head()

# User-Movie Dataframe
user_movie_df = sample_df.pivot_table(index=["userId"],
                                      columns=["title"],
                                      values="rating")

# converting dataframe to desired format by surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(sample_df[["userId",
                                       "movieId",
                                       "rating"]], reader)


#########################
# 2. Modelling
#########################

# dividing the data we created into 2 as train and test
trainset, testset = train_test_split(data, test_size=.25)

# the model that we will use the matrix factorization method
svd_model = SVD()

# building model on train set
svd_model.fit(trainset)

# testing model on test set
prediction = svd_model.test(testset)

# r_ui = real rate
# est = estimated rate
# iid = item id
# uid = user id

# what is the average error
accuracy.rmse(prediction)
# RMSE : 0.9336

svd_model.predict(uid=1.0, iid=541, verbose=True)
# Prediction(uid=1.0, iid=541, r_ui=None, est=4.260963425165127, details={'was_impossible': False})

sample_df[sample_df["userId"] == 1]
# Prediction(uid=1.0, iid=541, r_ui=None, est=4.08071693620795, details={'was_impossible': False})

#########################
# 3. Model Tuning
#########################

# here we will focus on how to optimize the hyperparameters of the model.
# n_epoch parameter : number of iterations, default = 20
# lr_all : learning rate

# possible parameter sets
param_grid = {"n_epochs": [5, 10, 20],
              "lr_all": [0.002, 0.005, 0.007]}

gs = GridSearchCV(SVD, # model object
                  param_grid, # possible parameter sets
                  measures=["rmse", "mae"], # error metrics
                  cv=3, # 3-fold cross validation
                  n_jobs=-1, # use all CPUs
                  joblib_verbose=True) # report to me while transactions are taking place

gs.fit(data)

gs.best_score["rmse"] # 0.9301769705860913
gs.best_params["rmse"] # {'n_epochs': 5, 'lr_all': 0.002}

# optimum values were found and it is needed to update them in the model



#########################
# 4. Final Model & Prediction
#########################

svd_model.n_epochs
svd_model_tuned = SVD(**gs.best_params["rmse"])

# train the whole dataset
data = data.build_full_trainset()
svd_model_tuned.fit(data)

svd_model_tuned.predict(uid=1.0, iid=541, verbose=True)
# Prediction(uid=1.0, iid=541, r_ui=None, est=4.228895461634215, details={'was_impossible': False})

sample_df[sample_df["userId"] == 1]