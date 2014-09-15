java weka.filters.supervised.instance.StratifiedRemoveFolds -i feature_name.arff -o test/train1.arff -c last -N 2 -F 1 -V
java weka.filters.supervised.instance.StratifiedRemoveFolds -i feature_name.arff -o test/test1.arff -c last -N 2 -F 1
java weka.filters.supervised.instance.StratifiedRemoveFolds -i feature_name.arff -o test/train2.arff -c last -N 2 -F 2 -V
java weka.filters.supervised.instance.StratifiedRemoveFolds -i feature_name.arff -o test/test2.arff -c last -N 2 -F 2

java weka.classifiers.Evaluation weka.classifiers.trees.RandomForest -t test/train1.arff -T test/test1.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -v -o > result.txt
java weka.classifiers.Evaluation weka.classifiers.trees.RandomForest -t test/train2.arff -T test/test2.arff -I 500 -K 0 -S 1 -num-slots 1 -no-cv -v -o >>result.txt
pause