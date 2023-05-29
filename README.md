# Python-based Recursive DNS Resolver

This project represents a custom-built Recursive DNS Resolver developed in Python, providing an in-depth exposure to DNS operations, recursive algorithms, and network programming. This resolver directly interacts with root DNS servers, handling a variety of DNS record types such as 'A', 'AAAA', 'CNAME', and 'MX'.


## Features

### Direct Interaction with Root Servers
The resolver doesn't rely on other recursive resolvers and directly communicates with root DNS servers to perform all recursive operations, providing an enriched understanding of DNS operations.

### Wide Range of DNS Record Handling
The tool handles 'A', 'AAAA', 'CNAME', and 'MX' record types, showcasing a comprehensive approach towards DNS query resolution.

### Robust Error Handling 
The system is well-equipped to deal with non-responsive or slow servers. It uses a timeout mechanism to manage delayed responses, underlining the importance of reliability in network programming.

### Efficient Caching System
To prevent repeated queries for the same domain and optimize network performance, a caching mechanism is implemented. This system also caches intermediate results, reinforcing the efficiency of the resolver.

### PEP8 Coding Standards 
The codebase adheres to PEP8 coding standards, emphasizing readability and maintainability.

### Command-line Interaction
Utilizing argparse, a Python standard library, the resolver offers command-line interaction, highlighting the effective use of Python libraries.


## Installation & Usage
This project relies on the dnspython library. You can install it by running pip install dnspython. Once installed, you can run the resolver by using the command python resolve.py <domain_name>.


## Author
### Mohammed Hisham Moizuddin
### https://www.linkedin.com/in/hishammoizuddin/
