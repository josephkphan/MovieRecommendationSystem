# MovieRecommendationSystem

# Background Data
## The Training Data
The training data: a set of movie ratings by 200 users (userid: 1-200) on 1000 movies (movieid:
1-1000). The data is stored in a 200 row x 1000 column table. Each row represents one user.
Each column represents one movie. A rating is a value in the range of 1 to 5, where 1 is "least
favored" and 5 is "most favored". Please NOTE that a value of 0 means that the user has not
explicitly rated the movie.

## Test Data
[test5.txt] A pool of movie ratings by 100 users (userid: 201-300). Each user has already rated 5
movies. The format of the data is as follows: the file contains 100 blocks of lines. Each block
contains several triples : (U, M, R), which means that user U gives R points to movie M. Please
note that in the test file, if R=0, then you are expected to predict the best possible rating
which user U will give movie M.

ATTENTION: Please make the prediction block by block: every time when you are making
predictions for user U, please assume that you ONLY know the knowledge of the training data
(train.txt) and the existing 5 ratings for this user. In other words, please DO NOT use the
knowledge of any other blocks in the test file when making predictions.
The format of test10.txt and test20.txt is nearly the same as test5.txt, the only difference is that:
in test10.txt, 10 ratings are given for a specific user; in test20.txt, 20 ratings are given for a
specific user.

## How to get the accuracy?
To get the accuracy of your predictions, please submit the predicted ratings to our online system.

# Types of Recommendation Engines

## Case 1: Recommend the most Popular Items
 - the most popular items would be same for each user since popularity is defined on the entire user pool. So everybody will see the same results.
 - no personalization involved with this approach
 - There is division by section so user can look at the section of his interest.
 - At a time there are only a few hot topics and there is a high chance that a user wants to read the news which is being read by most others
 -
## Case 2: Using a Classifer to make recommendation
 - Use Classification Algorithms to make recommendations.
### Pros:
 - Incorporates personalization
 - It can work even if the user’s past history is short or not available
### Cons:
 - The features might actually not be available or even if they are, they may not be sufficient to make a good classifier
 - As the number of users and items grow, making a good classifier will become exponentially difficult

## Case 3: Recommendation Algorithms
### Content Based Algorthms
 - Idea: If you like an item then you will also like a “similar” item
 - Based on similarity of the items being recommended

### Collaborative filtering algorithms:
 - Idea: If a person A likes item 1, 2, 3 and B like 2,3,4 then they have similar interests and A should like item 4 and B should like item 1.
 - This algorithm is entirely based on the past behavior and not on the context. This makes it one of the most commonly used algorithm as it is not dependent on any additional information.

 - User-User Collaborative filtering: Here we find look alike customers (based on similarity) and offer products which first customer’s look alike has chosen in past. This algorithm is very effective but takes a lot of time and resources. It requires to compute every customer pair information which takes time. Therefore, for big base platforms, this algorithm is hard to implement without a very strong parallelizable system.
 - Item-Item Collaborative filtering: It is quite similar to previous algorithm, but instead of finding customer look alike, we try finding item look alike. Once we have item look alike matrix, we can easily recommend alike items to customer who have purchased any item from the store. This algorithm is far less resource consuming than user-user collaborative filtering. Hence, for a new customer the algorithm takes far lesser time than user-user collaborate as we don’t need all similarity scores between customers. And with fixed number of products, product-product look alike matrix is fixed over time.

