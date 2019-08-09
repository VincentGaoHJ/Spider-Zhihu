# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author : strangestring
# github : https://github.com/strangestring
# mailbox: 1814232115@qq.com


import time
import copy


count_time = 0
sort_time = 0
append_time = 0
start_time = time.perf_counter()


def load_balance(fetch_dict: list, func, work_flow_num: int, flood_discharge_ratio: float = 0.3,
                 floodplain_ratio: float = 0.1):
    """
    :param fetch_dict: 请求内容
    :param func: 传入的函数
    :param work_flow_num: 需要分配的work_flow总数
    :param flood_discharge_ratio: 允许少许溢出时,单次最大增幅占floodplain_size的比例
    :param floodplain_ratio: 允许少许溢出work_flow任务量占work_flow_capacity的比例
    :return:
    """
    if 'limit' in func.__code__.co_varnames:
        # url_token/answer_id是必须参数,因此减一
        func_limit = func.__defaults__[func.__code__.co_varnames.index('limit') - 1]
    else:
        func_limit = 1
        ...
    task_total_count = 0
    count_time_a = time.perf_counter()
    for task in fetch_dict:
        if 'range' in task.keys():
            task_range = task['range']
            step = limit = func_limit
            if len(task_range) == 2:
                pass
            elif len(task_range) == 3:
                step = task_range[2]
            else:
                step, limit = task_range[2:]
                ...
            # start and end
            assert 0 <= task_range[0] < task_range[
                1], f'\n\nStart and end must satisfy 0 <= start < end in task:\n{task}\nPlease check start and end.'
            # limit and step
            assert 0 < limit <= step, f'\n\nLimit and step must satisfy 0 < limit <= step in task:\n{task}\nPlease check limit and step.'
            span = task_range[1] - task_range[0]
            task_count = span // step * limit + min(limit, span % step)
            # for unexpected occasions
            assert task_count > 0, f'\n\nTask_count <= 0 in task:\n{task}\nPlease check start,end[,step[,limit]].'
        else:
            task_count = 1
            ...
        task['task_count'] = task_count
        task_total_count += task_count
        ...
    count_time_b = time.perf_counter()
    global count_time
    count_time += count_time_b - count_time_a
    # 以上task_count耗时3%以下
    
    if work_flow_num == 1:  # 效率提升显著
        return {'task_count': task_total_count, 'task_pool': fetch_dict}  # '_gather_result()'通过task_count判断
    
    work_flow_capacity = task_total_count // work_flow_num  # type:float
    work_flow_task_count = [0 for x in range(work_flow_num)]  # type:list
    work_flows = [{'task_count': 0, 'task_pool': []} for x in range(work_flow_num)]  # type:list
    # print(work_flows)
    # print(f'work_flow_capacity\t{work_flow_capacity}')
    
    min_flood_discharge = 1 if floodplain_ratio > 0 else 0  # 有缓冲区时的最小洪峰
    floodplain_size = max(0, int(min(1, floodplain_ratio) * work_flow_capacity))
    flood_discharge = max(min_flood_discharge, int(min(1, flood_discharge_ratio) * floodplain_size))
    # print(f'floodplain_size\t\t{floodplain_size}')
    # print(f'flood_discharge\t\t{flood_discharge}')
    
    sort_count = 0
    loop_count = 0
    pop_count = 0
    divide_count = 0
    
    pos = 0
    while fetch_dict:
        loop_count += 1
        sort_time_a = time.perf_counter()
        
        if pos == len(fetch_dict) - 1:  # 已遍历1次
            fetch_dict = sorted(fetch_dict, key=lambda x: x['task_count'], reverse=True)
            sort_count += 1
            pos = 0
            cur_task = fetch_dict[0]
        else:
            # 花里胡哨的,不如直接过一遍排序后再来一遍
            cur_task = fetch_dict[pos]
            ...
        sort_time_b = time.perf_counter()
        global sort_time
        sort_time += sort_time_b - sort_time_a
        
        allocate_time_a = time.perf_counter()
        # 大多数情况下,以下任务分配耗时占比>80%
        min_work_flow_index = work_flow_task_count.index(min(work_flow_task_count))
        min_work_flow = work_flows[min_work_flow_index]
        if (cur_task['task_count'] > 100) and (cur_task['task_count'] + work_flow_task_count[
            min_work_flow_index] > work_flow_capacity + floodplain_size):
            # 'task_count'>100且直接分配时超出缓冲区大小
            # 规避了当'work_flow_capacity'不为整数时
            # 最小的'work_flow'的'task_count'+1也会超出的情况
            # 严格按照步长'step'的倍数从前往后分割
            # 避免'start'!=0时,分割位点和offset的繁复计算
            
            if len(cur_task['range']) == 3:
                step = cur_task['range'][2]
            elif len(cur_task['range']) == 4:
                step = cur_task['range'][2]
            else:
                step = func_limit
                ...
            
            # 确定分配的task_count
            raw_allocate_task_num = (work_flow_capacity - work_flow_task_count[min_work_flow_index] + flood_discharge)
            # floodplain_ratio==0时flood_discharge为0
            allocate_task_num = raw_allocate_task_num - raw_allocate_task_num % step
            # 向下取step的公倍数
            
            start, end = cur_task['range'][:2]
            new_end = start + allocate_task_num
            
            new_task = copy.deepcopy(cur_task)
            new_task['task_count'] = allocate_task_num
            cur_task['task_count'] -= allocate_task_num
            
            new_task['range'][1] = new_end
            cur_task['range'][0] += allocate_task_num
            work_flow_task_count[min_work_flow_index] += allocate_task_num
            
            min_work_flow['task_count'] += allocate_task_num
            min_work_flow['task_pool'].append(new_task)
            
            divide_count += 1
        else:  # 直接分配
            min_work_flow['task_count'] += cur_task['task_count']
            min_work_flow['task_pool'].append(copy.deepcopy(cur_task))
            work_flow_task_count[min_work_flow_index] += cur_task['task_count']
            
            cur_task_index = fetch_dict.index(cur_task)
            fetch_dict.pop(cur_task_index)  # 无论如何都pop出'cur_task'
            pop_count += 1
            ...
        # 本次分配完成
        allocate_time_b = time.perf_counter()
        global append_time
        append_time += allocate_time_b - allocate_time_a
        ...
    # count = 0
    # for each_flow in work_flows:
    #     for each in each_flow:
    #         count += each['task_count']
    #         ...
    #     ...
    # print(count)
    # print('work_flows', work_flows)
    # print(f'sort_count\t\t{sort_count}')
    # print(f'loop_count\t\t{loop_count}')
    # print(f'pop_count\t\t{pop_count}')
    # print(f'divide_count\t{divide_count}')
    # print('/' * 30)
    return work_flows


