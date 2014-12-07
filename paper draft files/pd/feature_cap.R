#numtweets capping
library(data.table)
dat<-fread("G:/socialnetworks_project_log/feature11_check_country_us.csv")
dat<-as.data.frame(dat)
dat[which(dat$NumTweets>1000),c("NumTweets")]<-1000
write.csv(file="feature11_check_country_us_cap.csv", x=dat, row.names = F)
