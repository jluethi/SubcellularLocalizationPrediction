# Script to analyze mRNA localization to P-bodies in 20181102-bDNA-FISH-6 experiment
library(ggplot2)
library(ggforce)
# Type 4 probes
data = read.csv('/Users/Joel/Dropbox/Joel/PelkmansLab/Code/PyCharm/DeepLearning/notebooks/20181203-bDNA-FISH8-results-cleaned_improved.csv')

# combine T1 & T4 measurements into one (T1 for columns 3-8, T4 for 9 & 10)
# data$percentage_pbody = data$percentage_pbody_T1
# 
# data$percentage_pbody[as.character(data$well_name) == 'C09'] = data$percentage_pbody_T4[as.character(data$well_name) == 'C09']
# data$percentage_pbody[as.character(data$well_name) == 'C10'] = data$percentage_pbody_T4[as.character(data$well_name) == 'C10']
# data$percentage_pbody[as.character(data$well_name) == 'E09'] = data$percentage_pbody_T4[as.character(data$well_name) == 'E09']
# data$percentage_pbody[as.character(data$well_name) == 'E10'] = data$percentage_pbody_T4[as.character(data$well_name) == 'E10']


# Make selection for wells
row_c = startsWith(as.character(data$well_name), 'C')
row_e = startsWith(as.character(data$well_name), 'E')

#percentage_pbody_T1
# ggplot(data[data$well_name == 'E09',], aes(well_name, percentage_pbody_T4)) +
#   geom_sina(cex = 1) +
#   stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red')+
#   ylim(c(0,1))

cells_with_Pbodies = data$percentage_pbody > 0

ggplot(data[row_c,], aes(well_name, percentage_pbody)) +
  geom_sina() +
  ylim(c(0,0.4)) +
  stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red') +
  scale_x_discrete(labels = c('HPRT', 'Lamp1', 'CCND1', 'HIF1A', 'dapB', 'no probe', 'SPEN', 'no probe'))

ggplot(data[row_c & cells_with_Pbodies,], aes(well_name, percentage_pbody)) +
  geom_sina(cex = 1) +
  ylim(c(0,0.4)) +
  # stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red') +
  scale_x_discrete(labels = c('HPRT', 'Lamp1', 'CCND1', 'HIF1A', 'dapB', 'no probe', 'SPEN', 'no probe'))


ggplot(data[row_e,], aes(well_name, percentage_pbody)) +
  geom_sina(cex = 1) +
  ylim(c(0,0.4)) +
  stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red') +
  scale_x_discrete(labels = c('HPRT', 'Lamp1', 'CCND1', 'HIF1A', 'dapB', 'no probe', 'SPEN', 'no probe'))

ggplot(data[row_e & cells_with_Pbodies,], aes(well_name, percentage_pbody)) +
  geom_sina(cex = 1) +
  ylim(c(0,0.4)) +
  # stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red') +
  scale_x_discrete(labels = c('HPRT', 'Lamp1', 'CCND1', 'HIF1A', 'dapB', 'no probe', 'SPEN', 'no probe'))

# combine T1 & T4 measurements into one (T1 for columns 3-8, T4 for 9 & 10)
data$mRNA_spot_count = data$"mRNA_T1_Count_bDNA.FISH"

data$mRNA_spot_count[as.character(data$well_name) == 'C09'] = data$'mRNA_T4_Count_bDNA.FISH'[as.character(data$well_name) == 'C09']
data$mRNA_spot_count[as.character(data$well_name) == 'C10'] = data$'mRNA_T4_Count_bDNA.FISH'[as.character(data$well_name) == 'C10']
data$mRNA_spot_count[as.character(data$well_name) == 'E09'] = data$'mRNA_T4_Count_bDNA.FISH'[as.character(data$well_name) == 'E09']
data$mRNA_spot_count[as.character(data$well_name) == 'E10'] = data$'mRNA_T4_Count_bDNA.FISH'[as.character(data$well_name) == 'E10']

# Make sina plot for spot counts
ggplot(data[row_c,], aes(well_name, mRNA_spot_count)) +
  geom_sina(cex = 1, scale = FALSE) +
  # ylim(c(0,0.4)) +
  # stat_summary(fun.y = mean, fun.ymin = mean, fun.ymax = mean, geom = "crossbar", width = 0.5, col = 'red') +
  scale_x_discrete(labels = c('HPRT', 'Lamp1', 'CCND1', 'HIF1A', 'dapB', 'no probe', 'SPEN', 'no probe'))



