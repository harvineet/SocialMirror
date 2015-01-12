library(data.table)
dat<-fread("G:/socialnetworks_project_log/tweet sentiment/tag_sentiment.tsv")
dat<-as.data.frame(dat)
dat$Class<-as.factor(dat$Class)
dat$Polarity<-as.factor(dat$Polarity)

dat_v<-dat[which(dat$Class==1),]
dat_nv<-dat[which(dat$Class==0),]
dat_plot<-dat_v[20000:50000,]
dat1_plot<-dat_nv[20000:50000,]

library(ggplot2)
ggplot(dat_plot, aes_string(x="TweetNum", y="Polarity")) +
  geom_bar(stat = "identity") +
  facet_wrap( ~ TagName)
ggplot(dat1_plot, aes_string(x="TweetNum", y="Polarity")) +
  geom_bar(stat = "identity") +
  facet_wrap( ~ TagName)

# Box plot
p<-ggplot(dat,aes(y=Polarity,x=Class, fill=Class)) +
  geom_boxplot() +
  ylab(feature) + scale_fill_manual(values = c("#4A6FE3","#D33F6A"), labels = c("0" = "Non-Viral", "1" = "Viral")) +
  theme_bw(16) + scale_y_continuous(expand = c(0,0)) +
  ggtitle("Class wise box plot of sentiment labels")
print(p)

test<-dat[which(dat$TagName=='instagramnotworking'),]
ggplot(test, aes_string(x="TweetNum", y="Polarity",fill="Polarity")) +
  geom_tile()

ggplot(test, aes_string(x="TweetNum", y="Polarity")) +
  geom_line()

ggplot(test, aes_string(x="TweetNum", y="Class")) +
  geom_point(aes(color = Polarity), position = position_jitter(height = .1))+
  scale_colour_manual(values = c('red','blue','green')) +
  ggtitle(paste("Non-Viral topic","\n#",test$TagName[1]))+
  xlab("Number of tweets") + ylab(" ") +
  theme(axis.ticks.x = element_blank(), axis.text.y = element_blank())

ggplot(test, aes_string(x="TweetNum", y="Polarity")) +
  geom_point(aes(color = Polarity))+scale_colour_manual(values = c('red','blue','green')) +
  ggtitle(paste("Non-Viral topic","\n#",test$TagName[1]))+
  xlab("Number of tweets")+ylab(" ") +
  theme(axis.ticks.x = element_blank(), axis.text.y = element_blank())

ggplot(test, aes_string(x="TweetNum", y="Polarity")) +
  geom_bar(data=subset(test,Polarity==0), colour="blue", stat = "identity",position = "identity") +
  geom_bar(data=subset(test,Polarity==1), colour="green", stat = "identity",position = "identity") +
  geom_bar(data=subset(test,Polarity==-1), colour="red", stat = "identity",position = "identity")

ggplot(test, aes_string(x="TweetNum", y="Polarity")) +
  geom_bar(data=subset(test,Polarity==0),aes(y = Polarity+1), colour="blue", stat = "identity",position = "identity") +
  geom_bar(data=subset(test,Polarity==1),aes(y = Polarity), colour="green", stat = "identity",position = "identity") +
  geom_bar(data=subset(test,Polarity==-1),aes(y = -Polarity), colour="red", stat = "identity",position = "identity")