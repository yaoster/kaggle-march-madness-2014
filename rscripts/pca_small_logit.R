source('load_data.R')

process.data <- function(data) {
    #data <- data.frame(sag_ps_last=data$sag_ps_last, dol_ps_last=data$dol_ps_last, col_ps_last=data$col_ps_last, wlk_ps_last=data$wlk_ps_last)
    #data <- data.frame(sag_ps_first=data$sag_ps_first, dol_ps_first=data$dol_ps_first, col_ps_first=data$col_ps_first, wlk_ps_first=data$wlk_ps_first)
    data <- data.frame(sag_ps_first=data$sag_ps_last_vs_first, dol_ps_first=data$dol_ps_last_vs_first, col_ps_first=data$col_ps_last_vs_first, wlk_ps_first=data$wlk_ps_last_vs_first)
    return(data)
}

# prune features and train logit model
ndim <- 4
target <- data$target
data <- process.data(data)
pca <- princomp(data, cor=T)
pcadata <- data.frame(pca$scores[,1:ndim])
#pcadata$Comp.4 <- NULL
pcadata$target <- as.numeric(target > 0)
model <- glm(target~., data=pcadata, family=binomial)

# apply to test data and write to output
TEST_SEASON <- 'Q'
TEST_OUTPUT <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/pca_small_logit_predictions.csv', sep='')
hteam <- test.data$hteam
lteam <- test.data$lteam
test.data <- process.data(test.data)
pca.test.data <- predict(pca, newdata=test.data)
pca.test.data <- data.frame(pca.test.data[,1:ndim])
predictions <- predict(model, pca.test.data, type='response')
output.game.id <- rep('', dim(test.data)[1])
output.pred <- rep(0, dim(test.data)[1])
for (i in 1:dim(test.data)[1]) {
    pwin <- predictions[i]
    team1 <- hteam[i]
    team2 <- lteam[i]
    if (hteam[i] > lteam[i]) {
        pwin <- 1 - pwin
        team1 <- lteam[i]
        team2 <- hteam[i]
    }
    game.id <- paste(TEST_SEASON, as.character(team1), as.character(team2), sep='_')
    output.game.id[i] <- game.id
    output.pred[i] <- pwin
}

output <- data.frame(id=output.game.id, pred=output.pred)
write.csv(output, file=TEST_OUTPUT, quote=F, row.names=F)
