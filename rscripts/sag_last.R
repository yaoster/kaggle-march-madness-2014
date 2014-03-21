source('load_data.R')

process.data <- function(data) {
    data <- data.frame(target=data$target, sag_ps_first=data$sag_ps_first)
    return(data)
}

# prune features and train logit model
data <- process.data(data)
data$target <- as.numeric(data$target > 0)
model <- glm(target~., data=data, family=binomial)

# apply to test data and write to output
TEST_SEASON <- 'Q'
TEST_OUTPUT <- paste(path.expand('~'), '/src/kaggle/kaggle-march-madness-2014/data/sag_last_predictions.csv', sep='')
test.data <- data.frame(hteam=test.data$hteam, lteam=test.data$lteam, sag_ps_first=test.data$sag_ps_first)
predictions <- predict(model, test.data, type='response')
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
