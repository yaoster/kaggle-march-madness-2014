library(randomForest)
source('load_data.R')
data <- as.matrix(data)
p <- dim(data)[2] - 1
rf <- randomForest(x=data[,2:dim(data)[2]], y=data[,1], corr.bias=T, do.trace=T,
                   ntree=801, 
                   mtry=p/3, # default p/3
                   nodesize=15 # default 5
)

#param1 <- c()
#param2 <- c()
#param3 <- c()
#rsq <- c()
#for (ntree in seq(100, 1000, 100)) {
#    for (mtry in seq(p/5, p, p/5)) {
#        for (nodesize in (seq(5, 50, 5))) {
#            print('*****')
#            print(c(ntree, mtry, nodesize))
#            rf <- randomForest(x=data[,2:dim(data)[2]], y=data[,1], corr.bias=T, 
#                               ntree=ntree, 
#                               mtry=mtry,
#                               nodesize=nodesize)
#            print(rf$rsq[length(rf$rsq)])
#            param1 <- c(param1, ntree)
#            param2 <- c(param2, mtry)
#            param3 <- c(param3, nodesize)
#            rsq <- c(rsq, rf$rsq[length(rf$rsq)])
#        }
#    }
#}
