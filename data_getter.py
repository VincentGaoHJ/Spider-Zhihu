# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time  : 2019/7/17 19:26
# author : strangestring
# github : https://github.com/strangestring
# mailbox: 1814232115@qq.com


import random
import asyncio
import aiohttp
import traceback
from zhihu_APIs import *
from headers_pool import HEADERS_POOL
from multiprocessing import Pool, Manager
from workflow_load_balance import load_balance


# 放弃支持get_blocked_users_api, 反正不可能拿到大量cookies
async def _fetch(url: str, identifier: str or int, func, session, headers: dict, **kwargs):
    """
    :param url: 直接请求url
    :param identifier: url_token/answer_id/etc.,用于标识此字典的归属,全局异步爬取需要
    :param func: 生成url的函数,用于定位错误
    :param session: aiohttp.ClientSession
    :param headers: 随机选取的headers
    :param args: 可能包含offset/limit,用于定位错误
    :return:
    """
    async with session.get(url, headers=headers, ssl=False) as resp:
        # verify_ssl is deprecated, use ssl=False instead
        status = resp.status  # 此处似乎无法await,也无需await
        if status == 200:
            _json = await resp.json(encoding='utf-8', )
            _json['paging']['identifier'] = identifier  # 加入标识
        else:
            # todo: 偶发错误记录与重试
            # (错误主要包含'账号已停用'/'账号已注销'/'内容已被删除')
            print(f'{func.__name__}\t{identifier} kwargs={kwargs}\tSTATUS CODE:{status}')
            _json = {'paging': {'identifier': identifier, 'status_code': status},
                     'data': {f'{func.__name__}\t{identifier} kwargs={kwargs}\tSTATUS CODE:{status}'}}
            ...
        return _json


# 如果某个fetch对象offset in range(0,0,20), 则其无返回的字典(不请求)
async def _gather_result(work_flow: dict, func, headers_pool: list, process_id: int):
    """
    :param work_flow: e.g. {'A': [[0, 10000], [5000, 15000]], 'B': [[0, 50]]}
    :param func: API functions above
    :param headers_pool: 从中随机选取headers
    :return: 返回列表, 列表元素是'fetch()'返回的字典
    """
    if 'limit' in func.__code__.co_varnames:
        # url_token/answer_id是必须参数,因此-1.
        func_limit = func.__defaults__[func.__code__.co_varnames.index('limit') - 1]
    else:
        func_limit = 1
        ...
    if work_flow['task_count'] > 0:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            task_pool = []
            for task in work_flow['task_pool']:
                identifier = task['identifier']
                if 'query_args' in task.keys():
                    query_args = task['query_args']
                else:
                    query_args = None
                if 'range' in task.keys():
                    step = limit = func_limit
                    if len(task['range']) == 2:  # step=limit使用func默认值
                        start, end = task['range']
                    elif len(task['range']) == 3:
                        start, end, step = task['range']
                    else:
                        start, end, step, limit = task['range']
                        ...
                    remainder = end % step
                    for offset in range(start, end, step):
                        if offset + step > end:  # 余数部分需要单独定制
                            offset = end - remainder
                            step = limit = remainder
                            ...
                        url = func(identifier, offset, limit=limit, query_args=query_args)
                        task_pool.append(
                                _fetch(url, identifier, func, session, random.choice(headers_pool), offset=offset,
                                       step=step, limit=limit))
                        ...
                    ...
                else:  # 'range' not in task.keys():
                    url = func(identifier, query_args=query_args)
                    task_pool.append(_fetch(url, identifier, func, session, random.choice(headers_pool)))
                    ...
                ...
            result = await asyncio.gather(*task_pool, return_exceptions=True)
            # return_exceptions=True 可知从哪个任务抛出的异常,但似乎并没见过抛出异常...
            return result
    else:
        print(f'Process\t{process_id}\ttask count {work_flow["task_count"]} is not positive.')
        return 'NO TASK'


