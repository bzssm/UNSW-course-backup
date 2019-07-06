import org.apache.spark.graphx._
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf

object Problem2 {
  def main(args: Array[String]) {
    val conf = new SparkConf().setAppName("SSSP").setMaster("local")
    val sc = new SparkContext(conf)

    val fileName = args(0)
    val k = args(1)
    val edges = sc.textFile(fileName)

    val edgelist = edges.map(x => x.split(" ")).map(x => Edge(x(1).toLong, x(2).toLong, 1.0))
    val graph = Graph.fromEdges[Double, Double](edgelist, 0.0)

    var cycles = graph.vertices.collect().flatMap(v => {
      for (e <- graph.edges.collect() if e.srcId == v._1) yield (List(e.srcId, e.dstId))
    })
    for (i <- 1 until k) {
      cycles = cycles.flatMap(c => {
        for (e <- graph.edges.collect() if e.srcId == c.last) yield (c ::: (List(e.dstId)))
      })
    }
    val lenk = cycles.filter(_.distinct.length == k)
    val cyclek = lenk.filter(pair => pair.head == pair.last)
    val res = cyclek.length/k

    println(res)


  }
}