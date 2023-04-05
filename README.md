# STOCK PRICE ANALYST

We need to add the stock that we want to run our analysis in the `config.json` file @two places.</br>
"new_stocks" is for all the newly added stocks, for which we would like to get the history added.</br>
"stocks" is for all the stocks on which the history is already run and we are running the daily analysis on these stocks.

When updating the data of the stocks, we need to run two commands:

1. First command is to update the history of the stock, which is applicable on all the newly added stocks
   
   ```python orchestrator.py hist```
   
2. Next command is to update the current info of the stock which are already added.
   
    ```python orchestrator.py info```

N.B.: hist command need to run before info.


### TODO ITEMS
Covariance is a statistical tool that is used to determine the relationship between the movements of two random variables.
When two stocks tend to move together, they are seen as having a positive covariance; when they move inversely, the covariance is negative.
Covariance is different from the correlation coefficient, a measure of the strength of a correlative relationship.
Covariance is a significant tool in modern portfolio theory used to ascertain what securities to put in a portfolio.
Risk and volatility can be reduced in a portfolio by pairing assets that have a negative covariance.

N.B. : Use Covariance to Create a stock portfolio. Negatively covariated stocks can become a part of a portfolio
making it way stable.
