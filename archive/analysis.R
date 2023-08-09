setwd("/Users/samharrison/Documents/data_sci/chatgpt_prisoners_dilemma")

# read
data <- read.csv("raw_data.csv")

# factorize / rename levels
data$Treatment <- factor(data$Treatment)
levels(data$Treatment) <- c("A0", "A1", "A2")
data$Treatment <- relevel(data$Treatment, ref = "A0")
data$Strategy <- factor(data$Strategy)
levels(data$Strategy) <- c("F1", "F0")
data$Strategy <- relevel(data$Strategy, ref = "F0")

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

# reorder
data$Treatment_Strategy <- factor(data$Treatment_Strategy,
    levels = c("A0.F0", "A0.F1", "A1.F0", "A1.F1", "A2.F0", "A2.F1"))

# reorder
levels(data$Treatment) <- c("A0: No\nanthropom.",
                            "A1:\nText-based",
                            "A2:\nVoice-based")

# my colours
my_colors <- c("lightskyblue2", 
               "skyblue4", 
               "lightskyblue2", 
               "skyblue4", 
               "lightskyblue2", 
               "skyblue4")

# boxplot
ggplot(data, aes(x = Strategy, y = Yi, fill = Strategy)) +
  geom_boxplot() +
  scale_fill_manual(values = my_colors, labels = c("F0: Cooperate", "F1: Betray")) +
  labs(x = "Treatment Combination", y = "Response, Y\n(Cooperation measure)",
       title = "Response for each Treatment Combination") +
  facet_wrap(~ factor(Treatment)) +
  guides(fill = guide_legend(title = "First move made\nby computer ")) + 
  theme(plot.title = element_text(hjust = 0.5, size = 20), 
        axis.title.x = element_text(size = 18),
        axis.title.y = element_text(size = 18),
        strip.text = element_text(size = 16),
        legend.title = element_text(size = 16),
        legend.text = element_text(size = 14),
        axis.text.x = element_text(size = 14),
        axis.text.y = element_text(size = 14))



