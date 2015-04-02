make

CORPUS=pi/pi-billion_spaces.txt
SAVE_FILE=pi/vectors.txt
VOCAB_FILE=pi/vocab.txt

time ./word2vec -train $CORPUS -output $SAVE_FILE -cbow 0 -size 300 -window 5  -hs 1 -sample 1 -min-count 2 -threads 10 -binary 0 -iter 15 -save-vocab $VOCAB_FILE
