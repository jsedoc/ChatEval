## SETC: A Standard Evaluation Tool for Chatbots

This tool is an attempt to bring some order to chaos. We employed the help of statisticians to design a tool to better compare models.  So you compare your model to another one. Each model comparison costs $1.20 ...

Consider SETC a vending machine .. insert models and $1.20 and out come evaluation scores! Yay! Now _no one_ should have to suffer.

### [We are in a state of confusion](https://docs.google.com/document/d/1EJPr0dHtaOSKw5AaBCQfueSoJlBT39ZDf-7FRjAerU0/edit?usp=sharing)

Currently researchers do not use standard model parameters, or human analysis setup to test if a model inproves results.

![human evaluators](human_evaluator_inconsistency.gif)

### Support or Contact

Having trouble email joao at upenn dot edu

### Backstory

On Feb 2nd 2018, Joao was tired of trying to eva1uate his chat bot model. He could simply not replicate the neural conrersation model. Eventually he started looking for a standard tool for evaluation . But it didn't exist! Out of frustration SETC was born.

So the next step was to evaluate super simple ideas. Do random seeds matter? (NO) What is the effect of data filtering? (Sometimes)  How do we decide to stop the training of the model? (Open question, but _not_ perplexity!)
