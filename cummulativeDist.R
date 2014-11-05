library(data.table)
dat<-fread("G:/socialnetworks_project_log/geo_us_stats1.csv")

library(ggplot2)
ggplot(dat,aes(x = V2)) +xlab("proportion of users from US") + ylab("number of hashtags") + ggtitle("cumulative frequency of hashtags")+
stat_bin(aes(y=cumsum(..count..)),geom="smooth") +theme_bw(16)

dat1<-dat[which(dat$V2<0.25),]
ggplot(dat1,aes(x = V3)) +xlab("number of tweets") + ylab("number of hashtags") + ggtitle("cumulative frequency of hashtags")+
  stat_bin(aes(y=cumsum(..count..)),geom="smooth")

nrow(dat1[which(dat1$V3>=10000),])
nrow(dat1[which(dat1$V3>=10000),])/nrow(dat1)
write.csv(file="tags_us_25.csv",dat1$V1,row.names=F)
