import org.apache.spark.{SparkConf, SparkContext}

object RSJoin {
    def main(args: Array[String]): Unit = {
        // Configuration
        val inputFile1 = "src/unsorted1/file1"
        val inputFile2 = "src/unsorted1/file2"
        val outputFile = "resUnsorted"
        val threshold = "0.8".toDouble
        // Spark Config
        val conf = new SparkConf().setAppName("SetSimJoin").setMaster("local")
        val sc = new SparkContext(conf)
        
        val input1 = sc.textFile(inputFile1)
        val input2 = sc.textFile(inputFile2)
        
        // Cal token freq from R
        val freqR = input1.flatMap(_.split(" ").drop(1))
            .map(word => (word, 1))
            .reduceByKey(_ + _)
            .collect()
            .toMap
        
        // Cal token freq from S
        val freqS = input2.flatMap(_.split(" ").drop(1))
            .filter(word => freqR.keySet.contains(word))
            .map(word => (word, 1))
            .reduceByKey(_ + _)
            .collect()
            .toMap
        
        // Joint freq
        val freq = freqR ++ freqS.map(t => t._1 -> (t._2 + freqR.getOrElse(t._1, 0)))
        
        //Mapping token
        val RPrefix = input1.flatMap(line => {
            val index = line.split(" ")(0)
            val token = line.split(" ").drop(1).map(_.toInt).sorted.map(_.toString)
            val sortedtoken = token.sortBy(x => freq.getOrElse(x, 0))
            sortedtoken.dropRight(math.ceil(token.length * threshold).toInt - 1)
                .map {
                    (_, List((index, token)))
                }
        })
        
        val SPrefix = input2.flatMap(line => {
            val index = line.split(" ")(0)
            val token = line.split(" ").drop(1).map(_.toInt).sorted.map(_.toString)
            val sortedtoken = token.sortBy(x => freq.getOrElse(x, 0))
            sortedtoken.dropRight(math.ceil(token.length * threshold).toInt - 1)
                .map {
                    (_, List((index, token)))
                }
        })
        
        // Joint prefix, only join two lines which have at least one same token in prefix
        (RPrefix join SPrefix)
            .values
            .map({ case (List((a, b)), List((c, d))) =>
                (a, c) -> b.intersect(d).distinct.length.toDouble / b.union(d).distinct.length.toDouble
            })
            // Threshold filter
            .filter(_._2 >= threshold)
            // To int to sort
            .map({ case ((a, c), sim) =>
                (a.toInt, c.toInt) -> sim
            })
            //remove redundancy
            .reduceByKey((v1, v2) => v1)
            .sortByKey()
            //output
            .map(x => x._1 + "\t" + BigDecimal(x._2).setScale(6, BigDecimal.RoundingMode.HALF_UP).toDouble)
            .saveAsTextFile(outputFile)
    }
}