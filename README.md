[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README.ru.md)
# Skillbox. Diploma "Recommendation system for online hypermarket Instacart"

Within the diploma, a recommendation system was developed for the online hypermarket Instacart within [competition](https://ww.kaggle.com/competitions/skillbox-recommender-system) on the platform [Kaggle](https://www.kaggle.com/).
The *hybrid approach* was used to create the system. The rating of the user’s products is formed from the products he has already bought, using several filtering methods:
- by the frequency of purchases;
- on time of purchase (number of days from date of transaction to date of last transaction);
- by adding the product to the basket number;
- on the popularity of the product (among all users).

Within the model training the *optimal* values of coefficients of the last three types of filtration are selected. *The optimum* value of the coefficient is such that the MAP@10 metric of product predictions in the last transaction based on previous transactions takes the maximum value.  

In case the number of products that the user bought is less than the required size of recommendations, the recommendations are supplemented by the most popular products from the groups that he is most interested in.

The trained model got the following validating scores on [Kaggle](https://www.kaggle.com/):
- Private Score - `0.3264`
- Public Score - `0.32822`

The process of creating the model is given in [notebook](skillbox_recommender.ipynb). Before starting the notebook, you need to configure a little:
- to specify the path to the project folder where the data will be placed (`PROJECT_PATH`, default - "D:/skillbox-recommender-system");
- set the number of parallel computing processes (`WORKERS`, default - 4).

In addition, the class [Recommender] (recommender.py) is created, which implements the resulting recommendatory model and interface with it. To demonstrate the work of this class, a special [dashboard](main.py) has been created using the [Streamlit](https://streamlit.io/) and [Streamlit-Option-Menu] (https:/git.hub.yhb/streamlit-optionmenu). Before starting the dashboard, you must install the given framework and components, i.e.

Start dashbord by running the script [run.py](run.py) with two parameters: 
- --data_path - the path to the project folder where the data will be placed (it is recommended to use the folder `PROJECTS_PATH`/data);
- --wokers - number of parallel computing processes (it is recommended to use no more than 4 with 16 GB of RAM).

Learning a model on a complete set of transactions takes about `7.5` minutes.
The list of 10 recommended products shall be drawn up of approximately:
- `0.23` c - for single user;
- `23.5` с - for all users (100000).

### The composition of the repository is: 
- [skillbox_recommender.ipynb](skillbox_recommender.ipynb) - a notebook with solution
- [recommender.py](recommender.py) - a module that includes a class of Recomender
- [functions.py](.py) - library of auxiliary functions.
- [multiproc.py](multiproc.py) - a parallel computation script
- [average_precision.py](average_precision.py) - [library](https://github.com/benhamner/Metrics/blob/9a637aea795dc6f2333f022b0863398de0a1ca77/Python/ml_metrics/average_precision.py). [Wendy Kan](https://github.com/wendykan).
- [kaggle.py](kaggle.py) - Kaggle interface library 
- [main.py](main.py) - dashboard script for testing and demonstration of model 
- [run.py](run.py) - startup script
