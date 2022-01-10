# wells = c('C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
#           'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16',
#           'E05', 'E06', 'E07', 'E08', 'F05', 'F06', 'F07', 'F08')
# all_feature_values = data.frame()
# 
# for(i in 1:36){
#   well = wells[i]
#   feature_values = read.csv(paste0('/Users/Joel/shares/workShareJoel/SLP_feature_values/20180601-SLP_Multiplexing_p1_', well,'_Cells_feature-values.csv'))
#   meta_data = read.csv(paste0('/Users/Joel/shares/workShareJoel/SLP_feature_values/Metadata_', well,'.csv'))
#   
#   # colnames(feature_values)
#   # sum(is.nan(feature_values$Nuclei_Morphology_Elongation))
#   # sum(is.nan(feature_values$Nuclei_Texture_LBP.radius.1.4_2_DAPI.rescaled_image))
#   # sum(is.nan(feature_values$Nuclei_Texture_LBP.radius.1.5_1_PCNA.rescaled_image))
#   
#   a = colnames(meta_data)
#   a[19] = 'SPhase'
#   colnames(meta_data) = a
# 
#   # Check that mapobject ids are identical
#   if (sum(meta_data$mapobject_id != feature_values$mapobject_id) > 0) {
#     print('Metadata & feature values mapobject_id mismatch in current well!!')
#     break
#   }
#   
#   feature_values = cbind(meta_data[,c(2,3,4,5,8)], feature_values)
#   
#   feature_values$SPhase = meta_data$SPhase
#   # Sort out artefacts
#   to_be_removed = meta_data$is_border | meta_data$DAPI_Debris | meta_data$Mitotic | meta_data$Multinuclei
#   feature_values = feature_values[!to_be_removed,]
#   
#   area_threshold = 10000
#   feature_values = feature_values[feature_values$Morphology_Area > area_threshold,]
#   
#   
#   # Cell cyle
#   # library(mixtools)
#   # fit_data = feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image
#   # mixmdl = normalmixEM(fit_data, sigma = c(100000, 100000))
#   # plot(mixmdl,which=2, n = 50)
#   # lines(density(fit_data), lty=2, lwd=2)
#   
#   library(ggplot2)
#   # http://ianmadd.github.io/pages/PeakDensityDistribution.html
#   # Find the g1 peak
#   feature_values$CellCycle = NaN
#   feature_values[feature_values$SPhase == 1,]$CellCycle = 'S'
#   feature_values_nonS = feature_values[feature_values$SPhase == 0,]
#   x_axis_value = which.max(density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$y)
#   g1_peak = density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$x[x_axis_value]
#   
#   # Find the G2 peak: Peak that has at least 1.5x the DAPI intensity
#   MaxY<- max(density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$y[density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$x > g1_peak*1.5])
#   g2_peak = density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$x[which(density(feature_values_nonS$Nuclei_Intensity_sum_2_DAPI.rescaled_image)$y == MaxY)]
#   
#   span = (g2_peak - g1_peak) / 3
#   
#   # ggplot(feature_values_nonS, aes(Nuclei_Intensity_sum_2_DAPI.rescaled_image)) +
#   #   geom_density() +
#   #   geom_vline(xintercept = g1_peak, color = 'red') +
#   #   geom_vline(xintercept = g2_peak, color = 'green') +
#   #   geom_vline(xintercept = g1_peak - span, color = 'red', linetype='dashed') +
#   #   geom_vline(xintercept = g1_peak + span, color = 'red', linetype='dashed') +
#   #   geom_vline(xintercept = g2_peak - span, color = 'green', linetype='dashed') +
#   #   geom_vline(xintercept = g2_peak + span, color = 'green', linetype='dashed')
#   
#   g1_cells = (feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image > g1_peak - span) & (feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image < g1_peak + span) & !feature_values$SPhase
#   g2_cells = (feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image > g2_peak - span) & (feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image < g2_peak + span) & !feature_values$SPhase
#   feature_values[g1_cells == 1,]$CellCycle = 'G1'
#   feature_values[g2_cells == 1,]$CellCycle = 'G2'
#   
#   # Remove cells with unclear cell cycle information
#   feature_values = feature_values[!feature_values$CellCycle == 'NaN',]
#   feature_values$CellCycle = factor(feature_values$CellCycle, levels = c('G1', 'S', 'G2'))
#   
#   # Fuse feature_values
#   all_feature_values = rbind(all_feature_values, feature_values)
# }
# 
# 
# # Remove some outliers: sum_DAPI > 2'000'000
# all_feature_values = all_feature_values[all_feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image < 2000000,]
# 
# 
# # Add metadata info to the features, then save combined data
# write.table(all_feature_values, file = '/Users/Joel/shares/workShareJoel/SLP_feature_values/featureValues_allWells.csv', 
#             sep = ',', row.names = FALSE, col.names = TRUE)

