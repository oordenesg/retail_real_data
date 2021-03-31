# retail_real_data

The objective of this project is to predict the sale of a retail chain according to the signals captured by the beacons (IoT sensor) within a store. To do this, different methods such as time series, SVM or LSTM can be used. Although this summary will not analyze statistical issues of the data, it will mention some characteristics of this data set as well as the main results obtained with the SVM model.

- The data set has 14 variables. Some of these variables have similar characteristics and others are not useful for estimating sales.
- There are 6 variables that have null values. One of the attributes has 87% missing values.
- Within the data set there are different IDs for the sensors. The objective is to determine the sale of each one of them and then add these results to obtain the total sales.
- Within the data set there are also duplicate values. 4.6% of the data are repeated.
- Although there is a date attribute for each of the records. This must be separated by year, month and day.

