import weka.core.Instances;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import weka.filters.unsupervised.attribute.NumericToNominal;
import weka.filters.Filter;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.Evaluation;
import java.util.Random;
import weka.classifiers.meta.FilteredClassifier;
import weka.filters.supervised.instance.SMOTE;
import weka.filters.supervised.instance.SpreadSubsample;

public class samplingFilter {
	public static void main(String[] args) throws Exception{
		File dir = new File("data/arff");
		File[] directoryListing = dir.listFiles();
		for (File child : directoryListing) {
			BufferedReader reader = new BufferedReader(
	                new FileReader(child));
			Instances data = new Instances(reader);
			reader.close();
			// setting class attribute
			data.setClassIndex(data.numAttributes() - 1);
			// setting class attribute from numeric to nominal
			NumericToNominal convert= new NumericToNominal();
	        String[] options= new String[2];
	        options[0]="-R";
	        options[1]="last";  //range of variables to make numeric
	
	        convert.setOptions(options);
	        convert.setInputFormat(data);
	
	        Instances newData=Filter.useFilter(data, convert);
	        
	        String[] options1 = new String[2];
	        options1[0] = "-I";       
	        options1[1] = "500"; 
	        RandomForest rf = new RandomForest();         
	        rf.setOptions(options1);     // set the options
	        
	        for(int perc=100;perc<=130;perc=perc+5) //double spread=1.0;spread<=20.0;spread=spread+3
	        {
	        	/*System.out.println(spread);
	        	SpreadSubsample filter = new SpreadSubsample();
	        	filter.setDistributionSpread(spread);*/

	        	System.out.println(perc);
		        SMOTE filter = new SMOTE(); 
		        filter.setPercentage(perc);
		        
		        FilteredClassifier fc = new FilteredClassifier();
		        fc.setFilter(filter);
		        fc.setClassifier(rf);
		        //rf.buildClassifier(data);   // build classifier
		        Evaluation eval = new Evaluation(newData);
		        eval.crossValidateModel(fc, newData, 10, new Random(1));
		        // print the result
		        /*String strSummary = eval.toSummaryString();
		        System.out.println(strSummary);
		        System.out.println(eval.toClassDetailsString());
		        System.out.println(eval.toMatrixString());
		        
		        System.out.println(eval.areaUnderROC(1));*/
		        System.out.println(eval.areaUnderPRC(1));
	    	
	        }
		}
	}
}
