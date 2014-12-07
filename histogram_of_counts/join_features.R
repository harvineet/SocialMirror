library(data.table)

dat<-fread("G:/socialnetworks_project_log/histogram_of_counts/feature_files/feature_exp_cond.csv")
#seg<-fread("G:/socialnetworks_project_log/histogram_of_counts/tag_clusters/tag_clusters_1000_20.csv")
#seg<-fread("G:/socialnetworks_project_log/histogram_of_counts/tag_spread.csv")

seg<-fread("G:/socialnetworks_project_log/spectral_clustering/tag_clusters_loc_rbf_10.csv")

#hist<-fread("G:/socialnetworks_project_log/histogram_of_counts/tag_clusters/tag_histograms_1000(1).csv")

#check
all(dat$TagName==seg$TagName)
#all(dat$TagName==hist$TagName)

df <- cbind(subset(dat, select = c(2:10,48:52,17,18,53,20:22,24:28,55,58)),subset(seg, select = c(3:ncol(seg))),subset(dat, select = c(60)))

#train<- df[df$TrainExample==1,]
#test<- df[df$TrainExample==0,]
#train$TrainExample<-NULL
#test$TrainExample<-NULL

#write.csv(file="G:/socialnetworks_project_log/spectral_clustering/feature_clusters_loc_rbf_10.csv",train,row.names=F)
#write.csv(file="G:/socialnetworks_project_log/spectral_clustering/test.csv",test,row.names=F)

#df_hist <- cbind(subset(dat, select = c(2:10,48:52,17,18,53,20:22,24:28,55,58)),subset(hist, select = c(2:ncol(hist))),subset(dat, select = c(60)))

#write.csv(file="G:/socialnetworks_project_log/histogram_of_counts/feature_clust_1000_20.csv",df,row.names=F)
#write.csv(file="G:/socialnetworks_project_log/histogram_of_counts/feature_hist_1000(1).csv",df_hist,row.names=F)

write.csv(file="G:/socialnetworks_project_log/spectral_clustering/feature_clusters_loc_rbf_10.csv",df,row.names=F)
#write.csv(file="G:/socialnetworks_project_log/histogram_of_counts/feature_word_spread.csv",df,row.names=F)
