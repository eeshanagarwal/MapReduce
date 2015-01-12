from pyspark import SparkContext
import Sliding, argparse

def bfs_map(value):
    if value[1] != level:   #check if the level of the configuration passed in matches the current level
        return [value] #if it doesn't match the current level, return without re-mapping it (ie. do not call children on it)
    children = []
    children.append((value[0], level))
    for child in Sliding.children(WIDTH, HEIGHT, value[0]): #get a list of all the children for the current configuration
        children.append((child, level+1))   #append every child to the list of children
    return children

def bfs_reduce(value1, value2):
    return min(value1, value2) #as we are reducing by key, same configurations will be reduce by this method, and so pick the the one with the lowest level and remove the duplicate

def solve_sliding_puzzle(master, output, height, width):

    """
    Solves a sliding puzzle of the provided height and width.
     master: specifies master url for the spark context
     output: function that accepts string to write to the output file
     height: height of puzzle
     width: width of puzzle
    """
    # Set up the spark context. Use this to create your RDD
    sc = SparkContext(master, "python")

    # Global constants that will be shared across all map and reduce instances.
    # You can also reference these in any helper functions you write.
    global HEIGHT, WIDTH, level
   
    # Initialize global constants
    HEIGHT=height
    WIDTH=width
    level = 0 # this "constant" will change, but it remains constant for every MapReduce job

    # The solution configuration for this sliding puzzle. You will begin exploring the tree from this node
    sol = Sliding.solution(WIDTH, HEIGHT)
    
    rdd = sc.parallelize([(sol, level)]) #create an RDD from sol
  
    """ YOUR MAP REDUCE PROCESSING CODE HERE """
    size= WIDTH*HEIGHT*2 #store twice the size of the current configuration
    check = 0 #check is a flag to break out of the while loop when bfs has finished strongly solving the puzzle

    while check == 0:

        if level % 4 == 0 and level >= size:
            count1 = rdd.count()
       
        rdd = rdd.flatMap(bfs_map).reduceByKey(bfs_reduce) #tranfsform the rdd by calling flat_map and reducing it further

        if level % 4 == 0 and level >= size:
            count2 = rdd.count()
            if count1 == count2: #check if the size of the rdd has changed in subsequent iterations
                check = 1 #if the size has not changed, we are done transforming the rdd

        if level % 8 == 0: #partion the rdd on every 8th iteration
            rdd = rdd.partitionBy(16, lambda x: hash(x)) #hash-partition the rdd into 16 partitions and with accordance to python's default hash function

        level = level + 1

    """ YOUR OUTPUT CODE HERE """

    for board in rdd.collect():
        output(str(board[1]) + " " + str(board[0]))

    sc.stop()

""" DO NOT EDIT PAST THIS LINE

You are welcome to read through the following code, but you
do not need to worry about understanding it.
"""

def main():
    """
    Parses command line arguments and runs the solver appropriately.
    If nothing is passed in, the default values are used.
    """
    parser = argparse.ArgumentParser(
            description="Returns back the entire solution graph.")
    parser.add_argument("-M", "--master", type=str, default="local[8]",
            help="url of the master for this job")
    parser.add_argument("-O", "--output", type=str, default="solution-out",
            help="name of the output file")
    parser.add_argument("-H", "--height", type=int, default=2,
            help="height of the puzzle")
    parser.add_argument("-W", "--width", type=int, default=2,
            help="width of the puzzle")
    args = parser.parse_args()


    # open file for writing and create a writer function
    output_file = open(args.output, "w")
    writer = lambda line: output_file.write(line + "\n")

    # call the puzzle solver
    solve_sliding_puzzle(args.master, writer, args.height, args.width)

    # close the output file
    output_file.close()

# begin execution if we are running this file directly
if __name__ == "__main__":
    main()
