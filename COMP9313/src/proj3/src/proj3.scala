import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object proj3 {
    
    def main(args: Array[String]) {
        
        val inputFile1 = "src/small/file1"
        val inputFile2 = "src/small/file2"
        val outputFile = "res"
        val threshold = "0.1".toDouble
        //
        val conf = new SparkConf().setAppName("SetSimJoin").setMaster("local")
        
        val sc = new SparkContext(conf)
        val input1 = sc.textFile(inputFile1)
        val input2 = sc.textFile(inputFile2)
        val input = sc.union(Seq(input1, input2))
        val sep = input1.collect().length
        
        //      compute tokens frequency
        val freq = sc.broadcast(input.flatMap(_.split(" ").drop(1))
            .map(word => (word.toInt, 1))
            .reduceByKey(_ + _)
            .collect
            .toMap)
        
        //      .collect
        //      .toMap)
        //      .sortBy(_._2)
        //      .keys
        //      .toLocalIterator
        //      .toList
        
        
        val test1 = input1.map(x => x.split(" ").map(_.toInt)).map(x => (x(0), x.drop(1)))
            .map(x => (x._1, x._2.sortWith((x, y) => x < y).sortBy(e => freq.value(e))))
            .map(x => (x._1, x._2.toList))
            .flatMap(x => {
                for (i <- 0 until x._2.length) yield (x._2(i), x)
            })
        
        
        val test2 = input2.map(x => x.split(" ").map(_.toInt)).map(x => (x(0), x.drop(1)))
            .map(x => (x._1, x._2.sortWith((x, y) => x < y).sortBy(e => freq.value(e))))
            .map(x => (x._1, x._2.toList))
            .flatMap(x => {
                for (i <- 0 until x._2.length) yield (x._2(i), x)
            })
        //            .filter()
        //
        //    test1.first()._2.foreach(println)
        
        //    test1.saveAsTextFile("res")
        val test = (test1 join test2)
            //    test.saveAsTextFile("res1")
            .values //.map({ case ((a,b),(c,d)) => List((a, b), (c, d)) }) //.saveAsTextFile("res1")
            .filter({
            case ((a, b), (c, d)) =>
                b.length >= d.length * threshold && d.length >= b.length * threshold
        })
        
        val transformedTest = test.map({ case ((a, b), (c, d)) => ((a, c), (b, d)) }).reduceByKey((v1, v2) => v1)
        //    compute Jaccard similarity
        val t2 = transformedTest.mapPartitions(line => {
            line.map({
                case ((a, c), (b, d)) =>
                    val sim = b.intersect(d).distinct.length.toDouble / b.union(d).distinct.length.toDouble
                    (a, c) -> sim
            })
        })
        
        //     remove duplicates
        //      .reduceByKey((v1, v2) => v1)
        
        //     filter similary > threshold
        t2.filter(_._2 >= threshold)
            //      .sortBy(_._2)
            .sortByKey()
            .map(x => x._1 + "\t" + BigDecimal(x._2).setScale(6, BigDecimal.RoundingMode.HALF_UP).toDouble)
            .coalesce(1)
            .saveAsTextFile(outputFile)
    }
}
