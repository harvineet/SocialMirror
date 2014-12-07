library(data.table)
library(ggplot2)

dat<-fread("G:/socialnetworks_project_log/pred_thresh_change/std/featureThreshold_subset.csv")
dat<-as.data.frame(dat)
dat<-dat[which(dat$Threshold %in% c(250,500,1000,1500,2000,2500)),] #,3000
dat$Threshold<-as.factor(dat$Threshold)
ggplot(dat, aes(FeatureSet, AUC)) +   
  geom_bar(aes(fill = Threshold), position = "dodge", stat="identity") +
  theme_bw(16) + #theme(axis.text=element_text(size=16)) +
  scale_y_continuous(expand = c(0,0)) + ggtitle("Performance of different categories\n at varying prediction threshold") +
  scale_fill_brewer(palette="Blues") #scale_fill_grey() #scale_fill_brewer(palette="Greys")
  #scale_fill_brewer(palette="Spectral")