def _sub_process(work_flow: dict, func, headers_pool: list, return_list: list, process_id: int):
    """
    :param work_flow: e.g. {'A': [[0, 10000], [5000, 15000]], 'B': [[0, 50]]}
    :param func: API functions above
    :param headers: 只需在get_data()中加入随机选取的headers, 即可定制每个请求的的headers
    :return: 若fetch_dict中所有vlue均为0,get_data()将返回空列表
    """
    __new_loop = asyncio.new_event_loop()  # 必须为当前进程创建新的event_loop, 同时支持单/多进程
    asyncio.set_event_loop(__new_loop)  # 指定new_loop为当前进程的eventloop
    __data = __new_loop.run_until_complete(_gather_result(work_flow, func, headers_pool, process_id))
    __new_loop.close()
    # 原注释: 若保留loop.close(),则会出现第二次调用时raise RuntimeError('Event loop is closed')
    if isinstance(__data, list):
        return_list.extend(__data)  # 性能很好,建议使用extend
        # 不应当使用append方法: return_list中,每个workflow单独存一个list
        ...
    ...


def get_data(fetch_dict: list, func, process_num: int = 4, max_process_num: int = 8, flood_discharge_ratio: float = 0.3,
             floodplain_ratio: float = 0.1, headers_pool: list = HEADERS_POOL):
    """
    :param fetch_dict:
    :param func:
    :param process_num:
    :param max_process_num:
    :param flood_discharge_ratio:
    :param floodplain_ratio:
    :param headers_pool:
    :return:
    """
    return_list = Manager().list()
    pool = Pool(max_process_num)
    task_allocation = load_balance(fetch_dict, func, process_num, flood_discharge_ratio=flood_discharge_ratio,
                                   floodplain_ratio=floodplain_ratio)  # 负载均衡和range参数检验
    for process_id in range(process_num):
        pool.apply_async(_sub_process, [task_allocation[process_id], func, headers_pool, return_list, process_id])
        ...
    pool.close()  # 不允许添加新进程
    pool.join()  # 等待所有进程结束
    
    # 合并同identifier的字典中的data
    dict_list_by_identifier = {}
    for each in return_list:
        identifier = each['paging']['identifier']
        if identifier in dict_list_by_identifier.keys():
            try:
                dict_list_by_identifier[identifier]['data'].extend(each['data'])
            except:  # 出错,data是字符串报错信息
                print(dict_list_by_identifier[identifier]['data'])
        else:
            dict_list_by_identifier[identifier] = each
            ...
        ...
    '''
    dict_list_by_identifier
    e.g.
    {
        "zhang-jia-wei":
        {
            "paging":
            {
                "is_end": "False",
                "totals": 2243453,
                "is_start": "True",
                "identifier": "zhang-jia-wei"
            },
            "data": [
            {
                "url_token": "1999nian-de-xia-tian",
                "id": "51651651",
                "balabala":"balabala"
            }]
        },
        "imike": balabala
    }
    '''
    return dict_list_by_identifier


# default args
PROCESS_NUM = 4
MAX_PROCESS_NUM = 8
FLOOD_DISCHARGE_RATIO = 0.3
FLOODPLAIN_RATIO = 0.1
HEADERS_POOL = HEADERS_POOL

if __name__ == '__main__':
    # 不考虑云端数据变化,step小于limit时,取样必然有重叠
    time.perf_counter()  # 计时

    zhi = ZhiHu()
    func = zhi.questions.answers

    fetch_body = [{"identifier": 29225091, "query_args": ["content"], "range": [0, 1]}, ]

    res = get_data(fetch_body, func, process_num=PROCESS_NUM, max_process_num=MAX_PROCESS_NUM,
                   flood_discharge_ratio=FLOOD_DISCHARGE_RATIO, floodplain_ratio=FLOODPLAIN_RATIO,
                   headers_pool=HEADERS_POOL)
    print(res)
    # type:'multiprocessing.managers.ListProxy'
    ...
