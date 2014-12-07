library(data.table)
library(ggplot2)
library(rgl)
htlocMat<-fread("G:/socialnetworks_project_log/spectral_clustering/ht_loc_class_matrix.csv",header=T)
htlocMat<-as.data.frame(htlocMat)
htlocMat$Class<-as.factor(htlocMat$Class)
locMat<-htlocMat[,c(3:ncol(htlocMat))]

#first source
pc <- princomp(locMat, scores=TRUE)
summary(pc)
plot(pc,type="lines")
biplot(pc)
qplot(pc$scores[,2],pc$scores[,1])+ geom_point(aes(colour = htlocMat$Class))

#second source
pcaResult<-prcomp(locMat)
plot(pcaResult)
# plot scores 
scores <- as.data.frame(pcaResult$x) 
qplot(x = PC1, y = PC2, data = scores, geom = "point", col = htlocMat$Class)
biplot(pcaResult)

plot(pcaResult$x,col=htlocMat$Class)

#third source
library(ggbiplot)

pca <- prcomp(locMat)
scores <- as.data.frame(pca$x) 

dat<-fread("G:/socialnetworks_project_log/spectral_clustering/feature_clusters_loc_rbf_10_first.csv")
dat$ClusterNum <- NULL
dat<-as.data.frame(dat)
df <- cbind(subset(dat, select = c(1:(ncol(dat)-2))),subset(scores, select = c(1:1)),subset(dat, select = c(ncol(dat))))
write.csv(file="G:/socialnetworks_project_log/spectral_clustering/feature_cond_pca_1.csv",df,row.names=F)

givecolor = function(class){
  if(class == "Non-viral") "red"
  else "blue"
}
colors = sapply(htlocMat$Class, givecolor)
plot3d(scores[,1:3], col=colors)

g <- ggbiplot(pca, obs.scale = 1, var.scale = 1, 
              groups = htlocMat$Class, ellipse = FALSE, circle = FALSE)
g <- g + scale_color_discrete(name = '')
g <- g + theme(legend.direction = 'horizontal', 
               legend.position = 'top')
print(g)

summary(pca)
y<-c(0.4117, 0.1197, 0.07639, 0.06401, 0.03647, 0.03574, 0.02918, 0.02627, 0.02433, 0.01966)
x<-c("PC1","PC2","PC3","PC4","PC5","PC6","PC7","PC8","PC9","PC10")
names(y) <- x
barplot(y,las=2,main ="Proportion of Variance explained by\nPrincipal Components",ylab ="Proportion of Variance")

#prediction features
dat<-fread("G:/socialnetworks_project_log/spectral_clustering/features_pca_vis.csv")
dat$ClusterNum <- NULL
dat<-as.data.frame(dat)
dat$Class<-as.factor(dat$Class)
featureMat <- dat[,c(1:ncol(dat)-1)]
pca <- prcomp(featureMat, center=TRUE, scale.=TRUE)

summary(pca)
y<-c(0.185, 0.3352, 0.4600, 0.55221, 0.61382, 0.66854, 0.71040, 0.7510, 0.78565, 0.81872)
x<-c("PC1","PC1 to PC2","PC1 to PC3","PC1 to PC4","PC1 to PC5","PC1 to PC6","PC1 to PC7","PC1 to PC8","PC1 to PC9","PC1 to PC10")
names(y) <- x
barplot(y,las=2,main ="Cumulative Proportion of Variance\n explained by Principal Components",ylab ="Proportion of Variance")

scores <- as.data.frame(pca$x) 
givecolor = function(class){
  if(class == "Non-viral") "red"
  else "blue"
}
colors = sapply(dat$Class, givecolor)
scores_sub <- subset(scores,  scores[,3]>-20)
plot3d(scores_sub[,1:3], col=colors)

g <- ggbiplot(pca, obs.scale = 1, var.scale = 1, 
              groups = dat$Class, ellipse = FALSE, circle = FALSE)
g <- g + scale_color_discrete(name = '')
g <- g + theme(legend.direction = 'horizontal', 
               legend.position = 'top')
g <- g + ylim(c(-10, 10)) + coord_cartesian(xlim = c(-10, 10)) + theme_bw(16)
print(g)
ggsave(g,filename="pca_2d_all_features.png", dpi=600)

#hashtag word-cluster vectors
wordMat<-fread("G:/socialnetworks_project_log/histogram_of_counts/tag_histograms_1000_new.csv")
wordMat<-as.data.frame(wordMat)
wordMat<-wordMat[,c(2:ncol(wordMat))]
wordMat<-wordMat[which(dat$TagName %!in% c("yfsfant1","beforedadeal","bb07","maverickradio","mbeurope","goodchocolate")),]

pca <- prcomp(wordMat)
scores <- as.data.frame(pca$x) 

dat<-fread("G:/socialnetworks_project_log/histogram_of_counts/feature_files/feature_exp_cond.csv")
dat$Class<-as.factor(dat$Class)
dat<-dat[which(dat$TagName %!in% c("yfsfant1","beforedadeal","bb07","maverickradio","mbeurope","goodchocolate")),]

df <- cbind(subset(dat, select = c(2:10,48:52,17,18,53,20:22,24:28,55,58)),subset(scores, select = c(1:3)),subset(dat, select = c(60)))
write.csv(file="G:/socialnetworks_project_log/histogram_of_counts/features_pca_3.csv",df,row.names=F)

givecolor = function(class){
  if(class == "0") "red"
  else "blue"
}
colors = sapply(dat$Class, givecolor)
plot3d(scores[,1:3], col=colors)

g <- ggbiplot(pca, obs.scale = 1, var.scale = 1, 
              groups = dat$Class, ellipse = FALSE, circle = FALSE)
g <- g + scale_color_discrete(name = '')
g <- g + theme(legend.direction = 'horizontal', 
               legend.position = 'top')
print(g)
