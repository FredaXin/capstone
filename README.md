# Using Regression Models to Predict Home Affordability Ratio 

Author: [Freda Xin](https://github.com/FredaXin)

---
## Table of Contents

---
## Problem Statement:
In regions where rapid new urban development emerges, home prices tend to become less affordable in the initial phase of the development. This phenomena occurs in many U.S. and Canadian cities such as San Francisco, Denver, and Vancouver, where the residents' income level does not keep up with the fast increase in home prices.

Home affordability ratio is defined as the home price and median annual income ratio. "Historically a house in the US cost around 3 to 4 times the median annual income. During the housing bubble of 2007 the ratio surpassed 5 - in other words, the median price for a single family home in the United States cost more than 5 times the US median annual household income"(reference). In recent years, many U.S. and Canadian neighborhoods have become unaffordable for the residents.

In my project, I will explore whether commercial activities in a given neighborhood can be an indicator for the affordability of home prices. In particular, I will explore which types of business might be the best indicator of the neighborhood's affordability level. This approch has the advantage of lower costs than the traditional method based on census information. It can also serve as an early indicator used by a municipality: if certain patterns of business activities emerges, the problem of a neighborhood becomes unaffordable might fellow.

I will use the Google Places API to gather data about neighborhood businesses, such as types, opening hours, price level etc. To calculate Home affordability ratio, I will scrap home prices data from Zillow, divided by the median income collected from US Cecus Bereau(good and cheap) (or buy the data from incomebyzipcode.com(Fast and Good).

I will use unsupervised model during the EDA process to explore patterns of commercial activities. I will develop supervised regression models to predict affordability.

My project will be develped in 4 phases:

Phase 1: Case study of NYC: develop models using NYC data
Phase 2: Test if model is transferable for other urban areas, such as L.A. or Toronto
Phase 3: Generlization: Test model can be generized and used in any given urban areas.
Phase 4: Web interface: Develop a simple web interface so a client can imput
informations, and receive predictions.

---
## Executive Summary

---
## List of Assumptions

---
## Workflow 

---
## Conclusion 
### Phase 1
In Phase 1, I engineered aggregated features based on each zipcode, and
concatenated them back to the original data-frame. In theory, the benefit of this
approach is two fold:
- we would be able to capture the general information of each zipcode.
- we would be able to retrain the same amount of data as the original dataset. This will ensure that we have sufficient amount data. 

The so-called “Naive Approach” is based on a simple idea: we would
be able to use ALL the original observations to train the models. However, as we
discovered that this approach led to data leakage issue, and therefore invalid. However, this does NOT mean that in general we can't use aggregated features along with the original dataset; we just can't aggregated the observations the SAME way that we aggregated the target.


### Phase 2
In Phase 2, I used the aggregated observations by zipcode, combining with census
data from the Income dataset to train the model.

The pattern sub-model enabled us to handle missing data without imputation or dropping observations.
Among all the regression models, the `BaggingRegressor` yields the best result
based on the test R2 score. However, even the best model still shows signs of
high variance, and the result is not optional.

During the model elevation process, we confirmed that the model violates the
Equality of Variance and Independence of Errors assumptions.

Based on the model evaluation, features from the census data play an
importance role in the model's performance. This finding might pose challenges
to my goal of developing a generalization of the model: i.e. Using the model to
predict home affordability ratio in other U.S. regions without retraining the
model.


### Phase 3
Without the census data, the performance of the model decreased. Training only with the Google Places API data, the `LinearRegression` Model combined with L1 Regularization outperforms the others. 

Using the trained `LinearRegression` Model to make predictions for the LA dataset, the model performed badly. Based on the test scores, as well as the residuals plots, we can conclude that the model trained on the New York State dataset is inadequate for the predication of home affordability ratios in LA, especially given the model tends to over-predict the target. We can conclude that the trained model is not transferable. 

This outcomes makes intuitive sense: New York State and LA has very different
commercial landscapes, as well as demographic factors (such as median home
prices and median annual income). The model that has been fitted and trained on the
former is not able to capture the patterns of the latter. 

---
## Limitation and Next Steps
### Next Steps
**Step 1**: Improve data quality: 
- Collect more data: during the early modeling process, I observed that the models' performance drastically increased after being trained with more data points (from only using NYC to NYS). Since the amount of observations (n = 1521), I will try to collect more data to improve the model's performance.
- Sampling data from different regions in the U.S, and stratify the samples: In order to help the model learn a wider variety of dataset, I will try to randomly sample some zipcode across the States.
- If step 1 has been accomplished, and there is no significant improvement in the model's ability of making predictions, I will do the following:

**Step 2**: Reevaluate the assumptions: 
 - Research on what known factors have proven links to home affordability ratio:
   the first and for-most assumption of this project is that commercial
   activities can be predictive for home affordability ratio. This assumption is
   very likely to be unsound. During this project, we have confirmed that
   including census data will increase the model performance; in other words,
   the commercial activity information collected from the Google Places API
   alone are not as predictive as combing with census data. There might be many
   factors that link to the target: home affordability ratio, and further
   research need to be conducted, so I will have more prior knowledge about what
   might the be most significant factors in predicting home affordability ratio.
   
 ### Limitations
Using **Google Place API** has many limitations in the data collection process: 

- When using string search, the results returned are unpredictable: e.g. when making an API call using param "stores near zipcode 10010", some unexpected result was returned, such as a school or an government office. 
- The API only returns up to 3 calls per location (each location only returns up to 20 results). This limits the amount of samples can be collect per location. 
- The API returns 20 results per call, and it's unclear what algorithms was behind these results: such as proximities to the location centroid or popularity of the business as search result. So the businesses returned by the calls might be biased based on Google's algorithms.
- As mentioned in notebook 04, the 'open_now' feature is dependent on the time when the API calls are made. 
- The Google Place API is not free: making many API calls will make the project very expensive. Therefore, the amount of data that can be collected can be very limited based on the budget of the project. 



---
## References 
- *[**Home Price-to-Income Ratios**](https://www.jchs.harvard.edu/home-price-income-ratios)* by Joint Center for Housing Studies of Harvard University
- 