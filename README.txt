1. OBSERVATIONS:


a. This problem requires the algorithm to perform two operations mainly: i) Sort tweets by timestamp (to access tweets in a non-increasing timestamp order) ii) Match query expression with the tweets.  


b. We can calculate the time complexities of these operations and decide which of them is more compute intensive. Let’s consider N as the total number of tweets in the list of tweets. Consider K as the length of each tweet (worst case: 280 characters) and M as the length of the query expression. With these considerations, we can calculate time complexities as follows: 
   1. Sorting list of tweets - O(N*logN)
   2. Matching the query string against each tweet - O(N*K*M)


c. For the given dataset, we can assume that matching query expression with the tweets is more compute intensive than sorting the entire list of tweets. 


d. From the dataset of tweets, we need to output only the five most recent tweets that match our query expression. If we had a sorted list of tweets by timestamp, the number of matching operations could be reduced if the first few tweets match the query string. 


2. APPROACH: 
Max Heap to sort and store list of tweets and Stack for evaluating the query expression against the tweet. 


3. INTUITION: 
The intuition behind this approach is to start analyzing tweets in a non-increasing order of their timestamp and match them against the query expressions. 

The query expression is evaluated from left to right. To ensure that the subexpression inside nested parentheses are evaluated first, we utilize a stack. The result is evaluated on the go, as it will be convenient to analyze expressions and also reduces the number of push and pop operations.  


4. EXPLANATION: 
As we analyze tweets in a non-increasing order of their timestamp, we use a max heap to provide us with the most recent tweet in O(1) operation. 

While iterating through the string, we store the operands and operators and evaluate them on-the-go. This result is stored in an ongoing/running variable. This would be the best case scenario, where we would not need a stack. 

In case of expressions with nested parentheses: the running result and the last observed operator, is stored in the stack, whenever an opening parenthesis is encountered. The opening parenthesis indicates the start of a new sub-expression, which will be evaluated in an ongoing manner. As we iterate through this sub-expression, if we encounter a closing parenthesis, this marks the end of the sub-expression. This subexpression’s result is operated on with the previous result, as per the operator stored in the stack. In this manner, subexpressions within parentheses are evaluated and then resolved with the previous result in an ongoing manner, therefore, ensuring that the left hand side of the expression is always evaluated. 


5. ALGORITHM: 
   1. Store the list of tweets in a max heap, based on its timestamp. In this max heap, the root at any point, would be the most recent tweet. 
   2. Preprocess the query string against the given tweet and create a boolean expression. 
   3. The resultant boolean expression is then evaluated based on the observance of a boolean operator. If a boolean operator is encountered, we need to first evaluate the expression to the left and then save this operator for the next evaluation.
   4. If we encounter an opening parenthesis ‘(‘, the ongoing result calculated so far and the operato are pushed on to the stack. The ongoing variables are reset, as we start to evaluate a new subexpression. 
   5. If we encounter a closing parenthesis ‘)‘, we evaluate the expression to the left, thus, evaluating the current subexpression, which is present within the set of parentheses that just got concluded. 
   6. This new result is then evaluated with the values stored on the stack. 
   7. The final boolean result is returned, which indicates whether the given tweet satisfies the query expression or not.


6. COMPLEXITY ANALYSIS: 

TIME COMPLEXITY: 
1. Heap: 
   1. Building the heap requires O(N*logN). 
   2. While extracting the top tweets from this heap, we pop the most recent tweet (root of the heap) and then heapify this list. This operation in best case takes only O(K*logN), wherein K is the number of recent tweets required. In the worst case, we would have to search through the entire list, resulting in a time complexity of O(N*logN). 


2. Query expression:
   1. Preprocessing: 
The query string is first preprocessed, to compare against the given tweet. This operation takes O(K*M). The resultant boolean expression is then evaluated. 
   2. Stack evaluation: 
* The best case time complexity for evaluating the query string expression obtained from the preprocessing, could be O(1), wherein there are no parentheses and only the operand and operator variables are used. 
* The query string can be considered to have a worse time complexity of O(k), where k is the length of the boolean expression. The query string’s character is stored in a stack, only in case of nested expressions. In addition, not all characters are stored in the stack even in case of nested expressions. 
* Characters are pushed onto the stack only when opening parentheses are encountered and popped for processing the subexpression when a closing parenthesis is observed. Hence, the total time complexity of these two operations is O(K*M). 


SPACE COMPLEXITY: 
1. Query stack: O(k), where k is the length of the boolean expression.
2. Max Heap: O(N), where N is the number of tweets in the input file. We store all the tweets in a heap for ease of extracting the most recent tweet(s). 


THIS SOLUTION IS MORE OPTIMAL COMPARED TO THE STARTER CODE FOR THE FOLLOWING REASONS:

1. The starter code iterates through the entire list of tweets and searches for tweets that match with all the words in the query. This approach is cubic, and has to iterate through the entire list of tweets just to ensure that there are no ‘more recent’ tweets than the current matched ones. The best case scenario would still require O(K*M*N), where K is the length of the query string, M is the length of the tweet and this has to be evaluated for a total of N tweets. 

2. In contrast, the usage of a max heap data structure in this solution ensures that the tweet that is extracted on every heap-pop, is always the most recent one. This provides
an opportunity for the algorithm to terminate quickly if the matching tweets happen to be recent. 



HOW TO RUN THIS PROGRAM: 

To run this program, the input required are: 
1. File containing the program - searchTweets.py 
2. File containing tweets - tweets.csv
3. File containing the query expression - query.txt


python3 .\searchTweets.py -h

usage: searchTweets.py [-h] [-i INPUT] [-q QUERY]

Search Top 5 Tweets:

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Provide input tweets csv file (default - tweets.csv)
  -q QUERY, --query QUERY
                        Provide query file (default - query.txt)

The output will be stored in ‘.\Output\Output_1.csv’. 

The unit test filename is - tweetsTest.py

Unit testing was performed to check the following: 
1. Query file containing multiple query expressions. This query file is stored in 'Test' folder. 
2. Compare if the output files matched with the expected output files or not. 
3. Output the time benchmarks for each execution. 

