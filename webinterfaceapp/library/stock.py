import requests
import json
import numpy as np
from webinterfaceapp.models import StockData
from webinterfaceapp.library.pca_stock import PcaRealTime



class StockMarketApi:
    def api_access(self, url):
        response = requests.get(url)
        result = response.json()
        return result


    def quandlPreprocessing(self, data):
        values = []
        dates = []
        for i in data:
            for j in data[i]:
                if (j == 'data'):

                    for k in data[i][j]:
                        dates.append(k[0])
                        values.append(k[1:5])
        values = np.array(values)
        values = np.flip(values, 0)
        return values, dates


    def alphavantagePreprocessing(self, data):
        values = []
        dates = []
        for i in data:
            # if (i == 'Time Series (Daily)'):
            if (i == 'Time Series (Daily)'):
                for j in data[i]:
                    value = []
                    dates.append(j)
                    for k in data[i][j]:
                        value.append(float(data[i][j][k]))
                    values.append(value)
        values = np.array(values)
        values = np.flip(values, 0)
        return values, dates

    def alphavantageGenericPreprocessing(self, data):
        values = []
        dates = []
        for i in data:
            # if (i == 'Time Series (Daily)'):
            if (i == 'Time Series (15min)'):
                for j in data[i]:
                    value = []
                    dates.append(j)
                    for k in data[i][j]:
                        value.append(float(data[i][j][k]))
                    values.append(value)
        values = np.array(values)
        values = np.flip(values, 0)
        return values, dates


    def model(self, input_matrix, block_size, output_dimension):
        pcaRealTime = PcaRealTime()
        output_matrix, eigen_vectors, eigen_values, dim_array = pcaRealTime.robust_real_time_PCA_target_dimension(
            input_matrix, block_size, output_dimension)
        return dim_array


    def saveResult(self, symbol, input_data, dates, output_data, block_size):
        dates = dates[: -block_size]
        input_data = np.flip(input_data, 0)
        input_data = input_data[: -block_size]
        input_data = np.flip(input_data, 0)
        dates.reverse()
        dictionary = {'1': 'open', '2': 'high', '3': 'low', '4': 'close', '5': 'volume', '6': 'dividend', '7': 'split',
                      '8': 'adj_open', '9': 'adj_high', '10': 'adj_low', '11': 'adj_close', '12': 'adj_volume'}
        dicts = {}
        result = []
        j = 0
        for i in dates:

            # dicts[i] = dictionary[str(output_data[j])]

            index = len(output_data) - 1

            data = StockData()
            data.symbol = symbol
            data.datetime = i
            _dimension1 = dictionary[str(output_data[index])]
            _dimension2 = str(input_data[j, output_data[j] - 1])
            _dim = _dimension1 + " : " + _dimension2
            data.dimension = _dim

            j = j + 1

            result.append(data)

            if(j==100):
                StockData.objects.bulk_create(result)
                result.clear()

        if len(result) != 0:
            StockData.objects.bulk_create(result)

            # data = StockData(symbol=symbol, datetime=i, dimension=dictionary[str(output_data[j])])
            # data.save()
        # with open('alphavantageMSFT.json', 'w') as fp:
        #     json.dump(dicts, fp)

    def alphavantage_api(self, symbol="MSFT"):
        # Your API key is: CVLWNI4QL796D3PJ

        # sym = "MSFT"
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+str(symbol)+"&outputsize=full&apikey=CVLWNI4QL796D3PJ"
        # url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(symbol)+"&interval=15min&apikey=CVLWNI4QL796D3PJ"
        result = self.api_access(url)
        print(len(result))
        input_dimension = 4
        block_size = 5
        output_dimension = 2
        input_data, dates = self.alphavantagePreprocessing(result)
        return input_data, dates, input_dimension, block_size, output_dimension

    def alphavantage15min_api(self, symbol="MSFT"):
        # Your API key is: CVLWNI4QL796D3PJ
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(symbol)+"&interval=15min&apikey=CVLWNI4QL796D3PJ"
        print(url)
        result = self.api_access(url)
        print(len(result))
        input_dimension = 4
        block_size = 5
        output_dimension = 2
        input_data, dates = self.alphavantageGenericPreprocessing(result)
        return input_data, dates, input_dimension, block_size, output_dimension

    def quandl_api(self):
        url = "https://www.quandl.com/api/v3/datasets/EOD/MSFT.json?api_key=AHFizsqmQ15Zyy-ckotr"
        result = self.api_access(url)
        input_dimension = 4
        block_size = 5
        output_dimension = 2
        input_data, dates = self.quandlPreprocessing(result)
        return input_data, dates, input_dimension, block_size, output_dimension

    def get_stock_data(self, symbol="MSFT"):
        # symbol = "MSFT"
        # input_data, dates, input_dimension, block_size, output_dimension = self.alphavantage_api(symbol)
        input_data, dates, input_dimension, block_size, output_dimension = self.alphavantage15min_api(symbol)
        # input_data, dates, input_dimension, block_size, output_dimension = quandl_api()
        output_data = self.model(input_data[:, 0: input_dimension], block_size, output_dimension)

        self.saveResult(symbol, input_data, dates, output_data, block_size)

        return True

#
# if __name__ == "__main__":
#     main()
