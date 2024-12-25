# AI powered Java to Kotlin conversion


## Improving the Java to Kotlin conversion experience with AI

- As we know static conversion does not provide the best results, we are introducing an AI powered Java to Kotlin conversion tool.
- This approach includes collecting, preprocessing and training data, and then using a machine learning model to convert Java code to Kotlin.


## Collecting data

### Special case
- *If the dataset already exists, this step can be skipped.*

### Usual case

- We need a large dataset of Java code and its corresponding Kotlin code.
- We can use open-source projects, GitHub repositories, and other sources to collect the data.
- Our target would be mobile native app codebases, that are in transition from Java to Kotlin.
- We can also use Libraries and SDKs that have both Java and Kotlin versions.
- While collecting the data, we need to ensure that the Java and Kotlin code are semantically equivalent. That is the first step of preprocessing.


## Preprocessing data

- The preprocessing step involves cleaning the data and ensuring that the Java and Kotlin code are semantically equivalent.
- Since we are using valid code snippets, we can skip the syntax validation step.
- We need to ensure that the Java and Kotlin code are functionally equivalent.
- Conventionally, we should use Java and Kotlin code pairs (paired by the name of the file) transfer code into a unified format such as AST (Abstract Syntax Tree) or tokenized format. Each unified entity should contain context such as dependencies, imports, and other necessary information.
- This strucutre allows us to form Call Graphs and represent method context in a more structured way.
    - Since Call Graphs are directed, they represent the flow of the program and are important for the conversion process as well as the later unpacking of the results.
- We are using method-level decomposition as an approach to reduce the overhead of input tokens and to make the model more efficient.
    - First methods for translation are Nodes with no dependencies (no calls to other methods).
    - In the dataset, each feature stores the code of the method and the **context** of the method. 
- Idea for this approach comes from the paper [Program Decomposition and Translation with Static Analysis](https://arxiv.org/pdf/2401.12412).
    - Decomposition is done to reduce the overhead of input tokens and to make the model more efficient.

## Choosing the model

- My main idea is to use a pre-trained model for the conversion process.
- The model should be fine-tuned on the dataset we collected.
- Some of the models that can be used are:
    - OpenAI Codex
    - Facebook's TransCoder

## Fine-tuning the model

- We need to fine-tune the model on the dataset we collected.
- Fine-tunning is performed on the preprcessed data and the pre-trained model.

## Evaluation

- We can evaluate the model on a test set.
- We can use BLEU score, ROUGE score, and other metrics to evaluate the model.
- We can also use human evaluation to evaluate the model, by that we can get feedback on the quality of the conversion by real developers.
- We can also use static analasys tools to evalute idomatic Kotlin code.

## Model improvement

- We can improve the model by collecting more data and fine-tuning the model on the new data.
    - When new entry passes the evaluation, it is added to the dataset and the model is retrained once in a while.


# Main problems

- Context is important for the conversion process, as well as the "unpacking of the results".
- Collecting data may present a challenge, as we need a large dataset of Java and Kotlin code pairs.
- Forming Abstract Syntax Trees (AST) and Call Graphs is a complex process, using a lot of resources.