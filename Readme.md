# Question 1
## Question 1.1
For this purpose we started reading the csv file using pandas libary. A function was defined in order to create a histogram of a numerical field of the dataframe.

![Balance Histogram](figures/balance_hist.png)
## Question 1.2
For this part of the question i will comment on some findings of the data structure:
- There are important differences in the scale of the variables.
- There are 6 fields which have null values, two of them are the date fields wich is strange and could be a data source error. The credit limit field has some null values, this is interesting to me because i think that credit cards always assign a limit; I am assuming that asset-backed loans are not included here.
- This is a very unbalanced dataset. The percentage of fraud is 0.78%, data augmentation techiniques could be necessary.
- There is a correlation of 0.92 between purchases and oneoff_purchases, wich means that most customer purchases are sporadic. The correlation between purchases_frequency and purchases_installments_frequency is 0.86 wich means that most customer purchases are paid in installments.
- Finally, the fraud field (target) is more correlated with oneoff_purchases and to a lesser extent with payments, this reinforces the intuitive idea that customers with sporadic and large purchases can be riskier.

![Balance Histogram](figures/correlation_map.png)
## Question 1.3
Again, a function is defined to group by year and month and calculate mean and median of the field balance per year/month. Only the necesary fields were used. The code for this question is Question1.py.

# Question 2
## Question 2.1
For this excersice i kept only the five necessary fields, we turn date fields to datetime type in order to extract the year of both dates and then select only the rows with year 2020 of activation and last payment. I also extracted the first letter of cust_id and modified activation_date to show only year and month. Finally, the calculated field is as shown in the code; the code for this question es Question2.py.

# Question 3
## Question 3.1
To build a model, first the date features were drop and instead a new calculated feature was used. This new one is the days between last payment and activated date, in some cases days < 0, and i assume that this means that it is an advance payment. Cust_id feature were drop because its one row per client. Other dropped features were oneoff_purchases and purchases_installments_frequency because they were very correlated with purchases and purchases_frequency. Finally there were some features with missing data so i applied a simple imputation method with the median because its more robust to outliers than mean. Finally a standar scaling was applied because in regression problems it is important to have features of similar scale.
Once the above was done i decided to apply a logistic regression because this is a binary classification problem and i wanted an easy to interpret model. The hiperparameter optimization was done with optuna which is based on bayesian optimization, we focus on the hiperparamteres based on regularization. Metrics like accuracy, precision, recall, f1, auc and specificity were calculated but focusing the optimization in f1 because i wanted to control both type 1 and type2 errors; i think that it was also reasonable to optimize with respect to recall because I consider the type 2 error to be more serious. The f1 is 0.30, precision is 0.18 and recall 0.82, as we can see it has failures to detect type 1 error but does not do badly in detecting type 2 error.
## Question 3.2
Here we just need to see the absolute value of the coefficients. The purchases, cash_advance_trx, balance coeff were some of the most importants, which makes sense because the riskiest clients are those who buy the most or who have cash from their line of credit, which implies a higher interest rate.

# More comments
- A virtual enviroment was used during this excersise.
- For this excersise, the folder figures contains two of the plots made, the codes are in the folder src and there is one python file per question. The requirements.txt contains the libaries used and their versions to replicate this in a docker enviroment, for example.
- About the model, we could try a more complex model with techiniques like boosting but with regressors functions instead of trees. This kind of models perform feature bagging to avoid overfitting.
- But more important than the above, is neccessary to try some syntetic data creation to get a more balanced set. Techiniques that do this is SMOTE techinique.