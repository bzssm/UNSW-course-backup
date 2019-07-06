package hadoop.src;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.RunningJob;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.chain.ChainMapper;
import org.apache.hadoop.mapreduce.lib.chain.ChainReducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;


import java.io.IOException;
import java.util.*;

public class TFIDF {
    private static int totalDocuNo = 0;

    public static class DocumentMapper extends Mapper<Object, Text, Text, IntWritable> {
        private static int docNo;
        private final static IntWritable one = new IntWritable(1);
        private String word = new String();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString(), " *$&#/\t\n\f\"'\\,.:;?![](){}<>~-_");
            totalDocuNo++;
            docNo = Integer.parseInt(itr.nextToken());
            while (itr.hasMoreTokens()) {
                word = String.valueOf(docNo) + " " + itr.nextToken().toLowerCase() + " ";
                context.write(new Text(word), one);
            }
        }
    }

    public static class DocumentReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {

        public void reduce(Text key, Iterable<IntWritable> value, Context context) throws IOException, InterruptedException {
            String[] keySplit = key.toString().split(" ");

            int sum = 0;
            for (IntWritable val : value) {
                sum += Integer.parseInt(val.toString());
            }

            double tf = 1.0 * sum;
            String newkey = keySplit[1] + " " + keySplit[0];
            context.write(new Text(newkey), new DoubleWritable(tf));
        }
    }


//    public static class TFIDFMapper extends Mapper<Object, Text, Text, Text> {
//        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
//            String[] val = value.toString().split(" |\t");
//            if (val.length != 1) {
//                String word = val[0];
//                String docNoWithTF = val[1] + " " + val[2] + " 1";
//                context.write(new Text(word), new Text(docNoWithTF));
//            }
//
//        }
//    }
    public static class TFIDFMapper extends Mapper<Text, DoubleWritable, Text, Text> {
        public void map(Text key, DoubleWritable value, Context context) throws IOException, InterruptedException {
            String[] keys = key.toString().split(" |\t");
            String docNoWithTF = keys[1]+" "+value.toString()+" 1";
            context.write(new Text(keys[0]), new Text(docNoWithTF));


        }
    }

    public static class TFIDFReducer extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

            float fileCount = 0;
            Hashtable<Integer, String> words = new Hashtable<Integer, String>();
            for (Text val : values) {
                String[] vals = val.toString().split(" ");
                fileCount += Integer.parseInt(vals[2]);
                words.put(Integer.parseInt(vals[0]), vals[1]);
            }
            List<Integer> temp = new ArrayList<Integer>(words.keySet());
            Collections.sort(temp);
            double IDF = Math.log10((totalDocuNo * 1.0) / (fileCount * 1.0));
            for (Integer val : temp) {
                float TF = Float.parseFloat(words.get(val));
                context.write(key, new Text(val + "," + String.valueOf(TF * IDF)));
            }
        }
    }


    public static void main(String[] args) throws Exception {

//        Configuration conf1 = new Configuration();
//        Job job1 = Job.getInstance(conf1, "TFIDF Stage 1");
//        job1.setJarByClass(TFIDF.class);
//        job1.setMapperClass(DocumentMapper.class);
//        job1.setReducerClass(DocumentReducer.class);
////        job1.setPartitionerClass(MyPartitoner.class);
//        job1.setMapOutputKeyClass(Text.class);
//        job1.setMapOutputValueClass(IntWritable.class);
//        job1.setOutputKeyClass(Text.class);
//        job1.setOutputValueClass(Text.class);
//        job1.setNumReduceTasks(Integer.parseInt(args[2]));
//        FileInputFormat.addInputPath(job1, new Path(args[0]));
//        FileOutputFormat.setOutputPath(job1, new Path(args[1]));
//        job1.waitForCompletion(true);
//
//
//        Configuration conf2 = new Configuration();
//        Job job2 = Job.getInstance(conf2, "TFIDF Stage 2");
//        job2.setJarByClass(TFIDF.class);
//        job2.setOutputKeyClass(Text.class);
//        job2.setOutputValueClass(Text.class);
//        job2.setMapperClass(TFIDFMapper.class);
//        job2.setReducerClass(TFIDFReducer.class);
//        job2.setNumReduceTasks(Integer.parseInt(args[2]));
//        FileInputFormat.addInputPath(job2, new Path(args[1]));
//        FileOutputFormat.setOutputPath(job2, new Path(args[3]));
//        job2.waitForCompletion(true);

        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "Random?");
        job.setJarByClass(TFIDF.class);

        ChainMapper.addMapper(job, DocumentMapper.class, Object.class, Text.class, Text.class, IntWritable.class,new Configuration(false));
        ChainReducer.setReducer(job, DocumentReducer.class, Text.class, IntWritable.class, Text.class, DoubleWritable.class,new Configuration(false));
        ChainReducer.addMapper(job, TFIDFMapper.class, Text.class, DoubleWritable.class, Text.class, Text.class,new Configuration(false));


        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[3]));

    }

}
