# Distributed Persistent Project Indexing

In the following document, I will recap my analysis and potential solution to this issue.  
The approach following contains conceptual idea and not a detailed software architecture.  

# TRIE (Prefix trie)

- **Data structure** responsible for project structure representation.
    - *Example of a real-world project structure*

            MyApp/  
            ├── backend/  
            │   ├── src/  
            │   │   ├── config/
            │   │   │   └── db.js             
            │   │   ├── controllers/
            │   │   │   └── userController.js     
            │   │   ├── middleware/
            │   │   │   ├── authMiddleware.js     
            │   │   │   └── errorHandler.js       
            │   │   ├── models/  
            │   │   │   └── userModel.js          
            │   │   ├── routes/
            │   │   │   └── userRoutes.js         
            │   │   ├── services/
            │   │   │   └── userService.js        
            │   │   ├── utils/
            │   │   │   ├── logger.js             
            │   │   │   └── constants.js          
            │   │   ├── app.js                    
            │   │   └── server.js                 
            │   ├── package.json                  
            │   └── .env                          
            ├── frontend/
            ...        

- If we would to form a prefix trie based on this project structure, Nodes would be formed from parts of a filepath.
- Filesystem is a tree by itself. By doing the DFS we would conduct **whole words** (filepaths) from the system, and by doing that we could insert new words into our trie structure.
- Let's take the *userRoutes.js* filepath as an example. **MyApp/backend/src/routes/userRoutes.js** represents a whole word in our prefix trie. 
- Root node is MyApp, other nodes are backend, src, routes and the leaf os userRoutes.js.
- Each node stores the id (path) and the hashed (as well as the list of child node hash values) value on that node. (important for later analasys).  
- As we know it is a usual case to have nodes with only one child. In that case, we could merge those nodes into one and construct a more compact trie.
- By doing that we would minimize the memory footprint of the trie structure.
- Leaf in this trie structure can be a file or a code construct like a function, class, variable, etc. By storing the hashed value of the file, we could easily track the changes in the file as well as the subcomponent changes.



### **Querying the trie**

- Initialy we perform a query on Bloom Filter to check if the file exists in the project structure.
- When we want to search for a specific file, we would do the DFS on the trie structure.
- We would start from the root node and go down the tree until we reach the leaf node.
- If we reach the leaf node, we would return the path to the file.

### **Updating the trie**

- Since our goal is to minimize redundancy, we would need to update only the part of the trie that is affected by the change.

### **Optimizing the trie**

- As we mentioned earlier, we could merge nodes with only one child into one node.

- **Bloom Filter** could present a reasonable optimization in search time. 
    - Bloom filter is a probabilistic data structure that is used to test whether an element is a member of a set. 
    - It may return false positives, but it will never return false negatives.
    - We could use it to check if the file exists in the project structure before we start the DFS on the trie structure.
    - Since bloom filter allows us to check if the element is in the set in O(1) time complexity  (depending on hash function time complexity), we could save a lot of time in the search process.
    - Huge datasets could be stored in a bloom filter with a small memory footprint.
    - When initializing the trie for a specific project, we have the information on the expected size of the dataset. We could adjust the size of the bloom filter accordingly by leveraging the false positive rate.


# AST (Abstract Syntax Tree)

- **Data structure** responsible for code representation.
- We could use AST to analyze the codebase and extract the code constructs.
- AST represents a unified structure of the codebase, regardless of the programming language.
- Since our trie leaf nodes represent the files (and file subcomponents), each AST is the is the prequisite for the trie leaf node.
- AST allows us to extract information about dependencies and relationships between files.



# Dependency Graph

- **Data structure** responsible for dependencies representation.
- We could use the dependency graph to represent the relationships between files (as well as the file subcomponents).
- Nodes with their ids and hashed values are present in the trie, and the dependency graph would store its component hash and id.

- **Directed Acyclic Graph (DAG)** could be used to represent the dependencies between files.
    - Nodes in the graph represent files, functions, classes, variables, etc.
    - Edges represent the dependencies between these entities.
    - By traversing the graph, we could analyze the dependencies and relationships between files, etc.
    - Inital representation idea is the simple hashmap where the key is the node id and the value is the list of nodes that depend on that node.
        - Using a hashmap allows us to quickly access the dependencies of a specific node, but introduces memory overhead. 
        - This approach is not optimal for the large codebases, and we could use more advanced data structures like adjacency list or adjacency matrix or even graph databases.
    

# Project Workflow

- **Initialization**
    - When the project is initialized, we would construct the prefix trie, analyze the codebase to extract the AST, and build the dependency graph, as well complete the trie with AST prequisited constructs.
    
    - Initial structures are stored on a distributed server.

    - **Change tracking**
        - When developer intializes the local project instance, automatically the local trie is initialized as well as the local dependency graph.
        - When the developer makes a change, affected nodes are marked as dirty.
        - Only when developer triggers merge request, the hash values are recalculated and the merge process starts.
        - Hash recomputation is performed as if the trie is a Merkle tree. The result is the root node hash. 
        - Since only the affected nodes are updated, the process is efficient.
        - The merge process is distributed across the servers, and the final result is stored in the distributed server.
        - The developer can pull the changes from the distributed server to update the local project instance.

    - **Merge workfklow**
        - After triggering the merge request, new root hash is compared with the distributed server root hash.
        - If the hashes are the same no merge is needed.
        - If the hashes are different we continue the trie traversal until we find  the subtree that has a different root hash.
        - After localizing the subtree, we need to display the affected dependencies and files.
        - Request to the dependency graph is sent and the affected nodes are displayed.
            - Changed node is fetched and the affected nodes are recieved as a response.
        - The developer can resolve the conflicts and complete the merge.
        - After the merge is completed, the new root hash is calculated and stored on the distributed server. 
        - Only the affected nodes are updated in the trie as well as in the dependency graph.
        - Further optimizations allow batch updates of the nodes to minimize the number of requests to the distributed server.
        - Some more advanced optimizations could be implemented like caching.
        - Certain merge requests could be automated based on the predefined rules.
        - Since our dependency graph is  a forrest of trees, we could leverage the parallel processing to speed up the merge process.
        - Each tree represents a file or a module, and we could merge the trees in parallel.
        - Precomputed hash values even on base level allow us to quickly determine the differences between the tree nodes and speed up the conflict resolving process.


    - **Distributed system**
        - An important part of distributing the system is a Load Balancer.
        - The distributed system is responsible for storing the project structures and handling the merge requests.
        - Data is stored in a distributed database, and the system is scalable.
        - Horizontal scalability is achieved by adding more servers and sharding data across them.
        - Sharding algorithms are to be defined. But my initial idea is to shard the data based on the geographical location.
    
# Issues

- **Node failures**
    - In case of node failure, the system should be able to recover the data.
    - This could be achieved by action and data logging, performing an approach like  **WAL (Write-Ahead Logging)**.
    - By storing the actions and data changes in the log, we could recover the system to the previous state.
    - After the data is synchronized, logs could be deleted to prevent the memory overhead.

- **Network operations overhead**
    - Since the system is distributed, network operations could introduce latency.
    - We could optimize the network operations by using caching, batching, and parallel processing.
    - Caching could be used to store the frequently accessed data.
    - Batching could be used to minimize the number of requests to the distributed server.
    - Parallel processing could be used to speed up the merge process.

