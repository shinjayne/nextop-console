from . import models

import json
import numpy as np
import tensorflow as tf
import pandas as pd
from fbprophet import Prophet
from datetime import datetime

tf.set_random_seed(77)

mockForecastDictionary = {}
realForecastDictionary = {}






def LearningModuleRunner(task, forecastDay = 30):

    # task.data.path -> file path string

    decoded = json.loads(task.data)
    rawArrayDatas = [decoded["Date"], decoded["Data"]]  
    processId = task.id

    # TODO make dayOrWeekOrMonth parameter
    #     dayOrWeekOrMonth=dayOrWeekOrMonth
    dayOrWeekOrMonth = 'week'
    # options:
    # 'day', 'week', 'month
    feature = 'DayOfWeek_WeekNumber_Month_Season'

    # options:
    # dayOrWeekOrMonth='day': 'DayOfWeek_WeekNumber_Month_Season','DayOfWeek01_WeekNumber_Month_Season'//
    # dayOrWeekOrMonth='week': 'WeekNumber_Month_Season_Year'

    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "start of learning #" + str(processId),
     #                              DefineManager.LOG_LEVEL_INFO)


    # mock
    global mockForecastDictionary
    global realForecastDictionary
    mockForcastDay = forecastDay

    ##Make txsForRealForecastLstm   [:]
    ds = rawArrayDatas[0]   #Date -> ds
    y = list(np.sqrt(rawArrayDatas[1]))  #Data -> y
    sales = list(zip(ds, y)) # Combined Date and Data
    txsForRealForecastLstm = pd.DataFrame(data=sales, columns=['ds', 'y']) # make dataframe with date(ds) data(y)
    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "txsForRealForecastLstm create success",
     #                              DefineManager.LOG_LEVEL_INFO)
    ##Make txsForMockForecastLstm [:-forecastDay]
    ds = rawArrayDatas[0][:-forecastDay]  #input 인 day 만큼을 마지막에서 제외한 Date
    y = list(np.sqrt(rawArrayDatas[1][:-forecastDay]))  #input 인 day 만큼을 마지막에서 제외한 Data
    sales = list(zip(ds, y))
    txsForMockForecastLstm = pd.DataFrame(data=sales, columns=['ds', 'y'])
    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "txsForMockForecastLstm create success",
    #                               DefineManager.LOG_LEVEL_INFO)
    ##Make txsForRealForecastBayesian [:-forecastDay] & np.log
    ds = rawArrayDatas[0][:-forecastDay]
    # TODO bayseian에 대해서는 input값이 0인 상황처리 필요
    y = list(np.log(rawArrayDatas[1][:-forecastDay]))
    sales = list(zip(ds, y))
    txsForRealForecastBayesian = pd.DataFrame(data=sales, columns=['ds', 'y'])
    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner",
     #                              "txsForRealForecastBayesian create success",
      #                             DefineManager.LOG_LEVEL_INFO)
    ##Make txsForMockForecastBayseian   [:-(mockForcastDay+forecastDay)] & np.log
    ds = rawArrayDatas[0][:-(mockForcastDay + forecastDay)]
    # TODO bayseian에 대해서는 input값이 0인 상황처리 필요
    y = list(np.log(rawArrayDatas[1][:-(mockForcastDay + forecastDay)]))
    sales = list(zip(ds, y))
    txsForMockForecastBayseian = pd.DataFrame(data=sales, columns=['ds', 'y'])
    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner",
    #                               "txsForMockForecastBayseian create success",
    #                               DefineManager.LOG_LEVEL_INFO)

    # testY for algorithm compare has size of (mockForcastDay+forecastDay)  rawArrayDatas[1][-(mockForcastDay+forecastDay):-forecastDay]
    testY = rawArrayDatas[1][-(mockForcastDay + forecastDay):-forecastDay]
    ###############
    # ????????????? 윗부분 !
    ###############

    # realForecastDictionary['LSTM'] = LSTM(txsForRealForecastLstm, forecastDay, feature)
    if dayOrWeekOrMonth is 'day':

        # select feature module
        feature = 'DayOfWeek_WeekNumber_Month_Season'

        mockForecastDictionary['LSTM'] = LSTM(txsForMockForecastLstm, mockForcastDay, feature)

        ####Bayseian_day

        mockForecastDictionary['Bayseian'] = Bayseian(txsForMockForecastBayseian, mockForcastDay, 'day')
        #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "mockForecastBayseian success",
        #                               DefineManager.LOG_LEVEL_INFO)

        # 알고리즘 비교
        nameOfBestAlgorithm = AlgorithmCompare(testY)
        ####더 좋은 알고리즘 호출
        if nameOfBestAlgorithm is 'LSTM':
            tf.reset_default_graph()
            realForecastDictionary['LSTM'] = LSTM(txsForRealForecastLstm, forecastDay, feature)
         #   LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "LSTMrealForecast success",
          #                                 DefineManager.LOG_LEVEL_INFO)
        elif nameOfBestAlgorithm is 'Bayseian':
            realForecastDictionary['Bayseian'] = Bayseian(txsForRealForecastBayesian, forecastDay, 'day')


    elif dayOrWeekOrMonth is 'week':

        ####LSTM_week

        # select feature module
        feature = 'WeekNumber_Month_Season_Year'

        mockForecastDictionary['LSTM'] = LSTM(txsForMockForecastLstm, mockForcastDay, feature)
        #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "mockForecastLstm success",
        #                               DefineManager.LOG_LEVEL_INFO)

        ####Bayseian_week

        mockForecastDictionary['Bayseian'] = Bayseian(txsForMockForecastBayseian, mockForcastDay, 'week')
        #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "mockForecastBayseian success",
        #                               DefineManager.LOG_LEVEL_INFO)

        # 알고리즘 비교
        nameOfBestAlgorithm = AlgorithmCompare(testY)
        ####더 좋은 알고리즘 호출
        if nameOfBestAlgorithm is 'LSTM':
            tf.reset_default_graph()
            realForecastDictionary['LSTM'] = LSTM(txsForRealForecastLstm, forecastDay, feature)
        #    LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "LSTMrealForecast success",
        #                                   DefineManager.LOG_LEVEL_INFO)
        elif nameOfBestAlgorithm is 'Bayseian':

            realForecastDictionary['Bayseian'] = Bayseian(txsForRealForecastBayesian, forecastDay, 'week')
        #    LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "BayesianrealForecast success",
        #                                   DefineManager.LOG_LEVEL_INFO)

    elif dayOrWeekOrMonth is 'month':

        ####LSTM_month

        # select feature module
        feature = 'WeekNumber_Month_Season_Year'

        mockForecastDictionary['LSTM'] = LSTM(txsForMockForecastLstm, mockForcastDay, feature)

        ####Bayseian_month

        mockForecastDictionary['Bayseian'] = Bayseian(txsForMockForecastBayseian, mockForcastDay, 'month')

        # 알고리즘 비교
        nameOfBestAlgorithm = AlgorithmCompare(testY)
        ####더 좋은 알고리즘 호출
        if nameOfBestAlgorithm is 'LSTM':
            tf.reset_default_graph()
            realForecastDictionary['LSTM'] = LSTM(txsForRealForecastLstm, forecastDay, feature)

        elif nameOfBestAlgorithm is 'Bayseian':
            realForecastDictionary['Bayseian'] = Bayseian(txsForRealForecastBayesian, forecastDay, 'month')

            ####################################################################################BAYSEIAN
    # tf.reset_default_graph()

    data = rawArrayDatas[1][:-forecastDay] + realForecastDictionary[nameOfBestAlgorithm]
    date = rawArrayDatas[0]
    #LoggingManager.PrintLogMessage("LearningManager", "LearningModuleRunner", "FirebaseUploadPrepare ",
    #                               DefineManager.LOG_LEVEL_INFO)
    #FirebaseDatabaseManager.StoreOutputData(processId, resultArrayData=data, resultArrayDate=date,
    #                                        status=DefineManager.ALGORITHM_STATUS_DONE)
    result = {"Data":data, "Date":date}
    task.result = json.dumps(result)
    task.save()
    return 0




