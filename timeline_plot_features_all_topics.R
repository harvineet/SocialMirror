ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + stat_summary(fun.y="mean",geom="line") +
  stat_summary(fun.data=mean_se, geom="errorbar", alpha=0.25)
p<-ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + stat_summary(fun.y="mean",geom="line") +
  +     stat_summary(fun.data=mean_se, geom="smooth", alpha=0.25)
ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + 
   geom_smooth(se=FALSE) + 
   stat_summary(fun.data=mean_se, geom="ribbon", alpha=0.25)
ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + stat_summary(fun.y="mean",geom="line") +
   stat_summary(fun.data=mean_se, geom="pointrange", alpha=0.25)

library(data.table)
library(ggplot2)

tag_files<-list.files(path="G:/socialnetworks_project_log/feature_timeline_files", full.names = TRUE)
mainDir<-"G:/socialnetworks_project_log/plots/"
feature_name = c("Number of Tweets", "Hashtag", "Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Number of Tweets before 5hr","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Tweeting Entropy","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Class")
dat_comb_nviral<-data.frame()
dat_comb_viral<-data.frame()
for (tag in tag_files[1:length(tag_files)])
{
  dat<-fread(tag)
  dat<-as.data.frame(dat)
  #dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
  label<-dat[2,ncol(dat)]
  label_name<-colnames(dat)[label]
  colnames(dat)<-paste("col", 1:ncol(dat), sep="")
  if (label == 1) {
    dat_comb_viral<-rbind(dat_comb_viral,dat)
  } else {
    dat_comb_nviral<-rbind(dat_comb_nviral,dat)
  }
}

for(i in c(8,14,27,19,23,25,16,10)) #c(8,14,27,19,23,25,16,10) #3:(ncol(dat)-1)
{
  print(i)
  #feature<-paste("'",colnames(dat)[i],"'",sep="")  
  # Line plot
  p<-ggplot(dat_comb_nviral, aes_string(x="col1", y=paste("col",i,sep=""))) + 
    stat_summary(fun.y="mean",geom="line") + 
    stat_summary(fun.data=mean_se, geom="ribbon", alpha=0.25) +
    ylab("feature value") + xlab("number of tweets") + 
    theme(text = element_text(size=12)) + scale_y_continuous(expand = c(0,5e+08)) + 
    ggtitle(paste("Change in value of\n",feature_name[i])) + xlim(0,10100) +
    geom_vline(xintercept=c(1000,7892), linetype="dotted")
    #geom_rect(data=NULL,aes(xmin=0,xmax=1000,ymin=-Inf,ymax=Inf),fill="#4A6FE3",alpha=0.002) +
    #geom_rect(data=NULL,aes(xmin=1000,xmax=10100,ymin=-Inf,ymax=Inf),fill="#D33F6A",alpha=0.002)
  print(p)
  subDir<-"nonviral"
  if (!file.exists(file.path(mainDir, subDir)))
  {
    dir.create(file.path(mainDir, subDir))
  }
  ggsave(p,filename=paste(feature_name[i],".png",sep=""),path=file.path(mainDir,subDir))
}
for(i in c(8,14,27,19,23,25,16,10)) #c(8,14,27,19,23,25,16,10) #3:(ncol(dat)-1)
{
  print(i)
  #feature<-paste("'",colnames(dat)[i],"'",sep="")  
  # Line plot
  p<-ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + 
    stat_summary(fun.y="mean",geom="line") + 
    stat_summary(fun.data=mean_se, geom="ribbon", alpha=0.25) +
    ylab("feature value") + xlab("number of tweets") + 
    #theme(text = element_text(size=12)) + 
    scale_y_continuous(expand = c(0,5e+08)) + 
    ggtitle(paste("Change in value of\n",feature_name[i])) + xlim(0,10100) +
    geom_vline(xintercept=c(1000), linetype="dotted")
    #geom_rect(data=NULL,aes(xmin=0,xmax=1000,ymin=-Inf,ymax=Inf),fill="#4A6FE3",alpha=0.002) +
    #geom_rect(data=NULL,aes(xmin=1000,xmax=10100,ymin=-Inf,ymax=Inf),fill="#D33F6A",alpha=0.002)
  print(p)
  subDir<-"viral"
  if (!file.exists(file.path(mainDir, subDir)))
  {
    dir.create(file.path(mainDir, subDir))
  }
  ggsave(p,filename=paste(feature_name[i],".png",sep=""),path=file.path(mainDir,subDir))
}

require(gridExtra)

median_se <- function(x, mult = 1) {  
  x <- na.omit(x)
  q25 <- quantile(x, 0.25)
  q75 <- quantile(x, 0.75)
  median <- median(x)
  data.frame(y = median, ymin = q25, ymax = q75)
}

for(i in 3:(ncol(dat)-1)) #c(8,14,27,19,23,25,16,10) #3:(ncol(dat)-1)
{
  print(i)
  p1<-ggplot(dat_comb_nviral, aes_string(x="col1", y=paste("col",i,sep=""))) + 
    stat_summary(fun.y="median",geom="line") + 
    stat_summary(fun.data=median_se, geom="ribbon", alpha=0.25) +
    ylab("feature value") + xlab("number of tweets") + 
    #theme(text = element_text(size=12)) + 
    #scale_y_continuous(limits = c(0,0.6)) +
    coord_cartesian(xlim = c(0,10100), ylim = c(0.94,1)) +
    ggtitle(paste(feature_name[i],"\n(Non-viral)")) + 
    #ylim = c(0,300) +
    geom_vline(xintercept=c(1000,7892), linetype="dotted")
  
  p2<-ggplot(dat_comb_viral, aes_string(x="col1", y=paste("col",i,sep=""))) + 
    stat_summary(fun.y="median",geom="line") + 
    stat_summary(fun.data=median_se, geom="ribbon", alpha=0.25) +
    ylab("feature value") + xlab("number of tweets") + 
    #theme(text = element_text(size=12)) + 
    #scale_y_continuous(limits = c(0,0.6)) +
    coord_cartesian(xlim = c(0,10100), ylim = c(0.94,1)) +
    ggtitle(paste(feature_name[i],"\n(Viral)")) + 
    #ylim(0,300) +
    geom_vline(xintercept=c(1000), linetype="dotted")

  grid.arrange(p1, p2, ncol=2)
  p<-arrangeGrob(p1, p2, ncol=2)
  ggsave(p,filename=paste(feature_name[i],".png",sep=""),path=mainDir, width=8, height=5)
}
i<-20
feature_name[i]
8-(0,300), 14-(-150,0), 27-(0.3,0.4), 19-(0,4000), 23-(10,70), 25-(0,7500), 16-(-5e08,5e08), 10-(0,4500)
8-(0,300), 14-(-60,0), 27-(0,0.6), 19-(0,5000), 23-(0,85), 25-(0,7000), 16-(-25e05,25e05), 16- (-11250,11250), 10-(0,4500)