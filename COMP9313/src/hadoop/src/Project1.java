package hadoop.src;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


import java.io.IOException;
import java.util.*;

public class Project1 {
    private static int totalDocuNo = 0;

    public static int subcount(String[] str, String s) {
        int res = 0;
        for (String a : str) {
            if (s.equals(a)) {
                res++;
            }
        }
        return res;
    }

    public static class DocumentMapper extends Mapper<Object, Text, Text, Text> {
        private int totalDocNo = 0;

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            int index = value.toString().indexOf(" ");
            totalDocuNo++;
            int docNo = Integer.parseInt(value.toString().substring(0, index));
            String[] tokens = value.toString().substring(index + 1).split(" ");
            Set<String> s = new HashSet<>();
            for (String token : tokens) {
                if (!s.contains(token.toLowerCase())) {
                    s.add(token.toLowerCase());
                    context.write(new Text(token.toLowerCase()), new Text(String.valueOf(docNo) + " " + String.valueOf(subcount(tokens, token))));
                }
            }

        }
    }

    public static class DocumentReducer extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> value, Context context) throws IOException, InterruptedException {
//            System.err.println(key.toString());


            Hashtable<Integer, Integer> words = new Hashtable<Integer, Integer>();
            int n = 0;
            for (Text val : value) {
                int docID = Integer.parseInt(val.toString().split(" ")[0]);
                int tf = Integer.parseInt(val.toString().split(" ")[1]);
                words.put(docID, tf);
                n++;
            }
            List<Integer> temp = new ArrayList<Integer>(words.keySet());
            Collections.sort(temp);
            for (Integer val : temp) {
                double tfidf = 1.0 * words.get(val) * Math.log10((1.0 * totalDocuNo) / (1.0 * n));
                context.write(new Text(key.toString()), new Text(String.valueOf(val) + "," + String.valueOf(tfidf)));
            }
        }
    }

    public static void main(String[] args) throws Exception {

        Configuration conf1 = new Configuration();
        Job job1 = Job.getInstance(conf1, "TFIDF Stage 1");
        job1.setJarByClass(Project1.class);
        job1.setMapperClass(DocumentMapper.class);
        job1.setReducerClass(DocumentReducer.class);
//        job1.setPartitionerClass(MyPartitoner.class);
        job1.setMapOutputKeyClass(Text.class);
        job1.setMapOutputValueClass(Text.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(Text.class);
        job1.setNumReduceTasks(Integer.parseInt(args[2]));
        FileInputFormat.addInputPath(job1, new Path(args[0]));
        FileOutputFormat.setOutputPath(job1, new Path(args[1]));
        job1.waitForCompletion(true);

    }
}
