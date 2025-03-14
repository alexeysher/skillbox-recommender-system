# Skillbox. Thesis "Recommendation system for online hypermarket Instacart"

Within the thesis, a recommendation system was developed for the online hypermarket Instacart 
within [competition](https://ww.kaggle.com/competitions/skillbox-recommender-system)
on the platform [Kaggle](https://www.kaggle.com/).
The *hybrid approach* was used to create the system. The rating of the user’s products is formed 
from the products he has already bought, using several filtering methods:
- by the frequency of purchases;
- on time of purchase (number of days from date of transaction to date of last transaction);
- by adding the product to the cart order;
- on the popularity of the product (among all users).

Within the model training the *optimal* values of coefficients 
of the last three types of filtration are being obtained. 
*The optimum* value of the coefficient is such that the 
MAP@10 metric of product predictions in the last transaction based 
on previous transactions takes the maximum value.  

In case the number of products that the user bought is less than the required size of recommendations, 
the recommendations are supplemented by the most popular products from the groups that he is most interested in.

The trained model got the following validating scores on [Kaggle](https://www.kaggle.com/):
- Private Score - `0.32640`
- Public Score - `0.32822`

The process of creating the model is given in [notebook](skillbox_recommender_system.ipynb). 
Before starting the notebook, you need to configure a little:
- to specify the path to the project folder where the data will be placed (`PROJECT_PATH`, default - "D:/skillbox-recommender-system");
- set the number of parallel computing processes (`WORKERS`, default - 4).

Learning a model on a complete set of transactions takes about `7.5` minutes.
The list of 10 recommended products shall be drawn up of approximately:
- `0.23` c - for single user;
- `23.5` с - for all users (100000).

In addition, a dashboard with description of solution and demo of recommendation system base on this one.
The dashboard is utilising [Streamlit](https://streamlit.io) framework.
It's deployed on Streamlit community cloud and shared by this [link](https://skillbox-data-analytics.streamlit.io). 


### The composition of the repository is: 
- solution:
    - [average_precision.py](average_precision.py) - [library](https://github.com/benhamner/Metrics/blob/9a637aea795dc6f2333f022b0863398de0a1ca77/Python/ml_metrics/average_precision.py). [Wendy Kan](https://github.com/wendykan).
    - [kaggle.py](kaggle.py) - Kaggle interface library
    - [functions.py](functions.py) - library of auxiliary functions.
    - [multiproc.py](multiproc.py) - a parallel computation script
    - [skillbox_recommender.ipynb](skillbox_recommender_system.ipynb) - a notebook with solution
    - [recommender.py](recommender.py) - model class
- dashboard:
    - [auxiliary.py](auxiliary.py) - auxiliary functions
    - [main.py](main.py) - main executable script
