TRAINING_DATA <- '/home/yaoster/kaggle/kaggle-march-madness-2014/data/features.csv'

data <- read.table(TRAINING_DATA, sep=',', header=T)
data$gameid <- NULL
data$hteam <- NULL
data$lteam <- NULL
data <- as.matrix(data)
p <- dim(data)[2] - 1
rf <- randomForest(x=data[,2:dim(data)[2]], y=data[,1], ntree=501, mtry=p, corr.bias=T, do.trace=T)
