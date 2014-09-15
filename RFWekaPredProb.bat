java weka.classifiers.trees.RandomForest -t data/train1_oversample.arff -T data/test1.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 > predProb.txt
java weka.classifiers.trees.RandomForest -t data/train2_oversample.arff -T data/test2.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train3_oversample.arff -T data/test3.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train4_oversample.arff -T data/test4.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train5_oversample.arff -T data/test5.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train6_oversample.arff -T data/test6.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train7_oversample.arff -T data/test7.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train8_oversample.arff -T data/test8.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train9_oversample.arff -T data/test9.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
java weka.classifiers.trees.RandomForest -t data/train10_oversample.arff -T data/test10.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -p 0 >> predProb.txt
pause

rem java weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W 0.0 -t input.arff -classifications \"weka.classifiers.evaluation.output.prediction.CSV -suppress -p 1,2 -distribution -file predictions.arff\" -no-cv