from datetime import date, timedelta
import pandas as pd

def fitness(order_seq, PROCESS_TIME):
    # 初始化資料
    job = []
    start_time = []
    finish_time = []
    resource = []
    machine_state_ABC = {'A':0, 'B':0, 'C':0} # ABC機台狀況
    machine_state_D = 0 # D機台狀況
    machine_time_ABC = {'A':0, 'B':0, 'C':0} # ABC機台時間
    machine_time_D = 0  # D機台時間
    all_setup_time = 0 # 時間紀錄 
    all_tardiness_time = 0
    previous = None # 前一單產品類型
    today = date.today()
    today_timestamp = pd.Timestamp(today)
    
    for order in order_seq:
        wo_id = order.wo_id
        wo_type = order.wo_type
        machine = order.machine
        num_fill = order.num_fill
        num_sticker = order.num_sticker
        due = order.due
        # 計算填充時間跟貼標時間
        fill_time = round(num_fill * PROCESS_TIME[(machine, wo_type)][0],0)
        stick_time = round(num_sticker * PROCESS_TIME[(machine, wo_type)][1],0)
        setup_time = 20 * 60
        if previous == wo_type: # 若前一單與本單類型同，整備時間僅為5分鐘
            setup_time = 5*60
        all_setup_time += setup_time
        total_process_time = fill_time + stick_time + setup_time
        # print(f'排入工單編號:{wo_id}, 產線:{machine}, 產品類型:{wo_type}, 填充時間{fill_time}, 貼標時間:{stick_time}, 整備時間:{setup_time}, 總加工時間:{total_process_time}, DUE:{str(due)[:10]}')

        order_start_time = 0
        order_finish_time = 0

        if machine in ['A', 'B', 'C']:
            if sum(machine_state_ABC.values()) == 0: # 假如前一單是D排單
                order_start_time = machine_time_D # 開始時間為D佔用的最後時間
                order_finish_time = order_start_time + total_process_time # 加上本單作業時間
                machine_state_D = 0 # 釋放D機台
                machine_time_ABC[machine] = order_finish_time # 本單佔用機台最後時間
                machine_state_ABC[machine] = 1 # 更新佔用某機台
                # print(f'前單為D機台或此單為首單')

            elif sum(machine_state_ABC.values()) == 1: # 假如已有一台ABC機群運作，要判斷是否沿用同台或換台了
                previous_machine = ([current_machine for (current_machine, state) in machine_state_ABC.items() if state == 1])[0]
                if machine == previous_machine:
                    order_start_time = machine_time_ABC[machine]
                    order_finish_time = order_start_time + total_process_time
                    machine_time_ABC[machine] = order_finish_time # 本單佔用機台最後時間
                    # print('沿用同台，持續佔用')
                else:
                    order_start_time = machine_time_D # 開始時間為D佔用的最後時間
                    order_finish_time = order_start_time + total_process_time # 加上本單作業時間
                    machine_state_D = 0 # 釋放D機台
                    machine_time_ABC[machine] = order_finish_time # 本單佔用機台最後時間
                    machine_state_ABC[machine] = 1 # 更新佔用某機台
                    # print(f'插入非上一單機台')
            else :
                previous_machine = ([current_machine for (current_machine, state) in machine_state_ABC.items() if state == 1])
                if machine in previous_machine:
                    order_start_time = machine_time_ABC[machine]
                    order_finish_time = order_start_time + total_process_time
                    machine_time_ABC[machine] = order_finish_time # 本單佔用機台最後時間
                    # print('沿用同台，持續佔用')
                else:
                    ABC_list = [(pre_machine, time) for ((pre_machine,state), time) in (zip(machine_state_ABC.items(), machine_time_ABC.values())) if state == 1] # 找ABC佔用的情況跟最後時間
                    min_element = min(ABC_list, key=lambda x: x[1])
                    order_start_time = min_element[1] # 開始時間為D佔用的最後時間
                    order_finish_time = order_start_time + total_process_time # 加上本單作業時間
                    machine_state_ABC[min_element[0]] = 0 # 釋放D機台
                    machine_time_ABC[machine] = order_finish_time # 本單佔用機台最後時間
                    machine_state_ABC[machine] = 1 # 更新佔用某機台
                    # print(f'此單ABC機台已被佔用，需等待至佔用機台最早結束時間')
        else:
            if machine_state_D == 1:
                order_start_time = machine_time_D
                machine_time_D += total_process_time # 本單佔用機台最後時間
                order_finish_time = machine_time_D
                # print(f'繼續使用D機台')
            elif sum(machine_state_ABC.values()) > 0:
                ABC_list = [(pre_machine, time) for ((pre_machine,state), time) in (zip(machine_state_ABC.items(), machine_time_ABC.values())) if state == 1] # 找ABC佔用的情況跟最後時間
                min_element = max(ABC_list, key=lambda x: x[1])
                order_start_time = min_element[1] # 開始時間為佔用機台的最大時間
                order_finish_time = order_start_time + total_process_time # 加上本單作業時間
                for history in ABC_list:
                    machine_state_ABC[history[0]] = 0
                machine_time_D = order_finish_time # 本單佔用機台最後時間
                machine_state_D = 1 # 更新佔用某機台
                # print(f'此單前ABC機台已被佔用，需等待佔用機台結束後才可開工')
            else:
                order_start_time = machine_time_D
                machine_time_D = total_process_time # 本單佔用機台最後時間
                machine_state_D = 1 # 更新佔用某機台
                order_finish_time = machine_time_D
                # print(f'此單為首單')

        previous = wo_type
        finish_date = int(order_finish_time/(3600*24)) 
        tardiness = max((today_timestamp + timedelta(days=finish_date) - due).days,0)
        all_tardiness_time += tardiness
        # print(f'【真實】開始時間為{today_timestamp + timedelta(seconds=order_start_time)}，結束時間:{today_timestamp + timedelta(seconds=order_finish_time)}')
        # print(f'【時間戳記】開始時間: {int(order_start_time)}, 結束時間:{int(order_finish_time)}, 完工日期:{str(today_timestamp + timedelta(days=finish_date))[:10]}')
        # print(f'A:{machine_state_ABC["A"]}, B:{machine_state_ABC["B"]}, C:{machine_state_ABC["C"]}, D:{machine_state_D}')
        # print(f'A:{machine_time_ABC["A"]}, B:{machine_time_ABC["B"]}, C:{machine_time_ABC["C"]}, D:{machine_time_D}')

        job.append(wo_id)
        start_time.append(today_timestamp + timedelta(seconds=order_start_time))
        finish_time.append(today_timestamp + timedelta(seconds=order_finish_time))
        resource.append(machine)
        # print('------------------------------------------------------------------------------------------------------------------------------------------')

    max_ABC = max(machine_time_ABC.items(), key=lambda x: x[1])[1]
    maxspan = max_ABC
    if max_ABC < machine_time_D:
        maxspan = machine_time_D
    schedule = pd.DataFrame({"工單編號":job, "Start":start_time, "Finish":finish_time, "產線":resource})
    return maxspan, all_setup_time, all_tardiness_time*3600*24, schedule