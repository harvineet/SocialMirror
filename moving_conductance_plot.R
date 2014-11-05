library(data.table)
library(ggplot2)
require(gridExtra)

tag_files<-list.files(path="G:/socialnetworks_project_log/conductance_plot/disjoint", full.names = TRUE)
mainDir<-"G:/socialnetworks_project_log/plots/moving_conductance/tweet_wise/disjoint"
feature_name <- c("Number of Tweets", "Hashtag","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Absolute value of the cumulative conductance","Time from topic start","Absolute time","Number of Adopters in the topic graph","Total number of Adopters","Class")
labels <- c("(Non-viral)","(viral)")
#cond_nviral<-data.frame()
#cond_viral<-data.frame()

#i<-2
#tag<-tag_files[i]
for (tag in tag_files[1:length(tag_files)])
{
  dat<-fread(tag)
  dat<-as.data.frame(dat)
  #dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
  label<-dat[2,ncol(dat)]
  label_name<-colnames(dat)[label]
  hashtag_name<-dat[2,2]
  class_label<-labels[label+1]
  colnames(dat)<-paste("col", 1:ncol(dat), sep="")
  #date<-lapply(dat$col10, FUN=function(val) strftime(as.POSIXct(val, origin="1970-01-01", tz = "GMT"),"%d %b %Y %H:%M:%S"))
  
  p1<-ggplot(dat, aes_string(x="col1", y=paste("col",8,sep=""))) + geom_line() + 
    ylab("conductance") + xlab("tweets") + 
    #coord_cartesian(ylim = c(0.94,1)) +
    ggtitle(paste(feature_name[8],"\n",hashtag_name,class_label)) +
    scale_x_continuous(expand = c(0,0)) + scale_y_continuous(expand = c(0,0))
    #geom_vline(xintercept=c(1000,10000), linetype="dotted")
  
  p2<-ggplot(dat, aes_string(x="col1", y=paste("col",12,sep=""))) +  geom_line() + 
    ylab("number of adopters") + xlab("tweets") + 
    #coord_cartesian(ylim = c(0.94,1)) +
    ggtitle(paste(feature_name[12],"\n",hashtag_name,class_label)) + 
    scale_x_continuous(expand = c(0,0)) + scale_y_continuous(expand = c(0,0))
    #geom_vline(xintercept=c(1000,10000), linetype="dotted")
  
  #grid.arrange(p1, p2, ncol=2)
  #p<-arrangeGrob(p1, p2, ncol=2)
  ggsave(p1,filename=paste(hashtag_name,".png",sep=""),path=mainDir, width=8, height=5)
}