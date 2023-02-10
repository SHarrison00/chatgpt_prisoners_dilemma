setwd("/Users/samharrison/Documents/data_sci/chatgpt_prisoners_dilemma")

# read
data <- read.csv("raw_data.csv")

# factorize / rename levels
data$Treatment <- factor(data$Treatment)
data$Treatment <- relevel(data$Treatment, ref = "T1")
data$Strategy <- factor(data$Strategy)
data$Strategy <- relevel(data$Strategy, ref = "TFT_C")
# create Treatment_Strategy column
data$Treatment_Strategy <- interaction(data$Treatment, data$Strategy)

# filter data to include main variables of interest
data <- data[, c("Treatment", "Strategy", "Treatment_Strategy", "Yi")]

# fit the model, and summarize
options(contrasts=c("contr.sum", "contr.sum"))
fit <- aov(Yi ~ Treatment + Strategy, data)
summary(fit)

# coefficient analysis
coef(fit)

# Extract the residuals
residuals <- residuals(fit)

library(ggplot2)
ggplot(data, aes(x = Treatment, y = residuals(fit))) +
  geom_boxplot()

ggplot(data, aes(x = Strategy, y = residuals(fit))) +
  geom_boxplot()

ggplot(data, aes(x = Treatment_Strategy, y = residuals(fit))) +
  geom_boxplot()


