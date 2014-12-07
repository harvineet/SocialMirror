library(data.table)
library(ggplot2)

tag_files<-list.files(path="G:/socialnetworks_project_log/conductance_std_features_td/cond_ve_features/feature_files", full.names = TRUE)
mainDir<-"G:/socialnetworks_project_log/spectral_clustering/corr_plots/"
feature_name <- c("Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Usage Entropy","Std. of Average rate of change of conductance (last 100)","Std. of Second order derivative of conductance (last 100)","Class")
dat_comb<-data.frame()
totalspread<-fread("G:/socialnetworks_project_log/spectral_clustering/tag_freq.csv")
totalspread$logspread<-log10(totalspread$TotalSpread)
pthresh<-c(1000,1500,2000,250,2500,500)
thr=0
dat_corr<-data.frame()
for (tag in tag_files[1:length(tag_files)])
{
  print(tag)
  thr=thr+1
  corr<-data.frame(Threshold=pthresh[thr])
  df<-fread(tag)
  df<-as.data.frame(df)
  dat <- subset(df, select = c(2:15,17:22,24:28,31,34,48))
  dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
  logspread<-totalspread[totalspread$TagName %in% df$TagName,]$logspread
  for(i in 1:(ncol(dat)-1)) #c(8,14,27,19,23,25,16,10)
  {
    #corr_test<-cor.test(dat[,i], logspread)
    #corr_ci<-corr_test$conf.int
    #corr<-c(corr,corr_test$estimate,corr_test$conf.int)
    #colnames(corr)[i+1]<-feature_name[i]
    
    corr[,i+1]<-cor(dat[,i], logspread)
    #colnames(corr)[i+1]<-feature_name[i]
  }
  dat_corr<-rbind(dat_corr,corr)
}

write.csv(file="G:/socialnetworks_project_log/pred_thresh_change/std/feature_corr.csv",dat_corr,row.names=F)

for(i in 2:(ncol(dat_corr))) #c(8,14,27,19,23,25,16,10) #3:(ncol(dat)-1)
{
  p1<-ggplot(dat_corr, aes_string(x="Threshold", y=paste("V",i,sep=""))) + 
    geom_line() +
    ylab("Correlation coefficient") + xlab("Prediction threshold") + 
    theme_bw(16) + 
    coord_cartesian(ylim = c(-1,1)) +
    ggtitle(feature_name[i-1]) + 
    geom_hline(yintercept=c(0), linetype="dotted")
  #print(p1)
  ggsave(p1,filename=paste(feature_name[i-1],".png",sep=""),path=mainDir, width=8, height=5,dpi=400)
}