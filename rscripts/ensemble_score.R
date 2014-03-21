logit.predictions <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/logit_predictions.csv', sep='')
rf.predictions <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/rf_predictions.csv', sep='')
net.predictions <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/net_predictions.csv', sep='')
gbm.predictions <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/gbm_predictions.csv', sep='')
logit.df <- read.table(logit.predictions, sep=',', header=T)
rf.df <- read.table(rf.predictions, sep=',', header=T)
net.df <- read.table(net.predictions, sep=',', header=T)
gbm.df <- read.table(gbm.predictions, sep=',', header=T)
predictions <- cbind(logit.df$pred, rf.df$pred, net.df$pred, gbm.df$pred)

pred <- (1/3)*logit.df$pred + (1/6)*rf.df$pred + (1/3)*net.df$pred + (1/6)*gbm.df$pred
ensemble.predictions <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/test_predictions.csv', sep='')
write.csv(data.frame(id=logit.df$id, pred=pred), file=ensemble.predictions, quote=F, row.names=F)
