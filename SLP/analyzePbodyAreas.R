# Analyze relative P body area

sizes = read.csv('/Users/Joel/shares/dataShareJoel/jluethi/20180503-SubcellularLocalizationMultiplexing/Pbody_Sizes.csv', header = TRUE)
mean(sizes$PercentagePbody)
sum(as.numeric(sizes$PbodyArea), na.rm = TRUE)/sum(as.numeric(sizes$TotalArea), na.rm = TRUE)
sum(as.numeric(sizes$BackgroundArea), na.rm = TRUE)/sum(as.numeric(sizes$TotalArea), na.rm = TRUE)


