# ADR for domestic/NNA/CC

## Tools used in this project
* [Tools1](https://link.com/): Tool 1 - [article](https://article1.com)


## Project structure
```bash
.
├── config                      
│   ├── main.json                   # Main configuration file
│   ├── model                       # Configurations for training model
│   │   ├── model1.json             # First variation of parameters to train model
│   │   └── model2.json             # Second variation of parameters to train model
│   └── process                     # Configurations for processing data
│       ├── process1.json           # First variation of parameters to process data
│       └── process2.json           # Second variation of parameters to process data
├── data            
│   ├── final                       # data after training the model
│   ├── processed                   # data after processing
│   ├── raw                         # raw data
├── docs                            # documentation for your project
├── .gitignore                      # ignore files that cannot commit to Git
├── models                          # store models
├── notebooks                       # store notebooks
├── README.md                       # describe your project
├── src                             # store source code
│   ├── __init__.py                 # make src a Python module 
│   ├── process.py                  # process data before training model
│   └── train_model.py              # train model
└── tests                           # store tests
    ├── __init__.py                 # make tests a Python module 
    ├── test_process.py             # test functions for process.py
    └── test_train_model.py         # test functions for train_model.py
```

## Version control

Add and push all changes to Git:
```bash
git add .
git commit -m 'commit-message'
git push origin <branch>
```

## Project Description

My own project description.
    
### Steps

The steps followed on this project are:

* **[step1]**: Step 1 description - **[notebook]**: ```notebook_name.ipynb```

### Results

Here are the results