# Script to analyze differences in ABCD3 SLP prediction error rates
library(stringr)
base_path = '/Users/Joel/Desktop/20180620_Predictions/TestLosses/DDX6_Rescaling32/'
models = list.files(base_path)
model_inputs_chars = str_extract(models,"Input_.*_Pred")
model_inputs = substr(model_inputs_chars,7,nchar(model_inputs_chars) - 5)

percentage_model2_better = data.frame()
model_difference_scores = data.frame()
model_difference_scores_squared = data.frame()

# I used different scaling of the DDX6 image (16, 50, 32). Not sure if that's an issue which I need to correct for. Currently rerunning DAPI and DAPI + Succs network with scaling 32 to check
# loss_scaling = c(50,16,16,50,32,32)    
# general_scale_factor = 100

for (i in 1:length(models)){
  scores_model1 = read.csv(paste0(base_path,models[i]), header = FALSE)
  percentage_model2_better_current = c()
  current_model_difference_scores = c()
  current_model_difference_scores_squared = c()
  # mean(scores_model1$V1)
  # scores_model1$V1 = scores_model1$V1/loss_scaling[i] * general_scale_factor
  
  for (j in 1:(length(models))) { #length(models)
    scores_model2 = read.csv(paste0(base_path,models[j]), header = FALSE)
    # scores_model2$V1 = scores_model2$V1/loss_scaling[j] * general_scale_factor
    
    combined_scores = merge(scores_model1,scores_model2,by.x = 'V2', by.y = 'V2')
    colnames(combined_scores) = c('CellName', 'ScoreModel1','ScoreModel2')
    combined_scores$bigModelBetter = combined_scores$ScoreModel1 > combined_scores$ScoreModel2
    percentage_bigger_model_better = round(sum(combined_scores$bigModelBetter)/length(combined_scores$bigModelBetter),3)*100
    model_difference_score = round(mean((combined_scores$ScoreModel1 - combined_scores$ScoreModel2)),3)
    model_difference_score2 = round(mean((combined_scores$ScoreModel1 - combined_scores$ScoreModel2) ^ 2),3)
    title_str = paste0(model_inputs[i], ' vs ', model_inputs[j])
    percentage_model2_better_current = c(model_inputs[i],model_inputs[j],percentage_bigger_model_better)
    current_model_difference_scores = c(model_inputs[i],model_inputs[j],model_difference_score)
    current_model_difference_scores_squared = c(model_inputs[i],model_inputs[j],model_difference_score2)
    
    percentage_model2_better_current = data.frame(t(percentage_model2_better_current))
    colnames(percentage_model2_better_current) = c('Model1', 'Model2', 'percentage_model2_better')
    percentage_model2_better = rbind(percentage_model2_better,percentage_model2_better_current)
    
    current_model_difference_scores = data.frame(t(current_model_difference_scores))
    colnames(current_model_difference_scores) = c('Model1', 'Model2', 'model_scores')
    model_difference_scores = rbind(model_difference_scores,current_model_difference_scores)
    
    current_model_difference_scores_squared = data.frame(t(current_model_difference_scores_squared))
    colnames(current_model_difference_scores_squared) = c('Model1', 'Model2', 'model_scores_squared')
    model_difference_scores_squared = rbind(model_difference_scores_squared,current_model_difference_scores_squared)
  }
  
  # Update all the data frames with the current comparisons
  # percentage_model2_better_current = data.frame(t(percentage_model2_better_current))
  # colnames(percentage_model2_better_current) = model_inputs
  # rownames(percentage_model2_better_current) = model_inputs[i]
  # percentage_model2_better = rbind(percentage_model2_better,percentage_model2_better_current)
  
  # current_model_difference_scores = data.frame(t(current_model_difference_scores))
  # colnames(current_model_difference_scores) = model_inputs
  # rownames(current_model_difference_scores) = model_inputs[i]
  # model_difference_scores = rbind(model_difference_scores,current_model_difference_scores)
  
  # current_model_difference_scores_squared = data.frame(t(current_model_difference_scores_squared))
  # colnames(current_model_difference_scores_squared) = model_inputs
  # rownames(current_model_difference_scores_squared) = model_inputs[i]
  # model_difference_scores_squared = rbind(model_difference_scores_squared,current_model_difference_scores_squared)
}

# Plot all scores comparing the models pairwise
# Heatmap
library(ggplot2)
model_difference_scores$model_scores = as.numeric(levels(model_difference_scores$model_scores))[model_difference_scores$model_scores]
ggplot(data = model_difference_scores, aes(Model1,Model2, fill = model_scores))+
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = 0, limit = c(-0.5,0.5), space = "Lab",
                       name="Average Loss\nDifference") +
  theme_minimal()+
  theme(axis.text.x = element_text(angle = 15, vjust = 1,
                                   size = 12, hjust = 1))+
  coord_fixed()

