import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import fitness_count 
import GA
import PROCESS_TIME

# 工單物件化
class ORDER():
    def __init__(self, wo_id, wo_type, machine, num_fill, num_sticker, due):
        self.wo_id = wo_id
        self.wo_type = wo_type
        self.machine = machine
        self.num_fill = num_fill
        self.num_sticker = num_sticker
        self.due = due

# 讀取工單
wo = pd.read_excel('WIP.xlsx')


order_seq = []

for row in range(len(wo)):
    wo_id = wo.iloc[row]['工單編號']
    wo_type = wo.iloc[row]['產品類型']
    machine = wo.iloc[row]['產線']
    num_fill = wo.iloc[row]['填充需求數量']
    num_sticker = wo.iloc[row]['貼標需求數量']
    due = wo.iloc[row]['交期']
    order = ORDER(wo_id, wo_type, machine, num_fill, num_sticker, due)
    order_seq.append(order)

a,b,c,d = fitness_count.fitness(order_seq, PROCESS_TIME.PROCESS_TIME)
print(f'原始排序：maxspan:{a}, setup_total:{b}, tardiness_total:{c}')

order_result, fitness_result, sc = GA.GA(1,0,0, order_seq) # 只看maxspan最大的方法，可調整參數看不同情境下的結果
maxspan, setuptime, tardiness, sc = fitness_count.fitness(order_result[-1], PROCESS_TIME.PROCESS_TIME) # 印出最後一代的結果
sc["Start"] = pd.to_datetime(sc["Start"])
sc["Finish"] = pd.to_datetime(sc["Finish"])
df = sc.sort_values(by="產線", ascending=False)

fig = px.timeline(df, 
                  x_start="Start", 
                  x_end="Finish", 
                  y="產線", 
                  color="工單編號", 
                  title="Gantt Chart - by 機台")

fig.show()
df = pd.merge(sc, wo, on='工單編號').drop(columns=['產線_y'])
df['遲繳'] =  df['Finish'] - df['交期'] 
print(df)

plt.plot(fitness_result)
plt.xlabel('Iteration')
plt.ylabel('Fitness')
plt.title('The decreasing trend of fitness in each iteration')