# Load data
require(data.table)
all_feature_values = fread('/Users/Joel/shares/workShareJoel/SLP_feature_values/featureValues_allWells.csv', sep = ',', header = TRUE)

# Remove some more outliers: sum_DAPI > 1'500'000
all_feature_values = all_feature_values[all_feature_values$Nuclei_Intensity_sum_2_DAPI.rescaled_image < 1500000,]


## PLOT GENERAL P BODY STATISTICS
# P body count
library(ggplot2)
ggplot(all_feature_values, aes(x = CellCycle, y = Pbodies_Count)) +
  geom_boxplot() +
  scale_y_continuous(breaks = c(5,10,15,20,25,30,40,50,60,70)) + 
  theme(axis.text.x = element_text(size=14),axis.text.y = element_text(size=14))

ggplot(all_feature_values, aes(x = CellCycle, y = Pbodies_Mean_Morphology_Area)) +
  geom_boxplot()+
  scale_y_continuous(breaks = c(50,75,100,150,200)) + 
  theme(axis.text.x = element_text(size=14),axis.text.y = element_text(size=14))

median(all_feature_values[all_feature_values$CellCycle == 'G2',]$Pbodies_Count)/median(all_feature_values[all_feature_values$CellCycle == 'G1',]$Pbodies_Count)

hist(feature_values$Pbodies_Count,50)

# Plot P bodies count vs. Integrated DAPI
ggplot(all_feature_values, aes(x = Nuclei_Intensity_sum_2_DAPI.rescaled_image, y = Pbodies_Mean_Morphology_Area)) +
  geom_point(shape = '.')



## PREDICT P BODIES
# Throw out column that are constant or mostly contain NaNs. Throw out some cells that are NaN for a feature
library(dplyr)
all_feature_values_withPbodies = all_feature_values[all_feature_values$Pbodies_Count != 0,]
colnames(all_feature_values_withPbodies)[colSums(is.na(all_feature_values_withPbodies)) > 0]

all_feature_values_withPbodies = all_feature_values_withPbodies[!is.na(all_feature_values_withPbodies$Pbodies_Mean_Morphology_Circularity),]

zero_columns = c(c(FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), colSums(all_feature_values_withPbodies[, -c(1:6,4230, 4231)] != 0) == 0, c(FALSE, FALSE))
all_feature_values_withPbodies = select(all_feature_values_withPbodies, - as.integer(which(zero_columns)))
# Remove all P body count features and measurements of DDX6 & DCP1a
features = colnames(all_feature_values_withPbodies)

# For the moment, remove all measurements only made in P bodies (total amounts will scale too well with P body number)
pbody_features = unique(c(grep('DDX6', features), grep('DCP1a', features), grep('Pbodies', features)))


features_to_be_excluded = unique(c(1:6, grep('Count', features), grep('CellCycle', features), grep('SPhase', features),pbody_features))
pca_input_data = select(all_feature_values_withPbodies, -features_to_be_excluded)

## 75% of the sample size for training
smp_size <- floor(0.75 * nrow(all_feature_values_withPbodies))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(all_feature_values_withPbodies)), size = smp_size)

train_input_data = select(all_feature_values_withPbodies, -features_to_be_excluded)[train_ind,]
test_input_data = select(all_feature_values_withPbodies, -features_to_be_excluded)[-train_ind,]

# do PCA (watch out for Cell Cycle info)
require(caret)
transformed_train_feature_data = preProcess(train_input_data,method=c("BoxCox", "center", "scale", "pca"))
train_pc_features = predict(transformed_all_feature_data, train_input_data)
test_pc_features = predict(transformed_all_feature_data, test_input_data)

# write.table(pc_features, file = '/Users/Joel/shares/workShareJoel/SLP_feature_values/pc_features_20180629_BoxCox_noPbody_measurements.csv',
#             sep = ',', row.names = FALSE, col.names = TRUE)

# pca_features = fread('/Users/Joel/shares/workShareJoel/SLP_feature_values/pc_features_20180629_BoxCox_noPbody_measurements.csv', sep = ',', header = TRUE)

sum(is.na(pc_features))
# pca_features = prcomp(pca_input_data, center = TRUE, scale. = TRUE)

# Divide data in train & test (maybe even before PCA application), then run linear model & prediction
fit = lm(all_feature_values_withPbodies$Pbodies_Count ~ ., data = pc_features)
median(fit$residuals^2)
median(abs(fit$residuals))
mean(all_feature_values_withPbodies$Pbodies_Count)

