### dbt model analysis

For a given model name it will return all ref models and also the source tables


# PRE-REQUSITES:

1. python v3.7 or above.
2. If one line contain more then one ref or source , this script will not capture 2nd value.

The python script needs to placed in model folder.


# Run command format

py dbt_find_tables {model_name}.sql


#output 

ref models have level column also which implies from which level the model comes.

ex: model1 level 0 
    model2 level 0 
    model3 level 1 
    model4 level 1 
    
    In here model1 and model2 build on model3 and model4
