# 多目標基因算法實作

分享簡易多目標GA算法的實作，多目標採用權重來分配各項目標的重要性。
多目標GA的優勢在於可以根據不同情境進行排程情境的調換，以本題為例，多目標GA可在最小化完工時間、最小化整備時間與最小化延遲時間中取得平衡。

本題情境如下
*  WIP包含工單編號、產品類型、產線、填充數量、貼標數量與交期
*  其中只有D產線需要貼標的加工程序
*  ABC機台可同時選用兩台加工或D機台獨立運作，兩種情境二選一
*  一天工時為8小時

機台產能情況如下
| 機台 (Machine) | 產品類型 (Type) | 填充產能 (箱/hr) | 貼標產能 (箱/hr) |
| :------------- | :-------------- | :---------------- | :---------------- |
| A              | 330             | 500               | 0                 |
| A              | 310             | 200               | 0                 |
| A              | 380             | 300               | 0                 |
| A              | 500             | 500               | 0                 |
| A              | 600             | 500               | 0                 |
| B              | 6000            | 180               | 0                 |
| B              | 20000           | 144               | 0                 |
| B              | 17250           | 336               | 0                 |
| C              | 240             | 168               | 0                 |
| D              | 330             | 500               | 40                |
| D              | 380             | 300               | 40                |
| D              | 500             | 500               | 250               |

工單內容如下
工單編號 | 產品類型 | 產線 | 填充需求數量 | 貼標需求數量 | 交期      
-------- | -------- | ---- | ------------ | ------------ | -----------
1        | 20000    | B    | 3132         | 0            | 2023/6/22 
2        | 240      | C    | 3268         | 0            | 2023/8/5  
3        | 330      | D    | 4557         | 8175         | 2023/6/22 
4        | 17250    | B    | 3644         | 0            | 2023/7/17 
5        | 240      | C    | 3870         | 0            | 2023/7/28 
6        | 500      | A    | 4088         | 0            | 2023/7/2  
7        | 17250    | B    | 4247         | 0            | 2023/7/24 
8        | 500      | D    | 4510         | 7856         | 2023/7/17 

