import java.io.File;

import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

public class createArff {
	public static void RemoveAttr(String[] args) throws Exception {
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
	public static void main(String[] args) throws Exception {
		File dir = new File("data/csv");
		File[] directoryListing = dir.listFiles();
		for (File child : directoryListing) {
			System.out.println(child);
			String csvFileNameRel = child.getName();
			csvFileNameRel = csvFileNameRel.replace(".csv",".arff");
			
			//All features (no removal)
			File arffFile = new File("data/arff", csvFileNameRel);
			System.out.println(arffFile);
			String[] options = {child.getPath(),arffFile.getPath(),"","false"};
			RemoveAttr(options);
			
			/*
			//feature combinations for 28 features (with std)
			// e
			File arffFile = new File("data/arff", "e_"+csvFileNameRel);
			System.out.println(arffFile);
			String[] options = {child.getPath(),arffFile.getPath(),"15,16,21,22,28","true"};
			RemoveAttr(options);
			// en
			File arffFile1 = new File("data/arff", "en_"+csvFileNameRel);
			System.out.println(arffFile1);
			String[] options1 = {child.getPath(),arffFile1.getPath(),"20,2,3,25,23,24,10,11,12,13,14,17,26,27","false"};
			RemoveAttr(options1);
			// enc
			File arffFile2 = new File("data/arff", "enc_"+csvFileNameRel);
			System.out.println(arffFile2);
			String[] options2 = {child.getPath(),arffFile2.getPath(),"20,2,3,25,23,24","false"};
			RemoveAttr(options2);
			// engc
			File arffFile3 = new File("data/arff", "engc_"+csvFileNameRel);
			System.out.println(arffFile3);
			String[] options3 = {child.getPath(),arffFile3.getPath(),"","false"};
			RemoveAttr(options3);
			//e1
			File arffFile4 = new File("data/arff", "e1_"+csvFileNameRel);
			System.out.println(arffFile4);
			String[] options4 = {child.getPath(),arffFile4.getPath(),"15,16,28","true"};
			RemoveAttr(options4);
			//egc
			File arffFile5 = new File("data/arff", "egc_"+csvFileNameRel);
			System.out.println(arffFile5);
			String[] options5 = {child.getPath(),arffFile5.getPath(),"6,9,7,5,8,1,19,18,4","false"};
			RemoveAttr(options5);
			//eng
			File arffFile6 = new File("data/arff", "eng_"+csvFileNameRel);
			System.out.println(arffFile6);
			String[] options6 = {child.getPath(),arffFile6.getPath(),"10,11,12,13,14,17,26,27","false"};
			RemoveAttr(options6);
			//ec
			File arffFile7 = new File("data/arff", "ec_"+csvFileNameRel);
			System.out.println(arffFile7);
			String[] options7 = {child.getPath(),arffFile7.getPath(),"20,2,3,25,23,24,6,9,7,5,8,1,19,18,4","false"};
			RemoveAttr(options7);
			//eg
			File arffFile8 = new File("data/arff", "eg_"+csvFileNameRel);
			System.out.println(arffFile8);
			String[] options8 = {child.getPath(),arffFile8.getPath(),"6,9,7,5,8,1,19,18,4,10,11,12,13,14,17,26,27","false"};
			RemoveAttr(options8);
			*/
			/*
			//feature combinations for 32 features (with std)
			// e
			File arffFile = new File("data/arff", "e_"+csvFileNameRel);
			System.out.println(arffFile);
			String[] options = {child.getPath(),arffFile.getPath(),"17,18,24,25,34","true"};
			RemoveAttr(options);
			// en
			File arffFile1 = new File("data/arff", "en_"+csvFileNameRel);
			System.out.println(arffFile1);
			String[] options1 = {child.getPath(),arffFile1.getPath(),"1,16,22,3,4,23,26,27,11,12,13,14,15,19,28,29,30,31,32,33","false"};
			RemoveAttr(options1);
			// enc
			File arffFile2 = new File("data/arff", "enc_"+csvFileNameRel);
			System.out.println(arffFile2);
			String[] options2 = {child.getPath(),arffFile2.getPath(),"1,16,22,3,4,23,26,27","false"};
			RemoveAttr(options2);
			// engc
			File arffFile3 = new File("data/arff", "engc_"+csvFileNameRel);
			System.out.println(arffFile3);
			String[] options3 = {child.getPath(),arffFile3.getPath(),"1,16","false"};
			RemoveAttr(options3);
			//e1
			File arffFile4 = new File("data/arff", "e1_"+csvFileNameRel);
			System.out.println(arffFile4);
			String[] options4 = {child.getPath(),arffFile4.getPath(),"17,18,34","true"};
			RemoveAttr(options4);
			//egc
			File arffFile5 = new File("data/arff", "egc_"+csvFileNameRel);
			System.out.println(arffFile5);
			String[] options5 = {child.getPath(),arffFile5.getPath(),"1,16,7,10,8,6,5,9,2,20,21","false"};
			RemoveAttr(options5);
			//eng
			File arffFile6 = new File("data/arff", "eng_"+csvFileNameRel);
			System.out.println(arffFile6);
			String[] options6 = {child.getPath(),arffFile6.getPath(),"1,16,11,12,13,14,15,19,28,29,30,31,32,33","false"};
			RemoveAttr(options6);
			//ec
			File arffFile7 = new File("data/arff", "ec_"+csvFileNameRel);
			System.out.println(arffFile7);
			String[] options7 = {child.getPath(),arffFile7.getPath(),"1,16,7,10,8,6,5,9,2,20,21,22,3,4,23,26,27","false"};
			RemoveAttr(options7);
			//eg
			File arffFile8 = new File("data/arff", "eg_"+csvFileNameRel);
			System.out.println(arffFile8);
			String[] options8 = {child.getPath(),arffFile8.getPath(),"1,16,11,12,13,14,15,19,7,10,8,6,5,9,2,20,21,28,29,30,31,32,33","false"};
			RemoveAttr(options8);			
			*/
			
			/*
			// feature combinations for 26 features (without std)
			// e
			File arffFile = new File("data/arff", "e_"+csvFileNameRel);
			System.out.println(arffFile);
			String[] options = {child.getPath(),arffFile.getPath(),"17,18,24,25,28","true"};
			RemoveAttr(options);
			// en
			File arffFile1 = new File("data/arff", "en_"+csvFileNameRel);
			System.out.println(arffFile1);
			String[] options1 = {child.getPath(),arffFile1.getPath(),"1,16,22,3,4,23,26,27,11,12,13,14,15,19","false"};
			RemoveAttr(options1);
			// enc
			File arffFile2 = new File("data/arff", "enc_"+csvFileNameRel);
			System.out.println(arffFile2);
			String[] options2 = {child.getPath(),arffFile2.getPath(),"1,16,22,3,4,23,26,27","false"};
			RemoveAttr(options2);
			// engc
			File arffFile3 = new File("data/arff", "engc_"+csvFileNameRel);
			System.out.println(arffFile3);
			String[] options3 = {child.getPath(),arffFile3.getPath(),"1,16","false"};
			RemoveAttr(options3);
			//e1
			File arffFile4 = new File("data/arff", "e1_"+csvFileNameRel);
			System.out.println(arffFile4);
			String[] options4 = {child.getPath(),arffFile4.getPath(),"17,18,28","true"};
			RemoveAttr(options4);
			//egc
			File arffFile5 = new File("data/arff", "egc_"+csvFileNameRel);
			System.out.println(arffFile5);
			String[] options5 = {child.getPath(),arffFile5.getPath(),"1,16,7,10,8,6,5,9,2,20,21","false"};
			RemoveAttr(options5);
			//eng
			File arffFile6 = new File("data/arff", "eng_"+csvFileNameRel);
			System.out.println(arffFile6);
			String[] options6 = {child.getPath(),arffFile6.getPath(),"1,16,11,12,13,14,15,19","false"};
			RemoveAttr(options6);
			//ec
			File arffFile7 = new File("data/arff", "ec_"+csvFileNameRel);
			System.out.println(arffFile7);
			String[] options7 = {child.getPath(),arffFile7.getPath(),"1,16,7,10,8,6,5,9,2,20,21,22,3,4,23,26,27","false"};
			RemoveAttr(options7);
			//eg
			File arffFile8 = new File("data/arff", "eg_"+csvFileNameRel);
			System.out.println(arffFile8);
			String[] options8 = {child.getPath(),arffFile8.getPath(),"1,16,11,12,13,14,15,19,7,10,8,6,5,9,2,20,21","false"};
			RemoveAttr(options8);
			*/
			
			/*
			//removing conductance derivative features
			File arffFile = new File("data/arff", "c1_"+csvFileNameRel);
			System.out.println(arffFile);
			String[] options = {child.getPath(),arffFile.getPath(),"1,16,13,19","false"};
			RemoveAttr(options);
			File arffFile1 = new File("data/arff", "c2_"+csvFileNameRel);
			System.out.println(arffFile1);
			String[] options1 = {child.getPath(),arffFile1.getPath(),"1,16,13,11","false"};
			RemoveAttr(options1);
			File arffFile3 = new File("data/arff", "c3_"+csvFileNameRel);
			System.out.println(arffFile3);
			String[] options3 = {child.getPath(),arffFile3.getPath(),"1,16,11,15,19","false"};
			RemoveAttr(options3);
			File arffFile4 = new File("data/arff", "c4_"+csvFileNameRel);
			System.out.println(arffFile4);
			String[] options4 = {child.getPath(),arffFile4.getPath(),"1,16,11,19","false"};
			RemoveAttr(options4);
			File arffFile5 = new File("data/arff", "c5_"+csvFileNameRel);
			System.out.println(arffFile5);
			String[] options5 = {child.getPath(),arffFile5.getPath(),"1,16,11,15","false"};
			RemoveAttr(options5);
			File arffFile6 = new File("data/arff", "c6_"+csvFileNameRel);
			System.out.println(arffFile6);
			String[] options6 = {child.getPath(),arffFile6.getPath(),"1,16,15,19","false"};
			RemoveAttr(options6);
			*/
			
			/*
			// removing ratiofirsttosecond feature also with tagname and numtweets
			File arffFile3 = new File("data/arff", csvFileNameRel);
			System.out.println(arffFile3);
			String[] options3 = {child.getPath(),arffFile3.getPath(),"1,2,16","false"};
			RemoveAttr(options3);
			*/
		}
	}
}
