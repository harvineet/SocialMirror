library(data.table)
library(ggplot2)

#dat<-fread("G:/socialnetworks_project_log/spectral clustering/feature_files/feature_clusters_loc_rbf_10.csv")
dat<-fread("G:/socialnetworks_project_log/histogram_of_counts/feature_word_spread.csv")
dat<-as.data.frame(dat)
dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
label<-ncol(dat)
colnames(dat)[1:(ncol(dat)-1)]<-paste("col", 1:(ncol(dat)-1), sep="")
label_name<-colnames(dat)[label]
#feature_name <- c("Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Usage Entropy","Std. of Average rate of change of conductance (last 100)","Std. of Second order derivative of conductance (last 100)","Cluster number","Size of Cluster","Class")
feature_name <- c("Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Usage Entropy","Std. of Average rate of change of conductance (last 100)","Std. of Second order derivative of conductance (last 100)","Word Spread","Class")
#feature_name <- c("Ratio of Size of Two Largest Components", "Fraction of Self-Initiated","Fraction of Edges Across Geographies","Follower Count of Self-Initiated Adopters","Number of Self-Initiated Adopters","Number of Adopters with Heavy Following","Subgraph Density","Size of largest Connected Component", "Number of Edges in the Network Spread","Average rate of change of conductance (last 25)","Average rate of change of conductance (last 50)","Average rate of change of conductance (last 100)","Average rate of change of conductance (last 200)","Second order derivative of conductance","Growth Rate","Number of Adopters","Absolute value of the cumulative conductance","Ratio of Singletons","Ratio of number of Connected Components to number of adopters","Number of Infected Geographies","Number of Retweets","Number of User Mentions","Fraction of Intra Geography Activity (Retweets)","Fraction of Intra Geography Activity (User Mentions)","Usage Entropy","Std. of Average rate of change of conductance (last 100)","Std. of Second order derivative of conductance (last 100)","Fraction Of Sentiment Flips","Class")

for(i in 2:(ncol(dat)-1))
{
  print(i)
  feature<-feature_name[i]#colnames(dat)[i]
  legend_title="Class label"
  
  # Density plot
  p<-ggplot(dat, aes_string(x=paste("col",i,sep=""), fill=label_name)) + geom_density(alpha=.3) +
    ylab("probability density") + xlab(feature) +
    scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) + theme_bw(base_size = 30) +
    scale_y_continuous(expand = c(0,0)) + ggtitle("Class wise probability distribution")
  print(p)
  ggsave(p,filename=paste(feature,".png",sep=""))
  
  #i=1 #+ coord_cartesian(xlim = c(0, 50000))
  #i=5 #+ coord_cartesian(xlim = c(-50, 10))
  #i=6 #+ coord_cartesian(xlim = c(-5e07, 5e07)) #scale_y_continuous(limits = c(-5000, 5000))
  #i=12 #+ coord_cartesian(xlim = c(-200, 200)) #i<-17 #i<-7 #i<-22
  
  # Box plot
  #p<-ggplot(dat,aes_string(y=feature,x=label_name, fill=label_name)) + geom_boxplot() + ylab(feature) + scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) + theme_bw(16) + scale_y_continuous(expand = c(0,0)) + ggtitle(paste("Class wise box plot for the feature: ",feature,"",sep=""))
  #print(p)
  #ggsave(p,filename=paste("boxplot_",i,".png",sep=""))
  # Interleaved histograms
  #p<-ggplot(dat, aes_string(x=feature, fill=label_name)) + geom_histogram(position="dodge") + ylab("frequency") + xlab(feature_name[i]) + scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) + theme_bw(16) + scale_y_continuous(expand = c(0,0)) + ggtitle(paste("Class wise histogram of feature: ",feature_name[i],"",sep=""))
  #ggsave(p,filename=paste("histogram_",feature_name[i],".png",sep=""))
  
  # Density plot with all data points
  #p<-ggplot(dat, aes_string(x=feature)) + geom_density() + geom_density(alpha=.3,aes_string(fill=label_name)) + ylab("probability") + xlab(feature_name[i]) + scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) + theme_bw(16) + scale_y_continuous(expand = c(0,0)) + ggtitle(paste("Class wise histogram for the feature: ",feature_name[i],"",sep=""))
  #print(p)
  
  # Histogram overlaid with kernel density curve
  #ggplot(dat, aes_string(x=feature, fill=label_name)) + geom_histogram(position="dodge",aes(y=..density..)) + geom_density(alpha=.2, fill="#FF6666")  # Overlay with transparent density plot
}

dat<-fread("G:/socialnetworks_project_log/spectral_clustering/histogram_input.csv")
dat<-as.data.frame(dat)
dat[,ncol(dat)]<-as.factor(dat[,ncol(dat)])
feature_name<-colnames(dat)
label<-ncol(dat)
label_name<-feature_name[label]
i<-4
feature<-feature_name[i]

# Interleaved histograms
p<-ggplot(dat, aes_string(x=feature, fill=label_name)) +
  geom_histogram(aes(y=5*..density..),position='dodge',binwidth=5) +
  ylab("proportion of hashtags") + xlab(feature_name[i]) +
  scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) +
  theme_bw(20) + scale_y_continuous(expand = c(0,0)) +
  ggtitle("Class wise histogram of Number of Locations in Cluster")
  #ggtitle("Class wise histogram of Number of Infected Clusters")

# Histogram overlaid with kernel density curve
ggplot(dat, aes_string(x=feature, fill=label_name)) + geom_histogram(position="dodge",aes(y=..density..))
+ geom_density(alpha=.2, fill="#FF6666")  # Overlay with transparent density plot

print(p)
ggsave(p,filename=paste("histogram_",feature_name[i],".png",sep=""))