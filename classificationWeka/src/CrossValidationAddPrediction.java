import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.converters.ConverterUtils.DataSink;
import weka.core.Utils;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.filters.Filter;
import weka.filters.supervised.attribute.AddClassification;
import weka.filters.unsupervised.attribute.NumericToNominal;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Random;

/**
 * Performs a single run of cross-validation and adds the prediction on the 
 * test set to the dataset.
 *
 * Command-line parameters:
 * <ul>
 *    <li>-t filename - the dataset to use</li>
 *    <li>-o filename - the output file to store dataset with the predictions
 *    in</li>
 *    <li>-x int - the number of folds to use</li>
 *    <li>-s int - the seed for the random number generator</li>
 *    <li>-c int - the class index, "first" and "last" are accepted as well;
 *    "last" is used by default</li>
 *    <li>-W classifier - classname and options, enclosed by double quotes; 
 *    the classifier to cross-validate</li>
 * </ul>
 *
 * Example command-line:
 * <pre>
 * java CrossValidationAddPrediction -t anneal.arff -c last -o predictions.arff -x 10 -s 1 -W "weka.classifiers.trees.J48 -C 0.25"
 * </pre>
 *
 * @author FracPete (fracpete at waikato dot ac dot nz)
 */
public class CrossValidationAddPrediction {

  /**
   * Performs the cross-validation. See Javadoc of class for information
   * on command-line parameters.
   *
   * @param args        the command-line parameters
   * @throws Excecption if something goes wrong
   */
  public static void CrossValidationPrediction(String[] args) throws Exception {
    // loads data and set class index
    Instances data = DataSource.read(Utils.getOption("t", args));
    String clsIndex = Utils.getOption("c", args);
    if (clsIndex.length() == 0)
      clsIndex = "last";
    if (clsIndex.equals("first"))
      data.setClassIndex(0);
    else if (clsIndex.equals("last"))
      data.setClassIndex(data.numAttributes() - 1);
    else
      data.setClassIndex(Integer.parseInt(clsIndex) - 1);

    // classifier
    String[] tmpOptions;
    String classname;
    tmpOptions     = Utils.splitOptions(Utils.getOption("W", args));
    classname      = tmpOptions[0];
    tmpOptions[0]  = "";
    Classifier cls = (Classifier) Utils.forName(Classifier.class, classname, tmpOptions);

    // other options
    int seed  = Integer.parseInt(Utils.getOption("s", args));
    int folds = Integer.parseInt(Utils.getOption("x", args));

    // randomize data
    Random rand = new Random(seed);
    Instances randData = new Instances(data);
    randData.randomize(rand);
    if (randData.classAttribute().isNominal())
      randData.stratify(folds);

    // perform cross-validation and add predictions
    Instances predictedData = null;
    Evaluation eval = new Evaluation(randData);
    for (int n = 0; n < folds; n++) {
      Instances train = randData.trainCV(folds, n);
      Instances test = randData.testCV(folds, n);
      // the above code is used by the StratifiedRemoveFolds filter, the
      // code below by the Explorer/Experimenter:
      // Instances train = randData.trainCV(folds, n, rand);

      // build and evaluate classifier
      Classifier clsCopy = Classifier.makeCopy(cls);
      clsCopy.buildClassifier(train);
      eval.evaluateModel(clsCopy, test);

      // add predictions
      AddClassification filter = new AddClassification();
      filter.setClassifier(cls);
      filter.setOutputClassification(true);
      filter.setOutputDistribution(true);
      filter.setOutputErrorFlag(true);
      filter.setInputFormat(train);
      Filter.useFilter(train, filter);  // trains the classifier
      Instances pred = Filter.useFilter(test, filter);  // perform predictions on test set
      if (predictedData == null)
        predictedData = new Instances(pred, 0);
      for (int j = 0; j < pred.numInstances(); j++)
        predictedData.add(pred.instance(j));
    }

    // output evaluation
    System.out.println();
    System.out.println("=== Setup ===");
    System.out.println("Classifier: " + cls.getClass().getName() + " " + Utils.joinOptions(cls.getOptions()));
    System.out.println("Dataset: " + data.relationName());
    System.out.println("Folds: " + folds);
    System.out.println("Seed: " + seed);
    System.out.println();
    System.out.println(eval.toSummaryString("=== " + folds + "-fold Cross-validation ===", false));

    // output "enriched" dataset
    DataSink.write(Utils.getOption("o", args), predictedData);
  }
  public static void main(String[] args) throws Exception{
		File dir = new File("data/arff");
		File[] directoryListing = dir.listFiles();
		for (File child : directoryListing) {
			System.out.println(child);
			BufferedReader reader = new BufferedReader(
	                new FileReader(child));
			Instances data = new Instances(reader);	
			reader.close();
			// setting class attribute
			data.setClassIndex(data.numAttributes() - 1);
			// setting class attribute from numeric to nominal
			NumericToNominal convert= new NumericToNominal();
			String[] opts = {child.getPath(),arffFile.getPath(),"17,18,24,25,34","true"};
			CrossValidationPrediction(opts);
			
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
	        //rf.buildClassifier(data);   // build classifier
	        Evaluation eval = new Evaluation(newData);
	        eval.crossValidateModel(rf, newData, 10, new Random(1));
	        // print the result
	        String strSummary = eval.toSummaryString();
	        /*System.out.println(strSummary);
	        System.out.println(eval.toClassDetailsString());
	        System.out.println(eval.toMatrixString());
	        
	        System.out.println(eval.areaUnderROC(1));*/
	        System.out.println(eval.areaUnderPRC(1));
		}
	}
}
