package hadoop.src;

import java.util.HashSet;
import java.util.Hashtable;
import java.util.Set;

public class Test {

    public static int subcount(String[] str, String s){
        int res=0;
        for (String a:str){
            if (s.equals(a)){
                res++;
            }
        }
        return res;
    }
    public static void main(String args[]){
        String a = "aiu weiu aieu  weiu i";
        int index = a.indexOf(" ");
        System.out.println(a.substring(0,index));
        System.out.println(a.substring(index+1));

    }
}