fit2 = lm(all_feature_values_withPbodies$Pbodies_Count ~ Nuclei_Intensity_min_5_Yap.rescaled_image, data = all_feature_values_withPbodies)
median(fit2$residuals^2)
median(abs(fit2$residuals))

fit3 = lm(all_feature_values_withPbodies$Pbodies_Count ~ Nuclei_Intensity_sum_2_DAPI.rescaled_image, data = all_feature_values_withPbodies)
median(fit3$residuals^2)
median(abs(fit3$residuals))

# residuals_allFeatures = data.frame(cbind(fit$residuals^2, rep('AllFeatures', length(fit$residuals))))
# residuals_minYap = data.frame(cbind(fit2$residuals^2, rep('MinYap', length(fit2$residuals))))
# residuals_sumDapi = data.frame(cbind(fit3$residuals^2, rep('SumDAPI', length(fit3$residuals))))
residuals_allFeatures = data.frame(cbind(abs(fit$residuals), rep('AllFeatures', length(fit$residuals))))
residuals_minYap = data.frame(cbind(abs(fit2$residuals), rep('MinYap', length(fit2$residuals))))
residuals_sumDapi = data.frame(cbind(abs(fit3$residuals), rep('SumDAPI', length(fit3$residuals))))
count_residuals = rbind(residuals_minYap, residuals_sumDapi, residuals_allFeatures)
count_residuals$X1 = as.numeric(as.character(count_residuals$X1))
# count_residuals$X2 = factor(count_residuals$X2)

ggplot(data = count_residuals, aes(x=X2, y = X1)) +
  geom_boxplot() +
  ylab('Squared Error') +
  xlab('') +
  ylim(c(0,50))


fit = lm(all_feature_values_withPbodies$Pbodies_Mean_Morphology_Area ~ ., data = pc_features)
fit2 = lm(all_feature_values_withPbodies$Pbodies_Mean_Morphology_Area ~ Nuclei_Intensity_min_5_Yap.rescaled_image, data = all_feature_values_withPbodies)
fit3 = lm(all_feature_values_withPbodies$Pbodies_Mean_Morphology_Area ~ Nuclei_Intensity_sum_2_DAPI.rescaled_image, data = all_feature_values_withPbodies)

combined_fits = data.frame(cbind(abs(fit$residuals), abs(fit2$residuals)))

ggplot(data = combined_fits, aes(x = X1, y = X2)) +
  geom_point() + 
  xlim(c(0,40)) +
  ylim(c(0,40)) +
  geom_abline(intercept = 0, slope = 1, color = "red")




# Train MLR model
library(glmnet)

x = model.matrix(~., data=pc_features)
y = all_feature_values_withPbodies$Pbodies_Count

# use 10x crossvalidation to train optimal classifiers at different values for lambda using LASSO
cvfit = cv.glmnet(x, y) #, family = 'binomial'

# extract the model error and coefficientsof the optimal classifier
crossValidationErrorAtLambda1se = cvfit$cvm[cvfit$lambda==cvfit$lambda.1se]
fit = lm(all_feature_values_withPbodies$Pbodies_Count ~ pc_features)


# Run dummy model just based on DAPI
x1 = model.matrix(~all_feature_values_withPbodies$Nuclei_Intensity_sum_2_DAPI.rescaled_image)
y1 = all_feature_values_withPbodies$Pbodies_Count

# use 10x crossvalidation to train optimal classifiers at different values for lambda using LASSO
cvfit1 = cv.glmnet(x1, y1) #, family = 'binomial'

# extract the model error and coefficientsof the optimal classifier
crossValidationErrorAtLambda1se1 = cvfit1$cvm[cvfit$lambda==cvfit$lambda.1se]

# Run dummy model just based on Yap
x2 = model.matrix(~all_feature_values_withPbodies$Nuclei_Intensity_min_5_Yap.rescaled_image)
y2 = all_feature_values_withPbodies$Pbodies_Count

# use 10x crossvalidation to train optimal classifiers at different values for lambda using LASSO
cvfit2 = cv.glmnet(x2, y2) #, family = 'binomial'

# extract the model error and coefficientsof the optimal classifier
crossValidationErrorAtLambda1se2 = cvfit2$cvm[cvfit$lambda==cvfit$lambda.1se]



ninty_fith_percentil_index = which(a$importance[3,] > 0.95)[1]


# c = select_if(pca_input_data, is.numeric)
# run a multiple linear regression model for P body prediction (how to deal with categoricals?)





# row_sizes = read.csv('/Users/Joel/Dropbox/Pelkmans Lab/Code/PyCharm/DeepLearning/SLP/CellSizes_maxdim.csv', header = TRUE)
# cell_sizes = row_sizes[row_sizes$size_row > 10,]
# hist(cell_sizes$size_row,100)
# sum(cell_sizes$size_row > 640)