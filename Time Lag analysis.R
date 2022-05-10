install.packages("readxl")
library("readxl")
data=read_excel("TimeSeries for Tokens.xlsx")

par(mfrow=c(2,1))
plot(data$BTC_Growth,type="l",col="red")
plot(data$ETH_Growth,type="l",col="red")



### initial analysis on time lag. There is lag relationship but not clear
par(mfrow=c(3,2))
ccf(data$BTC_Growth,data$ETH_Growth,lag.max=5,main="BTC V.S. ETH")

###find out the distribution of %change----for further CI calculation
hist(data$BTC_Growth)
hist(data$ETH_Growth)

data2=read_excel("TimeSeries for Tokens.xlsx")
###calculate the quantile for each coin and set the data to 0 in this area, then we find out the process
###made the pattern clearer.
quantile(data2$BTC_Growth,c(0.05,0.95))
data2$BTC_Growth[data2$BTC_Growth<0.001833917  & data2$BTC_Growth>-0.001806681]=0

quantile(data2$ETH_Growth,c(0.05,0.95))
data2$ETH_Growth[data2$ETH_Growth<0.002341254  & data2$ETH_Growth>-0.002304487]=0

ccf(data2$BTC_Growth,data2$ETH_Growth,lag.max=5,main="BTC V.S. ETH")
value=ccf(data2$BTC_Growth,data2$ETH_Growth,lag.max=5,main="BTC V.S. ETH")
value


par(mfrow=c(3,2))
ccf(data2$BTC_Growth,data2$ETH_Growth,lag.max=5,main="BTC V.S. ETH")

write.csv(x = data2,file = "Modified %change2.csv")

par(mfrow=c(2,1))
plot(data2$BTC_Growth,type="l",col="red")
plot(data2$ETH_Growth,type="l",col="red")
