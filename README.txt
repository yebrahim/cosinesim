consinesim - a Cosine Similarity computation script for a collection of documents
----

This script takes a collection of documents that represent TF-IDF tokens from news articles (other measures can work too, provided they comply with the parsing format of this script). It also takes an additional file that describes votes for a number of users that we need to compute the cosine similarity between. It then computes the similarity in one of three modes:
    - User to user. In this case two user IDs are specified to the program. It outputs only one number representing similarity between the two users
    - User to all. Only one user is specified, and the similarities are calculated between this user and all other users. Output file will contain a one-dimensional table that describes similarities with other users.
    - All to all. No users are specified, and in this case the output file will contain also a one-dimensional table that has one entry per pair of users, and the corresponding similarity.

Please respect the following format, or modify the code yourself to fit your instances:
    - The user_vector.txt file:
        u1: item1, item2
        u2: item1
        u3: item2, item3
        ...
        ...

    - The documents containing the TF-IDF pairs look like:
        term1   tf-idf-score
        term2   tf-idf-score
        ...
        ...
The supplied example files demonstrats the rules above

Usage:
    python cosinesim [options] user_vectors.txt document_dir

Type -h to get a better explanation of the different directivs.

Please direct any comments, corrections, or questions to me at yasser [dot] ebrahim [at] gmail [dot] com.
