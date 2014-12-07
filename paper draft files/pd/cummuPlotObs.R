require(plyr)
library(ggplot2)

dat<-fread("G:/socialnetworks_project_log/paper draft files/cummObsTime_comb_modified.csv",header=T)
mydf_m <- ddply(dat,.(variable),transform, ecd = ecdf(value)(value))

ggplot(mydf_m,aes(x = value, y = ecd)) + geom_line(aes(group = variable,colour = variable)) + scale_y_continuous(expand = c(0,0))  + ylab("Cumulative distribution") + xlab("Observation time (in days)") + 
  theme_bw(30) +theme(legend.text = element_text(size = 24,face = "bold")) + labs(colour = "Dataset")+
  guides(colour = guide_legend(override.aes = list(size=2)))
ggsave(filename="cumulativePlotObsTime_modified.png", )

ggplot(mydf_m,aes(x = value)) + stat_ecdf(aes(colour = variable))

theme(legend.text = element_text(face = "bold"))
+theme(text=element_text(face = "bold"))
theme(axis.title=element_text(face="bold.italic", 
                              size="12", color="brown"), legend.position="top")