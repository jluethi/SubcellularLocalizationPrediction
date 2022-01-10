# Analyze single pixel correlation for 60x SLP experiment
all_correlations = data.frame()
# combinations = c('3_APPL_5_pS6.csv', '3_APPL_7_Actin.csv', '3_APPL_11_Sara.csv', '3_APPL_13_DDX6.csv', '5_pS6_7_Actin.csv', '5_pS6_11_Sara.csv', '5_pS6_13_DDX6.csv', '7_Actin_11_Sara.csv', '7_Actin_13_DDX6.csv', '11_Sara_13_DDX6.csv')
# combination_name = c('Actin_3_5', 'Actin_3_7', 'Actin_3_11', 'Actin_3_13', 'Actin_5_7', 'Actin_5_11', 'Actin_5_13', 'Actin_7_11', 'Actin_7_13', 'Actin_11_13')
# combinations = c('3_GM130_5_Yap.csv', '3_GM130_11_EEA1.csv', '3_GM130_13_DCP1a.csv','5_Yap_11_EEA1.csv', '5_Yap_13_DCP1a.csv', '11_EEA1_13_DCP1a.csv')
# combination_name = c('NUP_3_5', 'NUP_3_11', 'NUP_3_13', 'NUP_5_11', 'NUP_5_13', 'NUP_11_13')
# combinations = c('2_Calreticulin_8_Caveolin.csv', '2_Calreticulin_10_Pericentrin.csv', '8_Caveolin_10_Pericentrin.csv')
# combination_name = c('Fibrillarin_2_8', 'Fibrillarin_2_10', 'Fibrillarin_8_10')
# combinations = c('n2_EEA1_8_Pol2.csv', 'n2_EEA1_10_Paxillin.csv', '8_Pol2_10_Paxillin.csv')
# combination_name = c('bCatenin_2_8', 'bCatenin_2_10', 'bCatenin_8_10')
# combinations = c('2_Calreticulin_3_APPL.csv', '2_Calreticulin_3_GM130.csv', '2_Calreticulin_n2_EEA1.csv', '3_APPL_3_GM130.csv', 'n2_EEA1_3_APPL.csv', 'n2_EEA1_3_GM130.csv')
# combination_name = c('Fibrillarin_Actin', 'Fibrillarin_NUP', 'Fibrillarin_bCatenin', 'Actin_NUP', 'bCatenin_Actin', 'bCatenin_NUP')
combinations = c('3_APPL_13_DDX6.csv', '3_GM130_13_DCP1a.csv', '2_Calreticulin_10_Pericentrin.csv', 'n2_EEA1_10_Paxillin.csv', '2_Calreticulin_n2_EEA1.csv')
combination_name = c('Actin_3_13', 'NUP_3_13', 'Fibrillarin_2_10', 'bCatenin_2_10', 'Fibrillarin_bCatenin')

# Load data
for (i in 1:length(combinations)){
  filename = paste0('/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/singlePixelCorrelations/SinglePixelCorrelation_', combinations[i])
  correlations = read.csv(filename, stringsAsFactors = FALSE)
  correlations$Comparison = combination_name[i]
  
  # Make columns correct data format
  correlations$Comparison = as.factor(correlations$Comparison)
  correlations$PearsonR = as.numeric(correlations$PearsonR)
  
  # Remove NaNs
  correlations = correlations[!is.na(correlations$PearsonR),]
  
  # Append to data frame
  all_correlations = rbind(all_correlations, correlations)
}

all_correlations$SiteInfo = paste0(all_correlations$Well, '_', all_correlations$Site_x, all_correlations$Site_y)

# Plot correlation colored by site
library(ggplot2)
ggplot(all_correlations, aes(x = Comparison, y = PearsonR)) + 
  geom_boxplot() +
  ylim(c(-1,1))

# ggplot(correlations, aes(x = Comparison, y = PearsonR, color = SiteInfo)) + 
#   geom_point(position = "jitter")

correlations$PearsonR[1] + correlations$PearsonR[2]
mean(correlations$PearsonR)
correlations$PearsonR[1]
