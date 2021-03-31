# retail_real_data

The objective of this project is to predict the sale of a retail chain according to the signals captured by the beacons (IoT sensor) within a store. To do this, different methods such as time series, SVM or LSTM can be used. Although this summary will not analyze statistical issues of the data, it will mention some characteristics of this data set as well as the main results obtained with the SVM model.

- The data set has 14 variables. Some of these variables have similar characteristics and others are not useful for estimating sales.
- There are 6 variables that have null values. One of the attributes has 87% missing values.
- Within the data set there are different IDs for the sensors. The objective is to determine the sale of each one of them and then add these results to obtain the total sales.
- Within the data set there are also duplicate values. 4.6% of the data are repeated.
- Although there is a date attribute for each of the records. This must be separated by year, month and day.

The first idea was to use the SVM model to predict a sales threshold. However, this idea is not entirely good because as the threshold increases, there is less data to predict. Figure 1 illustrates this problem.


<p align="center" width="100%">
    <img width="35%" src="https://user-images.githubusercontent.com/76072249/113222557-af901000-925d-11eb-9a6e-da0d629dd1c0.png"> 
</p>

For this reason, and given the low amount of data for some sensors, an alternative is to go from a regression problem to a classification problem. This was done by creating sales ranges. The objective of this was to create small groups of data that allow us to apply some oversampling technique on the data. Figure 2 shows the results of the confusion matrix of the SVM model with oversampling and without an optimized model.

<p align="center" width="100%">
    <img width="35%" src="https://user-images.githubusercontent.com/76072249/113223201-fe8a7500-925e-11eb-9c7a-34e31c652402.png"> 
</p>

The next step was the process of optimization of the model's hyperparameters. In this stage 3 types of kernels were used as well as different values for the parameter C.

<p align="center" width="100%">
    <img width="35%" src="https://user-images.githubusercontent.com/76072249/113223396-72c51880-925f-11eb-9179-305d1c82f356.png"> 
</p>

The results of the optimization process allowed to improve the accuracy of the model. With this, we managed to achieve an accuracy of 90.6%. 5% higher than that obtained with a non-optimized SVM model. Figure 4 shows the new confusion matrix.


<p align="center" width="100%">
    <img width="35%" src="https://user-images.githubusercontent.com/76072249/113223551-cb94b100-925f-11eb-8eaf-91c1da62a2f4.png"> 
</p>

This problem can be addressed using different analytical techniques. In the future, new methods will be added to make a comparison between all the models.