if __name__ == '__main__':
    import zhihu_APIs
    
    
    # return:{'task_count': task_total_count, 'task_pool': [[{},{}],[]]}
    
    # 性能参考: 250k:10s 500k:33s
    # 对'work_flow_num'==1时已有优化
    # todo:如有远超250k规模的负载均衡需求,应考虑加入多进程执行负载均衡
    
    # 测试用例参数
    STEP = 20
    LIMIT = 17
    task_count_list = [5000 + x for x in range(100000, 0, -1)] + [3, 2, 1]
    
    print(f'len(task_count_list)\t{len(task_count_list)}')
    FETCH_DICT = [{"identifier": "url_token", "query_args": ["voteup_count", "answer_count", "article_count"],
                   "range": [0, x, STEP, LIMIT]} for x in task_count_list]
    
    # FETCH_DICT = [{"identifier": "url_token", "query_args": ["following_count", "thanked_count"], "range": [0, 200]},
    #               {"identifier": "zhang-jia-wei", "query_args": ["voteup_count", "answer_count", "article_count"],
    #                "range": [0, 10, 10, 7]}]
    
    FUNC = zhihu_APIs.ZhiHu().members.followers
    
    res = load_balance(FETCH_DICT, FUNC, 2, flood_discharge_ratio=0.3, floodplain_ratio=0.1)
    print(res)
    
    # 性能分析
    total_time = time.perf_counter()
    print(f'total_time = {total_time}')
    print(f'count_time\t/\ttotal_time\t{count_time / total_time}')
    print(f'sort_time\t/\ttotal_time\t{sort_time / total_time}')
    print(f'append_time\t/\ttotal_time\t{append_time / total_time}')
