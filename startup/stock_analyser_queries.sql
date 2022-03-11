use ticks;
Select count(*) from ticker_info where symbol='HAVELLS.NS';
-- Altering the ticker_info table
alter table ticker_info add sentiment varchar(10) DEFAULT NULL;
alter table ticker_info add sentiment_perc FLOAT DEFAULT NULL;

Insert into ticker_info (sector, fullTimeEmployees, city, operatingCashflow, revenueGrowth, operatingMargins, ebitda, targetLowPrice, targetMeanPrice, targetHighPrice, recommendationKey, recommendationMean, grossProfits, freeCashflow, targetMedianPrice, currentPrice, earningsGrowth, currentRatio, returnOnAssets, debtToEquity, returnOnEquity, totalCash, totalDebt, totalRevenue, totalCashPerShare, financialCurrency, revenuePerShare, quickRatio, exchange, shortName, longName, exchangeTimezoneName, exchangeTimezoneShortName, quoteType, symbol, annualHoldingsTurnover, enterpriseToRevenue, beta3Year, enterpriseToEbitda, 52WeekChange, morningStarRiskRating, forwardEps, revenueQuarterlyGrowth, sharesOutstanding, annualReportExpenseRatio, totalAssets, bookValue, shareShort, sharesPercentSharesOut, heldPercentInstitutions, netIncomeToCommon, trailingEps, lastDividendValue, SandP52WeekChange, priceToBook, heldPercentInsiders, yield, mostRecentQuarter, shortRatio, sharesShortPreviousMonthDate, floatShares, beta, enterpriseValue, priceHint, threeYearAverageReturn, lastSplitDate, lastSplitFactor, legalType, lastDividendDate, morningStarOverallRating, earningsQuarterlyGrowth, priceToSalesTrailing12Months, dateShortInterest, pegRatio, ytdReturn, forwardPE, lastCapGain, shortPercentOfFloat, sharesShortPriorMonth, impliedSharesOutstanding, category, fiveYearAverageReturn, previousClose, regularMarketOpen, twoHundredDayAverage, trailingAnnualDividendYield, payoutRatio, volume24Hr, regularMarketDayHigh, navPrice, averageDailyVolume10Day, regularMarketPreviousClose, fiftyDayAverage, trailingAnnualDividendRate, open, toCurrency, averageVolume10days, expireDate, algorithm, dividendRate, exDividendDate, circulatingSupply, startDate, regularMarketDayLow, currency, trailingPE, regularMarketVolume, lastMarket, maxSupply, openInterest, marketCap, volumeAllCurrencies, strikePrice, averageVolume, dayLow, ask, askSize, volume, fiftyTwoWeekHigh, fromCurrency, fiveYearAvgDividendYield, fiftyTwoWeekLow, bid, tradeable, dividendYield, bidSize, dayHigh, regularMarketPrice, preMarketPrice, logo_url, currentDate) VALUES ('Industrials', 5727, 'Noida', 13137500160, 0.317, 0.1267, 17772400640, 804, 1348.26, 1650, 'hold', 2.7, 39098200000, 6770212352, 1391.5, 1392.7, -0.073, 1.876, 0.10965, 10.441, 0.23295, 25625899008, 5768999936, 123624202240, 40.932, 'INR', 197.488, 0.974, 'NSI', 'HAVELLS INDIA', 'Havells India Limited', 'Asia/Kolkata', 'IST', 'EQUITY', 'HAVELLS.NS', NULL, 6.875, NULL, 47.82, 0.66907287, NULL, 23.56, NULL, 626302976, NULL, NULL, 88.253, NULL, NULL, 0.19502, 11921399808, 19.042, 3, 0.3175944, 15.7807665, 0.64893997, NULL, 1632960000, NULL, NULL, 216631445, 0.651388, 849874321408, 2, NULL, 1409011200, '5:1', NULL, 1635292800, NULL, -0.073, 7.0556746, NULL, 5.34, NULL, 59.112904, NULL, NULL, NULL, NULL, NULL, NULL, 1398.85, 1400, 1200.738, 0.0046466743, 0.3414, NULL, 1400, NULL, 850143, 1398.85, 1354.3917, 6.5, 1400, NULL, 850143, NULL, NULL, 6.5, 1635292800, NULL, NULL, 1380.85, 'INR', 73.13832, 151464, NULL, NULL, NULL, 872252112896, NULL, NULL, 1514460, 1380.85, 1393.55, 0, 151464, 1504.45, NULL, 0.69, 796, 1391.95, False, 0.0047, 0, 1400, 1392.7, NULL, 'https://logo.clearbit.com/havells.com', CURDATE());
select * from ticker_info where sector is not null;
select count(*) from ticker_info;
select * from ticker_info where symbol = "BURGERKING.NS" order by date_of_trade desc;
select count(*) from ticker_info where symbol = "BURGERKING.NS";
select * from ticker_info where sector is not null;
select * from ticker_info where date_of_trade>'2021-12-05';

update ticker_info set date_of_trade='2021-12-28' where DATE(date_of_trade)='2021-12-29';
select * from split_info where split_ratio != 0.0;
select * from dividend_info;
select * from ticker_info where symbol="JSWSTEEL.NS";
desc ticker_info;

select count(*) from ticker_info where symbol="IRCTC.NS";
select symbol,date_of_trade,sentiment from ticker_info;
update ticker_info set sentiment = "pos" where symbol="IRCTC.NS" and date_of_trade = "2019-10-14 00:00:00";
select symbol,date_of_trade,sentiment from ticker_info where symbol = "INFY.NS" and sentiment is not null;

delete from ticker_info where symbol="LATENTVIEW.NS" and date_of_trade < "2022-01-11";
delete from ticker_info where symbol="LATENTVIEW.NS";

-- Finding Primary Key if a Table
select COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ticks'
AND TABLE_NAME = 'ticker_info' and COLUMN_KEY = 'PRI';

desc dividend_info;

