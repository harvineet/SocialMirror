library(data.table)
dat<-fread("G:/socialnetworks_project_log/pred_thresh_change/std/misclassified_examples_plot/TwitDat_ENGC.csv")
dat<-as.data.frame(dat)
dat$Class<-as.factor(dat$Class)
  
library(ggplot2)
ggplot(dat, aes_string(x="count", y="probPositiveClass")) +
  geom_point(aes(color = Class))+
  scale_colour_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) +
  ggtitle("Eventual spread of mis-classified examples") + 
  geom_hline(yintercept=c(0.364), linetype="dotted") +
  geom_vline(xintercept=c(10000), linetype="dotted") +
  scale_y_continuous(expand = c(0,0)) +
  scale_x_log10()+
  #coord_cartesian(xlim = c(0, 100000)) +
  xlab("Number of tweets") + ylab("Probability of Viral Class") + theme_bw(16)