# AGENT IMPLEMENTATION


### DATA PREPROCESSING:
- Reviewing the data
- Findig missing values and filling them
- Dropping the noise
- Extracting features (failed test commit info, logs, code)
- Labeling the data (fix commit info, logs, code)
- Splitting data into training and testing sets
### Why features are failed tests and labels are fixes?
- Failed tests are the input data, and fixes are the output data.
- The model learns the patterns from the fixes and provides the most probable fix for the failed test.
- By follwing the work done on Facebook's *Getafix* tool, we can see that pattern recognition is the key to the success of the model.
- Key aspect of forming the patterns is the AST analysis, and the GumTree is used for that purpose.
### UNDERSTANDING OF PREPROCESSING:
- The data is being preprocessed by the NLP techniques.
- When extracting the features we associate the failed test with the commit info, logs, and code.
- When labeling the data we associate the fix with the commit info, logs, and code.
- It is important to associate fixes with the failed tests, because the model will learn the patterns from the fixes.
- Logs provide information on failure type and stack trace which is crucial for problem identification.
- AST of the failed and fixed code is being compared to find the differences along with the test configuration. Approach used is the GumTree.
- This approach allows us to see if the node in the AST is added, removed, or changed by checking the mapping of the nodes.

### CLUSTERING
- Clustering is used to group failures of similar type. Grouping by feature analysis.
- We perform clustering based on the failure logs (failure context).
- Since failures in the dataset are associated with the fixes, we can use the fix commit info to group the failures.
- Example:

            General Fix: Insert null check
        ├── Specific Fix 1: Insert `if (x == null) return;`
        ├── Specific Fix 2: Insert `if (x == null) throw new Exception();`
        │   └── Concrete Fix: Insert `if (x == null) throw new IllegalStateException("Error message");`
        └── Specific Fix 3: Add a default value assignment.
- How are the cluster formed?
    - There are multiple ways, but when the AST is generated and the concrete fix is found it represents the leaf. 
    - One approach is to vectorize these solutions using the code and the context (AST edit types, error message embeddings, context embeddings) and group them hierarchially.
    - By merging leaf nodes we create clusters, with associated context, this is being done until the root node is reached.
    - Merging by comparing cosine similarity of the embeddings (one possible approach).
    - In the example provided, General Fix is the root node, and the Concrete Fix is the leaf node. Specific Fix 1, 2, and 3 are the intermediate nodes. Each node represents a cluster.
# What does the model do?
- Associates the failed test with the cluster.
- Provides specific code changes from the predicted cluster/pattern.
- Ranks multiple results based on the probability of the fix.
- Under each generated candidate fix, the static analysis is performed to check if the fix is correct.

### Trainning the model:
- Approach: Supervised learning
    - Model predicts the cluster for proovided failed test with context.
- Using pre-trained models, but fine-tuning them on the dataset. (Bert, GPT)

### Evaluation phase:
- Model is evaluated on the test set.
- Models needs to provide human-like fixes.
- Metrics:
    - Accuracy, percentage of fixes that are correctly mapped to the cluster.
    - Precision, coverage of predictions.
    - Time complexity, how long does it take to predict the fix.
    - F1 score, harmonic mean of precision and recall.



# Additions

### Conntinual learning

- Since code practices are changing constantly, the model needs to be updated.
- We can strema new TeamCity CI data to the model and retrain the model on the new data.
    - Since retraining the model on the whole dataset is time-consuming, we can include stalleness parameter to the model.
    - This provides an insite in what patterns are outdated and can be removed from the model.
    - For general analysis of frequency of a single pattern we can use probabilistic data structures like Count-Min Sketch.
    - The model can be updated on the fly, by providing the new data and fine-tuning the model on the new data.
- Agent can be used to provide the feedback on the model performance, such as developer feedback on the provided fixes.

#  Conclusion

- Our agent uses the model fine tuned on the provided TeamCity CI data.
- Model is used to associate failures with potential fix clusters and return concrete fixes that pass the static analysis.
- Agent provides users with multiple fixes, ranked by the probability of the fix.
- Agent recieves candidate fixes, performs static analysis on the top fixes and provides the user with fixes that pass the static analysis.
- Agent collects the feedback such ass: 
    - Fix approved
    - Fix dissaproved
    - Fix corrected
- Approved fixes increase cluster weights, while rejected fixes lead to re-ranking or retraining.
- By collectin this data and processing it, we allow our model to achieve continual learning and get better as the time passes.

# Problems

- Dataset not easy to parse, depends on the format during the years.
    - Potential Solution: Spliting data into multiple parts by time and parsing it to a unified format.
- Problem during continual integration, **catastrophic forgetting**.
    - Potential Solution: periodical retraining of the model on a small subset of historical data.
- Flaky Tests: Flaky tests introduce noise to the dataset.
    - By analyzing historical trends we can exclude these features.
- Data drift: nature of test failures and fixes, code practices and etc. can change over time.
    - Potential solution: constant performance monitoring, model retraining, cluster updates.
- Parsing overhead, 15 year old dataset is huge.
    - Potential solution: parallel processing, distributed computing.




  
References:  
[GETAFIX: Facebook's test failure solving agent](https://dl.acm.org/doi/pdf/10.1145/3360585)  
[R Hero: Software repair bot based on Continual Leraning](https://www.researchgate.net/publication/350569349_A_Software_Repair_Bot_based_on_Continual_Learning)