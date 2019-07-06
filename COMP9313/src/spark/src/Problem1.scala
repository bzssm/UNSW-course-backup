import org.apache.spark.{SparkConf, SparkContext}

object Problem1 {
  def main(args: Array[String]) {
    var a = 0
    var b = 0
    val inputFilePath = args(0)
    val outputFilePath = args(1)
    val sc = new SparkContext(new
        SparkConf().setAppName("WordCount").setMaster("local"))
    val input = sc.textFile(inputFilePath)
    val words1 = input.map(_.toLowerCase().split("[\\s*$&#/\"'\\,.:;?!\\[\\](){}<>~\\-_]+"))
    val words = words1.map(line => line.filter(_.length() > 0)).map(line => line.filter(_.charAt(0).isLetter))
    val pairs = words.flatMap(line => {
      for (a <- 0 until line.length; b <- a + 1 until line.length) yield (line(a), (line(b), 1))
    })
    val fenmu = pairs.map(token => (token._1, token._2._2)).reduceByKey(_ + _)
    val fenzi = pairs.map(token => ((token._1, token._2._1), token._2._2)).reduceByKey((_ + _)).map(token => (token._1._1, (token._1._2, token._2)))
    val joined = fenzi join fenmu
    val res = joined.map(t => (t._1, t._2._1._1, t._2._1._2.toDouble / t._2._2.toDouble))
    val res1 = res.map(t => ((t._1, -1 * t._3, t._2), t))
    val res2 = res1.sortByKey()
    val res3 = res2.map(t => t._2._1 + " " + t._2._2 + " " + t._2._3)

    res3.saveAsTextFile(outputFilePath)
  }
}