# TODO : 엘에스티엠 개선


def Bayseian(txs, forecastDay, unit):
    global mockForecastDictionary
    global realForecastDictionary

    if unit is 'day':
        if (len(txs) < 366):
            model = Prophet()
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay)
            forecastProphetTable = model.predict(future)

        else:
            model = Prophet(yearly_seasonality=True)
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay)
            forecastProphetTable = model.predict(future)


    elif unit is 'week':
        if (len(txs) < 53):
            model = Prophet()
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay, freq='w')
            forecastProphetTable = model.predict(future)

        else:
            model = Prophet(yearly_seasonality=True)
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay, freq='w')
            forecastProphetTable = model.predict(future)

    elif unit is 'month':
        if (len(txs) < 12):
            model = Prophet()
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay, freq='m')
            forecastProphetTable = model.predict(future)

        else:
            model = Prophet(yearly_seasonality=True)
            model.fit(txs)
            future = model.make_future_dataframe(periods=forecastDay, freq='m')
            forecastProphetTable = model.predict(future)

    # date = [d.strftime('%Y-%m-%d') for d in forecastProphetTable['ds']]
    return [np.exp(y) for y in forecastProphetTable['yhat'][-forecastDay:]]

# TODO : 페이스북 라이브러리 조절 파라메터 도큐멘 공부해서 성능 높이기


###  TODO : 알고리즘 갯수 늘린다
# TODO : 파라메터 늘린다










def AlgorithmCompare(testY):
    global mockForecastDictionary
    nameOfBestAlgorithm = 'LSTM'
    minData = rmse(testY, mockForecastDictionary[nameOfBestAlgorithm])
    rms = 0
    for algorithm in mockForecastDictionary.keys():
        rms = rmse(testY, mockForecastDictionary[algorithm])
        if rms < minData:
            nameOfBestAlgorithm = algorithm
    print('testY is: ', testY)
    print('\n')
    print('LSTM forecast :', mockForecastDictionary['LSTM'], '\n@@@@@LSTM rmse: ',
          rmse(testY, mockForecastDictionary['LSTM']))
    print('Bayseian forecast :', mockForecastDictionary['Bayseian'], '\n@@@@@Bayseian rmse: ',
          rmse(testY, mockForecastDictionary['Bayseian']))
    print('\n')
    print(nameOfBestAlgorithm, 'WON!!!!!!')
    return nameOfBestAlgorithm



