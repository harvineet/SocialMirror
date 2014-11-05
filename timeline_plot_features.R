library(data.table)
library(ggplot2)

tag_files<-list.files(path="G:/socialnetworks_project_log/feature_timeline_files", full.names = TRUE)
mainDir<-"G:/socialnetworks_project_log/plots"
feature_name = c("Number of Tweets", "Hashtag", "Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Number of Tweets before 5hr","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Tweeting Entropy","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Class")
for (tag in tag_files[1:length(tag_files)])
{
  dat<-fread(tag)
  dat<-as.data.frame(dat)
  dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
  label<-ncol(dat)
  label_name<-colnames(dat)[label]
  hashtag_name<-dat[2,2]
  colnames(dat)<-paste("col", 1:ncol(dat), sep="")
  for(i in 3:(ncol(dat)-1)) #c(8,14,27,19,23,25,16,10)
  {
    print(i)
    #feature<-paste("'",colnames(dat)[i],"'",sep="")  
    # Line plot
    p<-ggplot(dat, aes_string(x="col1", y=paste("col",i,sep=""))) + geom_line() + ylab("feature value") + xlab("number of tweets") + 
      theme(text = element_text(size=12)) + scale_y_continuous(expand = c(0,0)) + 
      ggtitle(paste("Change in value of\n",feature_name[i],"\n#",hashtag_name)) + xlim(0,10100) +
      geom_rect(data=NULL,aes(xmin=0,xmax=1000,ymin=-Inf,ymax=Inf),fill="#4A6FE3",alpha=0.002)+
      geom_rect(data=NULL,aes(xmin=1000,xmax=10100,ymin=-Inf,ymax=Inf),fill="#D33F6A",alpha=0.002)
    print(p)
    subDir<-hashtag_name
    if (!file.exists(file.path(mainDir, subDir)))
    {
      dir.create(file.path(mainDir, subDir))
    }
    ggsave(p,filename=paste(feature_name[i],"_",hashtag_name,".png",sep=""),path=file.path(mainDir, subDir))
  }
}