import random
import fitness_count
import PROCESS_TIME

def GA(rate_maxspan, rate_setup, rate_tardiness, order_seq):
    weighted_maxspan, weighted_setuptime, weighted_tardiness = rate_maxspan, rate_setup, rate_tardiness
    all_pop_order = []      # 儲存所有族群的排序
    all_pop_fitness = []    # 儲存所有族群排序的適應度值
    best_fit = []           # 儲存每個世代中最佳的適應度值
    best_order = []         # 儲存每個世代中最佳的排序
    
    # 初始解
    for _ in range(1000):
        shuffled_order_seq = random.sample(order_seq, len(order_seq))   # 隨機洗牌排序序列
        maxspan, setuptime, tardiness, sc = fitness_count.fitness(shuffled_order_seq, PROCESS_TIME.PROCESS_TIME)  # 計算適應度值
        overall_fitness = weighted_maxspan * maxspan + weighted_setuptime * setuptime + weighted_tardiness * tardiness  # 計算整體適應度值
        all_pop_order.append(shuffled_order_seq)   # 將排序添加到族群列表中
        all_pop_fitness.append(overall_fitness)    # 將適應度值添加到適應度列表中
    
    for _ in range(100):   # 世代數
        sorted_orders = sorted([(seq, fitness) for (seq, fitness) in zip(all_pop_order, all_pop_fitness)], key=lambda x:x[1])[:2]
        best_order.append(sorted_orders[0][0])   # 將最佳排序添加到最佳排序列表中
        best_fit.append(sorted_orders[0][1])     # 將最佳適應度值添加到最佳適應度值列表中
        all_pop_order = []   # 清空族群列表，為下一個世代做準備
        all_pop_fitness = [] # 清空適應度列表，為下一個世代做準備
        
        for _ in range(100):   # 族群大小
            # 選擇前兩名進行交配
            random_numbers = sorted(random.sample(range(0, len(order_seq)), 2))
            best_mother = sorted_orders[0][0]
            second_mother = sorted_orders[1][0]
            find_segement = best_mother[random_numbers[0]:random_numbers[1]+1]  # 提取片段
            index_second_seg = sorted([second_mother.index(ele) for ele in find_segement])  # 在第二個父代中找到相應的片段
            new_segment = best_mother[0:random_numbers[0]] + [second_mother[index] for index in index_second_seg] + best_mother[random_numbers[1]+1:]  # 生成新片段
            
            # 隨機變異
            rate = 0.5
            if random.random() < rate:
                random_numbers = sorted(random.sample(range(0, len(order_seq)), 2))
                new_segment[random_numbers[0]], new_segment[random_numbers[1]] = new_segment[random_numbers[1]], new_segment[random_numbers[0]]  # 隨機交換兩個元素
            
            maxspan, setuptime, tardiness, sc = fitness_count.fitness(new_segment, PROCESS_TIME.PROCESS_TIME)
            overall_fitness = weighted_maxspan * maxspan + weighted_setuptime * setuptime + weighted_tardiness * tardiness  # 計算整體適應度值
            
            all_pop_order.append(new_segment.copy())     # 將新片段添加到族群列表中
            all_pop_fitness.append(overall_fitness)       # 將適應度值添加到適應度列表中

    return best_order, best_fit, sc