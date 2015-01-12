# MapReduce
MapReduce using Apache Spark framework; Strongly solving the "15 Puzzle".

Puzzles like the "15 Puzzle" have the property that you can get from any position (a particular unique configuration of the puzzle) to another; there are no "dead ends".
In this project, I wrote a breadth-first solver that starts from the single solution position, and walks the graph, recording every new position it reaches (and how many moves it took to get there - called the level).
Unlike breadth-first search, in which you stop when you've found a particular position, here I exhaustively visit the entire graph (strongly solving).
To do this, we keep track of two mappings:
pos_to_level: Given a position, what is its level? 
level_to_pos: Given a level, what are all the positions?

- SlidingBfsSpark.py contains the MapReduce job to solve a (Width x Height) Sliding puzzle.
- Makefile defines the configurations for the run commands including the size of the sliding puzzle, and the level of parallelism to use. 
- SlidingBfsReference.py contains the iterative breadth-first search implementation of a Sliding puzzle solver described above. This is used to  verify the correctness of the output.
- Sliding.py defines helper functions to produce solutions and children of WxH Sliding puzzle "objects" (which are Python tuples).

After running the MapReduce job, the program writes to a text file in the following form. (for example, for a 2x2 case):

0. ('A', 'B', 'C', '-')
1. ('A', '-', 'C', 'B')
1. ('A', 'B', '-', 'C')
2. ('-', 'A', 'C', 'B')
2. ('-', 'B', 'A', 'C')
3. ('B', '-', 'A', 'C')
3. ('C', 'A', '-', 'B')
4. ('B', 'C', 'A', '-')
4. ('C', 'A', 'B', '-')
5. ('B', 'C', '-', 'A')
5. ('C', '-', 'B', 'A')
6. ('-', 'C', 'B', 'A')	

For more on Spark-Python API : http://spark.apache.org/docs/latest/api/python/pyspark-module.html

The code was also made to run on a large cluster of Amazon Web Services Elastic Compute Cloud (AWS EC2) servers in order to crunch through a large problem.
