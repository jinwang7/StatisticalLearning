# Created on Mon 11/9/20
# 
# auther Jin
# version 0.1
# 
# Rpart regression tree model 


library(rpart)
library(caret)
library(dplyr)
library(rpart.plot)
library(rattle)
library(MLmetrics)
library(data.table)
library(ggplot2)

# Read final modeling dataset - 10% of random sample from the 2019 dataset. 
data <- read.csv('data_final_model.csv', header=TRUE, stringsAsFactors = TRUE, na.strings =c("NA","NULL","-","NaN","Inf","") ) # read text file 


# Reorder levels in the categorical variables such as WeekDay and month 
data$WeekDay <- factor(data$WeekDay, levels=c("Mon", "Tue", "Wed", "Thu","Fri","Sat","Sun"))
data$month <- factor(data$month, levels=c("Jan", "Feb", "Mar", "Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"))

# Remove extreme values from dependent variable "car accident handling time" and select important explanatory variables
s = data[data$HT <=200,]

# Only select features in the final model - For demo purpose
vars <- setdiff(colnames(s), c("timeHour","year"))

s = s[,vars]


# Set up seeds and create testing and training data sets 
set.seed(123456)
# split into training data and testing data
nRec <- dim(s)[1]
trainSize <- round(nRec * 0.75)
testSize <- nRec - trainSize 

trainIdx <- sample(1:nRec, trainSize)
trainData <- s[trainIdx,]
testData <- s[-trainIdx,]

dim(trainData) # 71250    13
dim(testData) # 23750    13


# Set up hyperparameters 
control <- rpart.control(minsplit = 300, # the minimum # of obs. in a node 
                         minbucket = 100, # The minimum # of obs. in a terminal code 
                         maxdepth = 10,
                         cp = 10^(-4),
                         xval = 10 , # The # of cross-validations 
                         maxsurrogate = 0,
                         usesurrogate = 0)


fit <- rpart(HT ~ .,method="anova", data=trainData, control = control)
printcp(fit) # display the results  
# "rel error" is the ratio of the objective to that of a single root tree: always decrease with cp
# "xerror" is the average of 10 fold cross validation error 
plotcp(fit) # visualize cross-validation results


# Prune tree 
cp <- fit$cptable[which.min(fit$cptable[,4]),1]
fit.pruned = prune(fit, cp = cp)

# Important explanatary variables 
fit.pruned$variable.importance

# Tree chart
rpart.plot(fit.pruned)


# Prediction and prediction accuracy measurements 
pred <- predict(fit.pruned, newdata = testData)
RMSE(pred, testData$HT)
MAPE(pred, testData$HT)
cbind(pred = pred, obs = testData$HT)

# Make a graph between prediction and actual values
scatter.smooth(x=pred, y=testData$HT, main="Predicted HT ~ Actual HT")  # scatterplot

# Save outcome rules from the model 
write.csv(rpart.rules(fit.pruned, roundint = FALSE, cover = TRUE), 
          file = "tree_rule.csv", row.names=FALSE)


# Save predictions from the model 
write.csv(cbind(pred = pred, obs = testData$HT), 
          file = "prediction.csv", row.names=FALSE)


### The End








