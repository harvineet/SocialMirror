library(data.table)
library(ggplot2)
library(plyr)
library(reshape2)

tag_files<-list.files(path="G:/socialnetworks_project_log/conductance_std_features_td/cond_ve_features/feature_files", full.names = TRUE)
mainDir<-"G:/socialnetworks_project_log/spectral_clustering/"
feature_name <- c("RatioSecondtoFirst", "RatioSelfInitComm","RatioCrossGeoEdges","SelfInitAdoptersFollowers","SelfInitAdopters","HeavyUsers","Density","LargestSize", "NumOfEdges","Conduct'_20","Conduct'_50","Conduct'_100","Conduct'_250","Conduct''","TimeTakenToPredThr","NumOfAdopters","CummConductance","RatioOfSingletons","RatioOfConnectedComponents","InfectedGeo","NumOfRT","NumOfMention","IntraGeoRT","IntraGeoMention","TweetingEntropy","Conduct'_stdev","Conduct''_stdev","Class")
dat_comb<-data.frame()
totalspread<-fread("G:/socialnetworks_project_log/spectral_clustering/tag_freq_5000.csv")
totalspread$logspread<-log10(totalspread$count)
pthresh<-c(100,1000,150,1500,200,2000,250,2500,3000,3500,4000,4500,50,500,5000)
thr=0
dat_corr<-data.frame()
dat_corr_low<-data.frame()
dat_corr_high<-data.frame()
for (tag in tag_files[1:length(tag_files)])
{
  print(tag)
  thr=thr+1
  corr<-data.frame(Threshold=pthresh[thr])
  corr_low<-data.frame(Threshold=pthresh[thr])
  corr_high<-data.frame(Threshold=pthresh[thr])
  df<-fread(tag)
  df<-as.data.frame(df)
  
  df<-df[df$TagName %in% totalspread$tag,]
  
  dat <- subset(df, select = c(2:15,17:22,24:28,31,34,48))
  dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
  logspread<-totalspread[totalspread$tag %in% df$TagName,]$logspread
  nsamp<-nrow(dat)
  for(i in 1:(ncol(dat)-1)) #c(8,14,27,19,23,25,16,10)
  {
    corr_test<-cor.test(dat[,i], logspread, method = c("spearman"))
    #corr_test<-cor.test(dat[,i], logspread)
    #corr_ci<-corr_test$conf.int
    #corr_low[,i+1]<-corr_ci[1]
    #corr_high[,i+1]<-corr_ci[2]
       
    corr_low[,i+1]<-tanh(atanh(corr_test$estimate)-1.03/(nsamp-3)^(1/2))
    corr_high[,i+1]<-tanh(atanh(corr_test$estimate)+1.03/(nsamp-3)^(1/2))

    colnames(corr_low)[i+1]<-feature_name[i]
    colnames(corr_high)[i+1]<-feature_name[i]
    corr[,i+1]<-corr_test$estimate
    
    #corr[,i+1]<-cor(dat[,i], logspread)
    colnames(corr)[i+1]<-feature_name[i]
  }
  dat_corr<-rbind(dat_corr,corr)
  dat_corr_low<-rbind(dat_corr_low,corr_low)
  dat_corr_high<-rbind(dat_corr_high,corr_high)
}
#dat_corr<-dat_corr[which(dat_corr$Threshold %in% c(1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000)),]
#dat_corr_low<-dat_corr_low[which(dat_corr_low$Threshold %in% c(1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000)),]
#dat_corr_high<-dat_corr_high[which(dat_corr_high$Threshold %in% c(1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000)),]

dat_ci<-merge(melt(dat_corr_low, id.vars = "Threshold", value.name="low"),
              melt(dat_corr_high, id.vars = "Threshold", value.name="high"),
              by=c("Threshold","variable"), all = TRUE)
dat<-merge(melt(dat_corr, id.vars = "Threshold", value.name="Correlation"),
           dat_ci, by=c("Threshold","variable"), all = TRUE)
colnames(dat)[3:5]<-c("Correlation","low","high")

#write.csv(file="G:/socialnetworks_project_log/pred_thresh_change/std/feature_corr.csv",dat_corr,row.names=F)

dat_plot<-dat[which(dat$variable %in% feature_name[c(15,16,21,22)]),]
p1<-ggplot(dat_plot, aes_string(x="Threshold", y="Correlation")) + 
  geom_line(colour="red",size=1) + geom_point(colour="red")+
  geom_errorbar(aes(ymin=low, ymax=high)) +
  ylab("Correlation coefficient") + xlab("Prediction threshold") + 
  theme_bw(16) + 
  theme(text = element_text(size=32)) +
  scale_x_continuous(expand = c(0,0)) +
  #ggtitle(feature_name[i-1]) + 
  geom_hline(yintercept=c(0), linetype="dotted") + 
  facet_wrap( ~ variable) #+ ggtitle("Correlation plots for Evolution features")
print(p1)

#ggsave(p1,filename="E_corr.png",path=mainDir, width=23, height=13,dpi=400)

dat_plot<-dat[which(dat$variable %in% feature_name[c(2,3,20,23,24,25)]),]
p1<-ggplot(dat_plot, aes_string(x="Threshold", y="Correlation")) + 
  geom_line(colour="green",size=1) + geom_point(colour="green")+
  geom_errorbar(aes(ymin=low, ymax=high)) +
  ylab("Correlation coefficient") + xlab("Prediction threshold") + 
  theme_bw(16) + 
  theme(text = element_text(size=32)) +
  scale_x_continuous(expand = c(0,0)) +
  #ggtitle(feature_name[i-1]) + 
  geom_hline(yintercept=c(0), linetype="dotted") + 
  facet_wrap( ~ variable) #+ ggtitle("Correlation plots for Geography features")
print(p1)

#ggsave(p1,filename="G_corr.png",path=mainDir, width=19, height=11,dpi=400)

dat_plot<-dat[which(dat$variable %in% feature_name[c(1,4,5,6,7,8,9,19,18)]),]
p1<-ggplot(dat_plot, aes_string(x="Threshold", y="Correlation")) + 
  geom_line(colour="magenta",size=1) +geom_point(colour="magenta")+
  geom_errorbar(aes(ymin=low, ymax=high)) +
  ylab("Correlation coefficient") + xlab("Prediction threshold") + 
  theme_bw(16) + 
  theme(text = element_text(size=32)) +
  scale_x_continuous(expand = c(0,0)) +
  #ggtitle(feature_name[i-1]) + 
  geom_hline(yintercept=c(0), linetype="dotted") + 
  facet_wrap( ~ variable) #+ ggtitle("Correlation plots for Network features")
print(p1)

#ggsave(p1,filename="N_corr.png",path=mainDir, width=19, height=11,dpi=400)

dat_plot<-dat[which(dat$variable %in% feature_name[c(10,11,12,13,14,17,26,27)]),]
p1<-ggplot(dat_plot, aes_string(x="Threshold", y="Correlation")) + 
  geom_line(colour="blue",size=1) +geom_point(colour="blue")+
  geom_errorbar(aes(ymin=low, ymax=high)) +
  ylab("Correlation coefficient") + xlab("Prediction threshold") + 
  theme_bw(16) + 
  theme(text = element_text(size=32)) +
  scale_x_continuous(expand = c(0,0)) +
  #ggtitle(feature_name[i-1]) + 
  geom_hline(yintercept=c(0), linetype="dotted") + 
  facet_wrap( ~ variable) 
  #ggtitle("Correlation plots for Conductance features")
print(p1)

#ggsave(p1,filename="C_corr.png",path=mainDir, width=19, height=11,dpi=400)


