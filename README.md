# 瑕疵檢測模組

## 檔案目錄
|folder |file or Package           |file                  |Memo|
|-------|--------------------------|----------------------|----|
|root   |enter.py                  |                      |入口|
|config |Config.py                 |                      |基本任務參數設定|
|       |ConfigPytorchModel.py     |                      |模型參數選擇及設定|
|       |ConfigAugmentation.py     |                      |資料擴增方法選擇及設定|
|       |ConfigDataClean.py        |                      |資料清理參數設定|
|       |ConfigEvaluation.py       |                      |相關評估方法選擇|
|       |ConfigModelService.py     |                      |模型讀檔、優化器、損失函數等模型周邊服務選擇及設定|
|       |ConfigModule.py           |                      |其他額外功能模組選擇及設定，尚未開發，不影響主流程進行|
|       |ConfigPostprocess.py      |                      |後處理參數設定|
|       |ConfigPreprocess.py       |                      |前處理參數設定|
|       |ConfigResultStorage.py    |                      |結果輸出方法選擇及設定|
|input  |Data                      |                      |影像資料放置區|
|       |PretrainedWight           |                      |預訓練權重放置區|
|main   |Main.py                   |                      |定義整體流程|
|output |                          |                      |存放訓練完全權重及各式結果|
|utils  |DataAugmentation          |                      |資料擴增模組|
|       |DatasetClean              |                      |資料清理模組，尚未完整併入主流程中|
|       |Evaluation                |                      |相關評估方法模組|
|       |ModelService              |                      |優化器、損失函數等模型周邊服務模組|
|       |AiModel                   |                      |模型架構模組|
|       |Others                    |                      |其他額外功能模組|
|       |Postprocess               |                      |後處理模組|
|       |Preprocess                |                      |前處理模組|
|       |ResultStorage             |                      |結果輸出方法模組|


## Edit server
39394