model_difference_scores_squared$model_scores_squared = as.numeric(levels(model_difference_scores_squared$model_scores_squared))[model_difference_scores_squared$model_scores_squared]
ggplot(data = model_difference_scores_squared, aes(Model1,Model2, fill = model_scores_squared))+
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = 0, limit = c(0,0.2), space = "Lab",
                       name="Average Loss\nDifference Squared") +
  theme_minimal()+
  theme(axis.text.x = element_text(angle = 15, vjust = 1,
                                   size = 12, hjust = 1))+
  coord_fixed()

percentage_model2_better$percentage_model2_better = as.numeric(levels(percentage_model2_better$percentage_model2_better))[percentage_model2_better$percentage_model2_better]
ggplot(data = percentage_model2_better, aes(Model1,Model2, fill = percentage_model2_better))+
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = 50, limit = c(0,100), space = "Lab",
                       name="Percentage Model2\nbetter") +
  theme_minimal()+
  theme(axis.text.x = element_text(angle = 15, vjust = 1,
                                   size = 12, hjust = 1))+
  coord_fixed()

# Manually make a dot plot for 1 comparison
# score_structural = read.csv('/Users/Joel/Desktop/20180620_Predictions/TestLosses/TestLoss_SLP_SubcellularLoss_Input_2_DAPI_3_GM130_4_HSP60_7_Acetyl_Tubulin_7_Actin_Predicting_9_ABCD3.csv', header = FALSE)
# score_structural = read.csv('/Users/Joel/Desktop/20180620_Predictions/TestLosses/TestLoss_SLP_SubcellularLoss_Input_2_DAPI_10_Pericentrin_11_EEA1_11_Sara_1_Lamp1_1_PCNA_2_Calreticulin_3_APPL_3_GM130_4_HSP60_4_LC3B_5_pS6_5_Yap_7_Acetyl_Tubulin_7_Actin_8_Caveolin_8_Pol2_Predicting_9_ABCD3.csv', header = FALSE)
# score_endocytic = read.csv('/Users/Joel/Desktop/20180620_Predictions/TestLosses/TestLoss_SLP_SubcellularLoss_Input_2_DAPI_11_EEA1_11_Sara_1_Lamp1_2_Calreticulin_3_APPL_4_LC3B_8_Caveolin_Predicting_9_ABCD3.csv', header = FALSE)
score_structural = read.csv('/Users/Joel/Desktop/20180620_Predictions/TestLosses/DDX6_Rescaling32/TestLoss_5x5_20180705SLP_SubcellularLoss_Input_2_DAPI_Predicting_13_DDX6.csv', header = FALSE)
score_endocytic = read.csv('/Users/Joel/Desktop/20180620_Predictions/TestLosses/DDX6_Rescaling32/TestLoss_5x5_20180705SLP_SubcellularLoss_Input_2_DAPI_13_Succs_Predicting_13_DDX6.csv', header = FALSE)

hist(score_endocytic$V1,500, xlim = c(0.2,4))
mean(score_structural$V1)
mean(score_endocytic$V1)
combined_scores = merge(score_structural,score_endocytic,by.x = 'V2', by.y = 'V2')
colnames(combined_scores) = c('CellName', 'ScoreDapi','ScoreFull')
combined_scores$bigModelBetter = combined_scores$ScoreDapi > combined_scores$ScoreFull
percentage_bigger_model_better = paste0(toString(round(sum(combined_scores$bigModelBetter)/length(combined_scores$bigModelBetter),3)*100),'%')
model_difference_score = round(sum((combined_scores$ScoreDapi - combined_scores$ScoreFull)/ length(combined_scores$ScoreDapi)),3)
model_difference_score2 = round(sum((combined_scores$ScoreDapi - combined_scores$ScoreFull) ^ 2)/ length(combined_scores$ScoreDapi) ,3)

library(ggplot2)
d = ggplot(combined_scores, aes(x = ScoreDapi, y = ScoreFull, color = factor(bigModelBetter))) +
  geom_point() +
  # ggtitle("DAPI vs. DAPI_EEA1_TfnR_Actin_aTubulin_GSK3b_Sara_CRT_Pericentrin") +
  # xlab('Error DAPI_3_GM130_4_HSP60_7_Acetyl_Tubulin_7_Actin') +
  xlab('Error DAPI Model') +
  ylab('Error DAPI & Succs Model') +
  xlim(c(0,1)) +
  ylim(c(0,1)) +
  geom_abline(intercept = 0, slope = 1, color = "red")
d + annotate("text",x = 0.5, y = 0.85,label = percentage_bigger_model_better) +
  annotate("text",x = 0.5, y = 0.75,label = model_difference_score)
