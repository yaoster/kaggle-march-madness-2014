source('load_data.R')

process.data <- function(data) {
    data$wlk_hrank_last_vs_first <- NULL
    data$dol_hrank_last_vs_first <- NULL
    data$col_hrank_last_vs_first <- NULL
    data$sag_hrank_last_vs_first <- NULL
    data$wlk_lrank_last_vs_first <- NULL
    data$dol_lrank_last_vs_first <- NULL
    data$col_lrank_last_vs_first <- NULL
    data$sag_lrank_last_vs_first <- NULL
    data$wlk_ps_last_vs_first <- NULL
    data$dol_ps_last_vs_first <- NULL
    data$col_ps_last_vs_first <- NULL
    data$sag_ps_last_vs_first <- NULL
    data$wlk_hrank_last_vs_first_ps <- NULL
    data$dol_hrank_last_vs_first_ps <- NULL
    data$col_hrank_last_vs_first_ps <- NULL
    data$sag_hrank_last_vs_first_ps <- NULL
    data$wlk_lrank_last_vs_first_ps <- NULL
    data$dol_lrank_last_vs_first_ps <- NULL
    data$col_lrank_last_vs_first_ps <- NULL
    data$sag_lrank_last_vs_first_ps <- NULL
    return(data)
}

# prune features and train logit model
ndim <- 2
data <- process.data(data)
pca <- princomp(data[,2:dim(data)[2]], cor=T)
pcadata <- data.frame(pca$scores[,1:ndim])
#pcadata$Comp.4 <- NULL
pcadata$target <- as.numeric(data$target > 0)
model <- glm(target~., data=pcadata, family=binomial)

# apply to test data and write to output
TEST_SEASON <- 'Q'
TEST_OUTPUT <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/pca_logit_predictions.csv', sep='')
test.data <- process.data(test.data)
pca.test.data <- predict(pca, newdata=test.data)
pca.test.data <- data.frame(pca.test.data[,1:ndim])
predictions <- predict(model, pca.test.data, type='response')
output.game.id <- rep('', dim(test.data)[1])
output.pred <- rep(0, dim(test.data)[1])
attach(test.data)
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
detach(test.data)

output <- data.frame(id=output.game.id, pred=output.pred)
write.csv(output, file=TEST_OUTPUT, quote=F, row.names=F)
