for i in *
    do                 # Line breaks are important
        if [ -d $i ]   # Spaces are important
            then
		echo $i
                cp $i/* ../TweetExtracts
                rm -r $i
        fi
    done
