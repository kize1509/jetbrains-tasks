# Data Synchronization Tool MVP

## Introduction

- Proposed solution solely focuses on synchronizing data between two databases.

- Data synchronization tool represents a way to synchronize and transfer data between remote databases and local databases. The tool is designed to be used by developers and data engineers to facilitate the process of data synchronization and transfer.

- It is developed as a DataGrip tool, which is a popular IDE for database management and development. The tool is designed to be user-friendly and easy to use, with a simple and intuitive interface.

- Intial idea is to build on top of a current diff tool in Data Grip, which allows us to incorporate the usefull features of the diff tool and add more features to it.

## User Stories

- As a developer, I want to be able to synchronize data between remote and local databases, so that I can work on my projects more efficiently.
- As a data engineer, I want to be able to transfer data between databases, so that I can maintain data consistency and integrity.
- As a database administrator, I want to be able to schedule data synchronization tasks, so that I can automate the process and save time.

## Features

- Connect to remote and local databases
- Select dbs, schemas, tables and columns to synchronize
- Schedule synchronization tasks
- Monitor synchronization progress


## Technology Stack

- Java
- Kotlin
- SQL
- DataGrip SDK


## MVP

- The MVP version of the data synchronization tool will include the following features:
  - Connect to remote and local databases
  - Select entire databases, schemas, tables and columns to synchronize
  - Add rules for automatic synchronization 
  - Synchronize data between databases
  - Monitor synchronization progress

- The MVP version will be developed as a DataGrip tool, with a simple and intuitive UI.



# Detailed implementation plan

## 1. Connect to remote and local databases

 -Since this feature is already implemented in DataGrip, we can use the existing functionality to connect to remote and local databases.

## 2. Select entities to synchronize

- By right-clicking on a database, schema, table, or column, and choosing the tools option, we can perform sync for the selected entity.

## 3. Set sync rules

- This is used when conflicts arise during synchronization. We can set rules to resolve conflicts.
- For example, we can set a rule to always overwrite the local data with the remote data, or vice versa or to merge the data.
- Additional rules can be added as needed, such as to keep the latest data, or to keep the data with the highest priority.

## 4. Synchronize data between databases

- Implement data synchronization functionality
- Allow users to synchronize data between databases
- Provide options to schedule synchronization tasks


## 5. Develop UI

- Current diff tool in Data Grip can be used as a base for the UI since it this tool does not differ much from the diff tool.
- Additional UI is required for rules and scheduling tasks.
- Tools such as Navicat and dbForge can be used as a reference for the UI design since they offer easy-to-use interfaces for data synchronization.

# Technical Details

### Remote connection

- Connection protocols inside DataGrip are already implemented, and the documentation is available, so using the existing functionality to connect to remote and local databases is the best approach.

### Data synchronization (Full data synchronization)

- Sync tool allows users to synchronize data between remote databases with no effort.
- Approach used later is from [dbForge's](https://docs.devart.com/data-compare-for-sql-server/comparing-data/data-comparison-algorithm.html?utm_source=chatgpt.com#step-6-caching-the-comparison-results) algorithm for data comparison.


![Comparison schema](./assets/comparison%20schema.png)


- The algorithm relays on the following steps:

1. DB metadata retreival
2. Metadata comparison and object mapping - done automatically if possible
3. Choosing the comparison key, primary key by default
4. Retrieving data from both databases. Data is ordered by the comparison key.
5. Data comparison, row by row, not relying on the checksums.
6. Comparison results caching
7. Generating comparison document
8. Generating synchronization scripts

### Implementing this approach in DataGrip

- When implementing this approach in DataGrip we have a few hotspots to consider:
  - Metadata comparison and object mapping:
    - When we perform comparison between two databases, we want to align the tables and columns that are the same in both databases. 
    - Since that is not always possible, we need to provide a way for the user to map the tables and columns that are not aligned.
  - Choosing the comparison key:
    - By default, the primary key is used as the comparison key. However, the user should be able to choose a different key if needed.
    - Comparison key can be a composit key.
  - Data retrieval:
    - We are potentially dealing with large amounts of data, so we need to optimize the data retrieval process.
    - Retreiving data in chunks is a good approach. But we need a mechanism to keep track of the chunks that are already retreived and in case of a failure, to continue from the last chunk.
  - Data comparison:
    - Comparing data row by row is a time-consuming process. We need to optimize this process as much as possible.
    - Since the rows gathered are ordered by the comparison key, we can use this to our advantage and automatically group the rows of the same type.
      - Possible types are: IN LOCAL and IN TARGET. If present in both, we compare the real data (data hash) and if it is the same, we mark it as EQUAL or DIFFERENT.
  - Caching comparison results:
    - Since our operation is performed on a large amount of data, we need to cache the results of the comparison.
    - We can use a simple cache mechanism, where we store the comparison results in a file on the disk, in a previously generated groups.
  - Generating synchronization scripts:
    - By applying pre-defined rules, we process the comparison results and generate the synchronization scripts.
    - The scrpts are bi-directional, meaning that we can sync data from local to remote and vice versa.

### Scheduling synchronization tasks

- We are looking for a way to keep constant automatic synchronization between the databases.
- In this case we tend to use Incremental updates rather than full comparisons.

#### Flow of the incremental updates:
- When the databases are set for continuous synchronization, we need to keep track of the changes in the databases.
- There is multiple ways to do this, some are:
  - Using triggers on the tables that are being synchronized.
  - Writing logs of the changes, such as CDC (Change Data Capture) logs.

- More simple and reasonable approach is to use triggers on the tables that are being synchronized.
- When a change is made to the table, the trigger is fired and the data is stored in a log table.

- When initializing the continous synchronization, we need to define the maximum volume of changes to perform the synchronization.
  - My suggestion is to use the same size of the chunks that we used for the data retrieval. That makes data easier to process and to keep track of.

- On the initialization of the cont. synchronization, we need to perform a full comparison of the data, to make sure that the data is in sync.
- After that, we start the incremental updates and follow the state of the data in the log tables.
- Important notes for incremental updates
  - Our log data should get deleted after the synchronization is done to reduce the size of the log tables.
  - By keeping cache of the comparison results, we can reduce the time needed for the incremental updates since we can automatically group the data from the log tables.

 #### Execting the synchronization scripts

- Since SQL syntax differs from database to database, we need to provide a way to execute the synchronization scripts.
- We can use the existing functionality in DataGrip to execute the scripts.
- The scripts are executed in a transaction, so if the script fails, the transaction is rolled back and the data is not changed.


# Conclusion

- My main focus in reasearching this topic was to optimize data comparison and transfer.
- Since the topic is well researched, I have been able to find useful papers and articles that helped me to understand the data comparison and transfer process.
- This document presents a limited view on tool's capabilities, but it is a good starting point for further development of the tool.
- This tool can represent a valuable asset for developers and data engineers, as it can save time and effort in the process of data synchronization and transfer.
- In the context of distributed systems, this tool can be used to synchronize data between multiple databases, which is a common requirement in distributed systems. 
  - Useful paper on the topic is [Efficient Synchronization of State-based CRDTs](https://arxiv.org/pdf/1803.02750)
- Also a paper that gave me deeper understanding of data analysis and comparison is [COMPARE: Accelerating Groupwise Comparison in Relational Databases for Data Analytics (Extended Version)](https://arxiv.org/pdf/2107.11967)
- Solution provided might not satisfy DBMSs that are not SQL based, but surely it can be built upon to support other DBMSs.