import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
 
import java.io.File;
 
public class RemoveAttr {
  /**
   * takes an ARFF file as first argument, the number of indices to remove
   * as second and thirdly whether to invert or not (true/false).
   * Dumps the generated data to stdout.
   */
  public static void main(String[] args) throws Exception {
	  if (args.length != 4) {
	      System.out.println("\nUsage: CSV2Arff <input.csv> <output.arff> <indices> <invert>\n");
	      System.exit(1);
	    }
	  	// load CSV
	    CSVLoader loader = new CSVLoader();
	    loader.setSource(new File(args[0]));
	    Instances inst = loader.getDataSet();
	    
	    // remove indices
		Instances instNew;
		Remove remove;
		remove = new Remove();
		remove.setAttributeIndices(args[2]);
		remove.setInvertSelection(new Boolean(args[3]).booleanValue());
		remove.setInputFormat(inst);
		instNew = Filter.useFilter(inst, remove);
		
		// save ARFF
	    ArffSaver saver = new ArffSaver();
	    saver.setInstances(instNew);
	    saver.setFile(new File(args[1]));
	    //saver.setDestination(new File(args[1]));
	    saver.writeBatch();
  }
}