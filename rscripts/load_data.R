TRAINING_DATA <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/features.csv', sep='')
data <- read.table(TRAINING_DATA, sep=',', header=T, as.is=T)
data <- data[complete.cases(data),]
data$gameid <- NULL
data$hteam <- NULL
data$lteam <- NULL
data$seed_diff <- NULL

TEST_DATA <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/test.csv', sep='')
test.data <- read.table(TEST_DATA, sep=',', header=T, as.is=T)
test.data$gameid <- NULL
test.data$seed_diff <- NULL
