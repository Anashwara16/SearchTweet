
import csv
import re
from heapq import heappop, heappush, heapify
import argparse
import readline
from pathlib import Path


class Tweet:

    # Preprocess query string against the given tweet (Case insensitive check).
    def preprocess(self, query, tweet):
        result = []

        for q in query:
            if q in "&|()!":
                result.append(q)

            elif q[0] == "!" and len(q) > 1:
                result.append(1) if q[1:].lower(
                ) not in tweet else result.append(0)

            else:
                result.append(1) if q.lower() in tweet else result.append(0)

        return result

    # Evaluate the boolean expression obtained from preprocessing.
    def evaluate(self, s) -> int:

        stack = []
        operand = 0  # Store the operand
        res = 0  # Running result
        prod = 1  # for sub-expressions involving '&'
        add = 0  # for sub-expressions involving '&'
        operators = ["&", "|", "(", ")", "!"]
        symbol = 1
        counter = 0
        # Variable that indicates if there is a prefix '!' operator.
        prefixNot = False

        # Evaluate the expression to left.
        for i, ch in enumerate(s):

            # If ch is not an operator, store it in operand.
            if ch not in operators:
                operand = ch

            # Evaluate expression to the left.
            elif ch == '&':
                # Start of a new sub-expression? retain the operand.
                if counter < 2:
                    res = (prod and operand)
                else:
                    res = (res and operand)
                symbol = ch

            # Evaluate expression to the left.
            elif ch == '|':
                # Start of a new sub-expression? retain the operand.
                if counter < 2:
                    res = (add or operand)
                else:
                    res = (res or operand)
                symbol = ch

            # If there is a prefix '!' operator, update the prefixNot variable.
            elif ch == '!':
                prefixNot = True

            # Store result and operator(s) obtained so far, onto the stack for later use.
            elif ch == '(':
                if counter >= 2:
                    stack.append(res)
                    stack.append(symbol)

                if prefixNot:
                    stack.append('!')
                    prefixNot = False

                # Reset variables for evaluation of new sub-expression.
                res = 0
                counter = -1

            elif ch == ')':

                # Evaluate the sub-expression within these parentheses.
                if symbol == '&':
                    res = (res and operand)
                if symbol == '|':
                    res = (res or operand)
                # Reset symbol
                symbol = 0

                # After evaluating the parentheses, check if the parentheses have a prefix '!' operator
                # by checking the top of the stack & update the result accordingly.
                while stack and stack[-1] == '!':
                    stack.pop()
                    res = int(not(res))

                # Evaluate all the previously stored values on the stack.
                while stack:
                    oper = stack.pop()
                    first = stack.pop()
                    if oper == "&":
                        res = (res and first)
                    if oper == "|":
                        res = (res or first)

            counter += 1

        # Evaluate any pending operations.
        if symbol == "&":
            res = (res and operand)
        if symbol == "|":
            res = (res or operand)

        # Return the boolean result.
        return bool(res)

    # Extract the top 5 tweets from the given file that satisfies the provided query expression.
    def topTweets(self, count, query, tweets, numTweets=5):

        # MaxHeap that stores all the tweets in the provided file.
        list_of_tweets = []

        with open(tweets, "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                timestamp = int(row[0])
                tweet = str(row[1])
                heappush(list_of_tweets, [(-1)*timestamp, tweet])

        heapify(list_of_tweets)

        # Filter & format the query string
        query = list(filter(None, re.split(r'([&|()])', query)))
        query = list(q.strip().lower() for q in query)
        query = list(filter(None, query))

        # Open a file to write the output to.
        outputFolder = Path("./Output/")
        outputFolder.mkdir(parents=True, exist_ok=True)
        fileName = "Output_"+str(count+1)+".csv"
        outputFile = outputFolder / fileName
        topfive = 0  # top 5 tweets counter

        # Pop, preprocess and evaluate tweets to obtain the top 5 tweets that satisfy
        # the provided query string.
        with Path(outputFile).open("w") as ofile:
            while list_of_tweets:
                tweet = heappop(list_of_tweets)[1]
                heapify(list_of_tweets)
                processed = self.preprocess(query, tweet)
                calcResult = self.evaluate(processed)

                if calcResult:
                    ofile.write(tweet+"\n")
                    topfive += 1
                    if topfive == numTweets:
                        break

        #ofile = open(".\Output\Output_"+str(count+1)+".csv", "r")
        # print(ofile.read())
    # self.compareFiles(count-1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=' Search Top 5 Tweets: ')
    parser.add_argument(
        '-i', '--input', help='Provide input tweets csv file (default - tweets.csv)', default='tweets.csv', required=False)
    parser.add_argument(
        '-q', '--query', help='Provide query file (default - query.txt)', default='query.txt', required=False)
    args = parser.parse_args()

    t = Tweet()
    qfile = "query.txt"

    with open(qfile, "r") as q:
        qline = q.readline()
        t.topTweets(0, qline, args.input)
