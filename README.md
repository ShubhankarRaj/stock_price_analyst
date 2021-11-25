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
