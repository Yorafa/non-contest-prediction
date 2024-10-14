# Non-Contest Leetcode Question Prediction

A trial for predicting scores of non-contest leetcode question. 

This repo uses [contest rating](https://github.com/zerotrac/leetcode_problem_rating) which based on Elo rating system and Maximum Likelihood Estimation. We try to use those rating to predict the rating of non-contest questions.


## Linear Regression Model

Conclusion: A simple linear regession based on diffculty, frequency, acceptance and submission can not predict the rating well.
with freq: Train score: 0.7188232929722936 Test score: 0.6942480033476257 Root Mean squared error: 228.7023129419836
without freq: Train score: 0.718227486342313 Test score: 0.6946786985956768 Root Mean squared error: 228.54117628039637

## Random Forest Model

Conclusion: Random Forest model can predict the rating better than linear regression model.
with freq: Train score: 0.9723476855446307 Test score: 0.7894121664348245 Root Mean squared error: 189.80276913241298
without freq: Train score: 0.9698870405274742 Test score: 0.7678132491970158 Mean squared error: 199.29877208764782