

from searchTweets import *
import unittest
import time
from pathlib import Path


class TestTweet(unittest.TestCase):

    def compareFiles(self, count):

        while count:
            outputFolder = Path("./Output/")
            file1 = "ExpectedOutput_"+str(count)+".csv"
            file2 = "Output_"+str(count)+".csv"

            with Path(outputFolder/file1).open("r") as f1, Path(outputFolder/file2).open("r") as f2:

                f1Lines = f1.readlines()
                f2Lines = f2.readlines()

                for i in range(len(f1Lines)):
                    if f1Lines[i] != f2Lines[i]:
                        print("These 2 files don't match \n")
                        print("Expected output file"+".\Output\ExpectedOutput_"+str(count)+".csv" + " " +
                              " does not match with obtained output file  "+" " + ".\Output\Output_"+str(count)+".csv")
                        return False
                count -= 1

        return True

    def test_query(self):
        ti = Tweet()
        tweet_csv_filename = "tweets.csv"
        qFolder = Path("./Test/")
        qfile = "query.txt"

        with Path(qFolder/qfile).open("r") as q:
            qlines = q.readlines()
            qfileLen = len(q.readlines()) + 1

            for count, qline in enumerate(qlines):
                ti.topTweets(count, qline, tweet_csv_filename)

        self.assertEqual(self.compareFiles(qfileLen), True)
        print("All files match!")

    def test_timeBenchmark(self):
        ti = Tweet()
        tweet_csv_filename = "tweets.csv"
        qFolder = Path("./Test/")
        qfile = "query.txt"

        with Path(qFolder/qfile).open("r") as q:
            qlines = q.readlines()

            for count, qline in enumerate(qlines):
                startTime = time.process_time()
                ti.topTweets(count, qline, tweet_csv_filename, numTweets=5)
                executionTime = (time.process_time() - startTime)
                print("EXECUTION TIME =>", executionTime)


if __name__ == "__main__":
    unittest.main()
