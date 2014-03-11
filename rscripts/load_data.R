TRAINING_DATA <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/features.csv', sep='')
data <- read.table(TRAINING_DATA, sep=',', header=T, as.is=T)
data <- data[complete.cases(data),]
data$gameid <- NULL
data$hteam <- NULL
data$lteam <- NULL
