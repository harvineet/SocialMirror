library(data.table)

dat<-fread("G:/socialnetworks_project_log/conductance_std_features_td/cond_ve_features/feature_files/feature_1500.csv")

df <- cbind(subset(dat, select = c(2:15,17:22,24:28,31,34,48)))

write.csv(file="G:/socialnetworks_project_log/conductance_std_features_td/cond_ve_features/feature_files/filtered_columns/feature_1500.csv",df,row.names=F)
#y<-round(x, digits = 5)