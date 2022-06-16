#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import calendar
import datetime
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime
from datetime import timedelta, date

str_job_name = '''dx_e0_dim_d02_zhuge_appid_event_product_mapping
    hv_e1_dwd_dim_dim_d02_zhuge_appid_event_product_mapping
    device_synchro_statistics'''

week_en_cn_dict = {
    "Monday": "周一",
    "Tuesday": "周二",
    "Wednesday": "周三",
    "Thursday": "周四",
    "Friday": "周五",
    "Saturday": "周六",
    "Sunday": "周日"
}

project_dic = {
    "Project_Daily_01": "fe823b8e-89f9-44eb-a566-c71e607e193c",
    "Project_Daily_01_00": "484120af-6dd5-4351-8838-143327b07dad",
    "Project_Daily_04": "261921f0-4ef8-4cca-a51c-d110d853c31c"
}


def multi_row_to_one_row():
    """
    把多行的字符串转换成一行,并且单引号引上,逗号做分隔符
    """
    str_conect = ''
    array = str_job_name.split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        str_conect += row + ','
    return str_conect


str_test = "'www.google.com.hk','www.google.com.hk999,'www.google.com.hk','www.google.com.hk','www.google.com.hk','www.google.com.hk'"


def one_row_to_multi_row(str2):
    """
    把用单引号引上的,且逗号作为分隔符的多个元素,一行整体的字符串转换成多行.
    multi_row_to_one_row <=> one_row_to_multi_row 两个方法正好相反
    """
    str_conect = ''
    array = str2.split(',')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.startswith('\'') and row.endswith('\'') or row.startswith("\"") and row.endswith("\""):
            row = row[1:-1]
        str_conect += row + '\n'
    return str_conect


def each_row_begin_and_end_add_char(add_str):
    """
    给每一行增加指定的前缀字符串 和 后缀字符串
    """
    add_str_array = add_str.split(',')
    if (len(add_str_array) == 2):
        begin_str = add_str_array[0]
        end_str = add_str_array[1]

    str_conect = ''
    clipboard_str = getClipboardData()
    array = clipboard_str.decode().split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            str_conect += begin_str + row + end_str + '\n'
    return str_conect


def getClipboardData():
    """
    获取到操作系统剪贴板中的内容(字符串)
    """
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    # retcode = p.wait()
    # retcode = p.communicate();
    data = p.stdout.read()
    return data


def get_clipboard_data():
    """
    获取到操作系统剪贴板中的内容(字符串)
    """
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data, _ = p.communicate()
    if p.returncode:  # pbpaste exited with non-zero status
        raise RuntimeError('pbpaste exited with: %d' % p.returncode)
    return data


def read_picture_to_clipboard(picture_path):
    """
    写入图片数据到操作系统剪贴板中
    """
    # subprocess.run(["osascript", "-e", 'set the clipboard to (read (POSIX file "/Users/kongxiaohan/Desktop/Xnip2021-11-04_23-36-09.jpg") as JPEG picture)'])
    # 测试如果是png的图片,仍然使用如下的as JPEG picture 也是可以的.
    subprocess.run(
        ["osascript", "-e", 'set the clipboard to (read (POSIX file \"' + picture_path + '\") as JPEG picture)'])


def send_text_to_clipboard(data):
    """
    写入字符串数据到操作系统剪贴板中
    """
    subprocess.run("pbcopy", universal_newlines=True, input=data)


def remove_blank_line():
    """
    去剪贴板内容中的空行
    """
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for rowOrigin in array:
        row = rowOrigin.strip()
        if len(rowOrigin) != 0:
            str_conect += row + '\n'
    return str_conect


def add_blank_line(symbol):
    """
    add blank line blow specify line, default each line add blank
    """
    clipboard_str = get_clipboard_data()
    line_array = clipboard_str.decode().split('\n')
    str_conect = ''
    if len(symbol) != 0 :
        symbol_array = symbol.split('==')
    else:
        symbol_array = []
    for rowOrigin in line_array:
        row = rowOrigin.strip()
        if len(symbol_array) != 0 :
            if whether_array_element_in_line(symbol_array,row):
                if len(row) != 0:
                    str_conect += row + '\n' + '\n'
            else:
                str_conect += row + '\n'
        else:
            str_conect += row + '\n' + '\n'

    return str_conect


def whether_array_element_in_line(symbol_array, line):
    exitFlag = False
    for element in symbol_array:
        if element in line:
            exitFlag = True
    return exitFlag

def sort_and_remove_duplicate_line():
    """
    对剪切板中的内容排序,并且去重
    """
    clipboard_str = get_clipboard_data()
    line_array = clipboard_str.decode().split('\n')
    line_set = set(line_array)
    str_conect = ''
    for rowOrigin in sorted(line_set):
        row = rowOrigin.strip()
        if len(rowOrigin) != 0:
            str_conect += row + '\n'
    return str_conect


def remove_duplicate_line():
    """
    对剪切板中的内容仅仅去重
    """
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    uniqueLines = list(dict.fromkeys(array))
    # uniqueLines=set(array)
    str_conect = ''
    for line in uniqueLines:
        row = line.strip()
        if len(line) != 0:
            str_conect += row + '\n'
    return str_conect


def get_speciy_column_by_index(symbol):
    """
    对剪切板中的内容仅仅去重
    """
    symbol = symbol.strip(' ')
    # 如果什么都不传默认使用"|"作为分隔符, 第一列为目标数据列.
    if len(symbol) == 0:
        separator = "|"
        lineNumber = "1"
    else:
        if "," in symbol:
            symbol_array = symbol.split(',')
            separator = symbol_array[0]
            lineNumber = symbol_array[1]
        else:
            separator = symbol
            lineNumber = "1"

    str_conect = ''
    clipboard_str = get_clipboard_data();
    array = clipboard_str.decode().split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            if re.search('[\+][-\+]+', row):
                continue
            if (row.startswith('|')):
                row = row[1:]
            if (row.endswith('|')):
                row = row[:-1]
            rowColumnArray = row.split(separator)
            str_conect += rowColumnArray[int(lineNumber) - 1].strip() + '\n'
    return str_conect


def rowhandle(symbol):
    """
    sql结果集中 去掉 | ,需要传入分隔符,如果不传默认使用\t
    """
    symbol = symbol.strip(' ')
    str_conect = ''
    # clipboard_str = getClipboardData()
    clipboard_str = get_clipboard_data();
    array = clipboard_str.decode().split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            if re.search('[\+][-\+]+', row):
                continue
            if (row.startswith('|') or row.endswith('|')):
                row = row[1:][:-1]
            cell_array = row.split("|")
            cell_conn = ''
            for cell in cell_array:
                cell_conn += cell.strip(' ') + '|'
            if len(symbol) == 0:
                str_conect += cell_conn[:-1].replace('|', '\t') + '\n'
            else:
                str_conect += cell_conn[:-1].replace('|', symbol) + '\n'
    return str_conect


def multi_row_to_one_row_with_args(arg):
    """
    sql结果集中 去掉 | ,需要传入分隔符,如果不传默认使用\t
    """
    arg_arr = arg.strip(' ').split(',')
    quotes = arg_arr[0]
    separator = arg_arr[1]
    if separator == '\\t':
        separator = '\t'
    if separator == '\\n':
        separator = '\n'
    if separator == '\\r':
        separator = '\r'

    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for rowOrigin in array:
        row = rowOrigin.strip()
        flag = (row.startswith('|') & row.endswith('|')) | (row.startswith('\'') & row.endswith('\'')) | (
                row.startswith('\"') & row.endswith('\"'))
        if (flag):
            row = (row[1:])[:-1].strip()
            str_conect += (quotes + row + quotes + separator)
    str_conect = str_conect[:-1]
    return str_conect


def index_of(val, in_list):
    """
    获取到指定字符,在指定字符串中的索引位置,如果不存在返回-1
    """
    try:
        return in_list.index(val)
    except ValueError:
        return -1

def last_index_of(val, in_list):
    """
    获取到指定字符,在指定字符串中的从最后查询对应的索引位置,如果不存在返回-1
    """
    try:
        return in_list.rindex(val)
    except ValueError:
        return -1


def each_row_begin_and_end_substring(spec_str):
    """
    对剪切板中的每行按照指定的前缀和后缀(两者逗号隔开)字符串剪切.
    """
    spec_str_array = spec_str.split(',')
    if (len(spec_str_array) == 2):
        start_str = spec_str_array[0]
        end_str = spec_str_array[1]

    str_conect = ''
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')

    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            start_index = index_of(start_str, row)
            end_index = index_of(end_str, row)
            if start_index == -1 | end_index == -1:
                str_conect += row + '\n'
            else:
                str_conect += row[start_index + len(start_str): end_index] + '\n'
    return str_conect



def getchar_by_separate_multilines(spec_str):
    """
    对剪切板中的每行按照指定的前缀和后缀(两者逗号隔开)字符串剪切.(使用指定字符在每行中的最后一个index)
    """
    start_str = ''
    end_str = ''
    if ',' in spec_str:
        spec_str_array = spec_str.split(',')
        if (len(spec_str_array) == 2):
            start_str = spec_str_array[0]
            end_str = spec_str_array[1]
        elif (len(spec_str_array) == 1):
            start_str = spec_str_array[0]
    else :
        start_str = spec_str

    str_conect = ''
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')

    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            if (start_str != ''):
                start_index = last_index_of(start_str, row)
            else :
                start_index = 0
            if (end_str != ''):
                end_index = last_index_of(end_str, row)
            else :
                end_index = len(row)
            if start_index == -1 or end_index == -1:
                str_conect += row + '\n'
            else:
                str_conect += row[start_index + len(start_str): end_index] + '\n'
    return str_conect



def judge_string_match_regular_expression(test_string, expression):
    """
    判断一个字符串是不是匹配某个特定的正则表达式
    """
    matched = re.match(expression, test_string)
    return bool(matched)


def validate_datetime_str(date_text):
    # 判断字符串是不是合法的yyyymmdd形式的日期
    yyyymmdd_regular = "((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))"
    # 判断字符串是不是合法的yyyy-mm-dd形式的日期
    yyyy_mm_dd_regular = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    validateFlag1 = judge_string_match_regular_expression(date_text, yyyymmdd_regular)
    validateFlag2 = judge_string_match_regular_expression(date_text, yyyymmdd_regular)

    if validateFlag2 or validateFlag1:
        return True
    else:
        return False


def validate_datetime_str3(date_text):
    """
    校验指定的字符串是不是合法的date_time字符串
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S.%f')
        datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be %Y-%m-%d %H:%M:%S.%f")


def validate_datetime_str2(date_text):
    """
    校验指定的字符串是不是合法的date_time字符串
    使用datetime的fromisoformat方法.
    https://docs.python.org/zh-cn/3/library/datetime.html
    返回一个对应于 date.isoformat() 和 datetime.isoformat() 所提供的某一种 date_string 的 datetime 对象。
    特别地，此函数支持以下格式的字符串：
    YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]
    """
    try:
        return datetime.fromisoformat(date_text)
    except ValueError:
        return -1


def get_regular_match_string(regular_express):
    """
    根据传入的正则表达式,获取匹配的字符
    """
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            match_list = re.findall(regular_express, row, re.M)
            if len(match_list) > 0:
                for match_str in match_list:
                    # str_conect += (match_str[0] + ",")
                    str_conect += (match_str + ",")
                str_conect = str_conect[:-1]
                str_conect += '\n'
    return str_conect


def find_between_all_target_str(first, last):
    try:
        clipboard_str = get_clipboard_data()
        array = clipboard_str.decode().split('\n')
        str_conect = ''
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row.strip() != '':
                start_index = index_of(first, row)
                while start_index != -1:
                    row = row[start_index + len(first): len(row)]
                    last_index = index_of(last, row)
                    target_char = row[0: last_index]
                    str_conect = str_conect + target_char + '\n'
                    start_index = index_of(first, row)
        return str_conect
    except ValueError:
        return ""


def get_same_line_count():
    """
    获取每一行出现次数.
    """
    try:
        clipboard_str = get_clipboard_data()
        array = clipboard_str.decode().split('\n')
        str_conect = ""
        result = {}
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row != '':
                line_count = result.get(row, 0)
                if not line_count:
                    result[row] = 1
                else:
                    result[row] = line_count + 1
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for item in result:
            str_conect += item[0] + " " + str(item[1]) + "\n"

        print(str_conect)

        return str_conect
    except ValueError:
        return ""


def remove_different_line_same_part():
    """
    去除行之间的重复元素
    """
    try:
        clipboard_str = get_clipboard_data()
        array = clipboard_str.decode().split('\n')
        str_conect = ""
        result = {}
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row != '':
                line_count = result.get(row, 0)
                if not line_count:
                    result[row] = 1
                else:
                    result[row] = line_count + 1
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for item in result:
            str_conect += item[0] + " " + str(item[1]) + "\n"

        print(str_conect)

        return str_conect
    except ValueError:
        return ""


def gen_etl_task_cmd():
    try:
        clipboard_str = get_clipboard_data()
        array = clipboard_str.decode().split('\n')
        str_connect = ""
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row != '':
                if row[0:6] == 'dx_e0_':
                    str_connect += '/home/etluser/app/azkabanagent/datax_task_agent.sh /home/etluser/task/datax/etl0/ ' + row + '\r'
                elif row[0:7] == 'dx_app_':
                    str_connect += '/home/etluser/app/azkabanagent/datax_task_agent.sh /home/etluser/task/datax/app/ ' + row + '\r'
                elif row[0:11] == 'dx_runonce_':
                    str_connect += '/home/etluser/app/azkabanagent/datax_task_agent.sh /home/etluser/task/datax/run_once/ ' + row + '\r'
                elif row[0:6] == 'hv_e1_':
                    str_connect += '/home/etluser/app/azkabanagent/hive_task_agent.sh /home/etluser/task/hive/etl1/ ' + row + '\r'
                elif row[0:6] == 'hv_e2_':
                    str_connect += '/home/etluser/app/azkabanagent/hive_task_agent.sh /home/etluser/task/hive/etl2/ ' + row + '\r'
                elif row[0:7] == 'hv_app_':
                    str_connect += '/home/etluser/app/azkabanagent/hive_task_agent.sh /home/etluser/task/hive/app/ ' + row + '\r'
                elif row[0:11] == 'hv_runonce_':
                    str_connect += '/home/etluser/app/azkabanagent/hive_task_agent.sh /home/etluser/task/hive/run_once/ ' + row + '\r'
                elif row[0:3] == 'sh_':
                    str_connect += 'sh /home/etluser/task/shell/' + row + '.sh' + '\r'
                elif row[0:3] == 'kn_':
                    str_connect += 'sh /home/etluser//azkabanagent/datax_task_agent.sh /home/etluser/task/kylin/ ' + row + '\r'
                else:
                    str_connect += '当前对应的行不合法' + '\r'
        print(str_connect)
        return str_connect
    except ValueError:
        return ""


def two_string_difference(str1, str2):
    """
    获取两个字符串的不同之处
    """
    if str1 is None:
        return str2
    if str2 is None:
        return str1
    at = index_of_difference(str1, str2)
    if at == -1:
        return ""
    return str2[at:len(str2)]


def index_of_difference(str1, str2):
    if str1 == str2:
        return -1
    if str1 is None or str1 is None:
        return 0

    index_count = 0
    loop_count = len(str1) if len(str1) < len(str2) else len(str2)
    for index in range(loop_count):
        if str1[index] != str2[index]:
            index_count = index
            break
    if index_count < len(str1) or index_count < len(str2):
        return index_count
    return -1


def delete_specify_char_line(specify_chars):
    """
    删除含有指定字符的行
    """
    try:
        clipboard_str = get_clipboard_data()
        specify_char_array = specify_chars.split(',')
        array = clipboard_str.decode().split('\n')
        str_conect = ""
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row != '':
                if not judge_line_contain_array_element(row, specify_char_array):
                    str_conect += row + '\n'
        print(str_conect)
        return str_conect
    except ValueError:
        return ""


def judge_line_contain_array_element(line, specify_char_array):
    """
    判断一行字符串中是否包含指定数组中的某个元素.
    """
    for specify_char in specify_char_array:
        specify_char = specify_char.strip()
        if line != '':
            if specify_char in line:
                return True
    return False


def replace_char(str1, str2, flag=0):
    """
    替换str1 为str2.
    flag为是否是正则模式.
    """
    try:
        clipboard_str = get_clipboard_data()
        array = clipboard_str.decode().split('\n')
        str_conect = ""
        for rowOrigin in array:
            row = rowOrigin.strip()
            if row != '':
                if flag == 0:
                    row = row.replace(str1, str2)
                    str_conect += row + '\n'
                else:
                    row = re.sub(str1, str2, row)
                    str_conect += row + '\n'
        return str_conect
    except ValueError:
        return ""


def split_element():
    """
    分隔字符串
    """
    aaa = ',,\t'
    array = aaa.split(',', 1)
    print(array)


def judge_date_format(date_text):
    """
    判断传入的日期字符串是什么类型的
    """
    # 判断日期格式
    yyyymmdd_regular = "((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))"
    yyyy_mm_dd_regular = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    validateFlag1 = judge_string_match_regular_expression(date_text, yyyy_mm_dd_regular)
    validateFlag2 = judge_string_match_regular_expression(date_text, yyyymmdd_regular)
    if validateFlag1:
        return '%Y-%m-%d'
    elif validateFlag2:
        return '%Y%m%d'


def gen_date_week(date_text, count=20):
    """
    生成日期 和 星期的工作流
    总结: 可以是一个参数 也可以是两个参数 , 也可以没有参数.
    - 没有参数: 以今天为标准 + 后续二十天 + 使用yyyymmdd的形式 + 星期几 + 两者\t分隔
    - 一个参数: 第一个参数传入的日期字符串 + 根据这个日期字符串的格式生成后续20天的日期.  +  其他的同上.
    - 两个参数: 第一个参数是传入的日期字符串 + 第二个参数是指定的后续多少天. + 其他的同上.
    """
    try:
        date_format = '%Y-%m-%d'
        #  如果没有传入日期,使用今天的日期
        if date_text == '':
            begin_date = datetime.today().strftime('%Y-%m-%d')
            begin_date_obj = datetime.strptime(begin_date, '%Y-%m-%d')
        else:
            date_format = judge_date_format(date_text)
            begin_date = date_text
            begin_date_obj = datetime.strptime(begin_date, date_format)
            str_conect = begin_date + '\t' + date_convert_week_number(begin_date) + '\n'
        for num in range(1, count):
            tempdate = (begin_date_obj + timedelta(days=num)).strftime(date_format)
            str_conect += tempdate + '\t' + date_convert_week_number(tempdate) + '\n'

        return str_conect
    except ValueError:
        return ""


"""
根据剪切板中的日期 的后面生成对应的星期几
主要匹配yyyy-mm-dd 的形式 和 yyyymmdd的形式
"""


def gen_date_week_mapping():
    try:
        yyyymmdd_regular = "((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))"
        yyyy_mm_dd_regular = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
        # 根据正则表达式匹配出日期
        yyyymmdd_regular_str = get_regular_match_string(yyyymmdd_regular)
        yyyy_mm_dd_regular_str = get_regular_match_string(yyyy_mm_dd_regular)
        str_connect = ""
        yyyymmdd_regular_array = yyyymmdd_regular_str.split('\n')
        yyyy_mm_dd_regular_array = yyyy_mm_dd_regular_str.split('\n')
        for yyyymmdd_regular in yyyymmdd_regular_array:
            yyyymmdd_regular = yyyymmdd_regular.strip()
            if yyyymmdd_regular != '':
                str_connect += yyyymmdd_regular + '\t' + date_convert_week_number(yyyymmdd_regular) + '\n'

        for yyyy_mm_dd_regular in yyyy_mm_dd_regular_array:
            yyyy_mm_dd_regular = yyyy_mm_dd_regular.strip()
            if yyyy_mm_dd_regular != '':
                str_connect += yyyy_mm_dd_regular + '\t' + date_convert_week_number(yyyy_mm_dd_regular) + '\n'

        return str_connect
    except ValueError:
        return ""


"""
根据日期计算今天是周几
"""


def date_convert_week_number(date_text):
    # 判断字符串是不是合法的yyyymmdd形式的日期
    yyyymmdd_regular = "((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))"
    # 判断字符串是不是合法的yyyy-mm-dd形式的日期
    yyyy_mm_dd_regular = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    validateFlag1 = judge_string_match_regular_expression(date_text, yyyy_mm_dd_regular)
    validateFlag2 = judge_string_match_regular_expression(date_text, yyyymmdd_regular)

    if validateFlag1:
        date_obj = datetime.strptime(date_text, '%Y-%m-%d')
    elif validateFlag2:
        date_obj = datetime.strptime(date_text, '%Y%m%d')
    return week_en_cn_dict.get(calendar.day_name[date_obj.weekday()])


def date_convert_each_timestamp(date_or_ts_or_type, type):
    """
    date类型字符串 和 timestamp字符串互相转换
    - 在date⇒ts转换的场景下.
        第一个参数为普通的日期时间 yyyy-mm-dd hh:mm:ss 或者 yyyy-mm-dd 或者 yyyymmdd 等 常用日期字符串.
        第二个参数是 秒或者毫秒 分别 用0 和 1 替代. (该参数可以省略,使用0做为默认值)
    - 在ts⇒date 转换的场景下:
        第一个参数还可以是timestamp(毫秒 或者 秒)  转换成为日期字符串
        毫秒的timestamp转换为精确到毫秒的 日期字符串.
        秒的timestamp转换成精确到秒的字符串.
        第二个参数 0 ,对应yyyy-mm-dd 的形式, 1对应的是 yyyymmdd的形式  (该参数可以省略,使用0为默认值)
    - 直接ts 输入0 (或者不输入)对应 今天的 日期 + 时间.
        直接ts 输入1 对应 精确到秒的ts时间.
    """
    result = ''
    # 如果没有输入任何参数对应输出 当前的yyyy-mm-dd hh:mm:ss的时间
    if date_or_ts_or_type == '' and type == '':
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif date_or_ts_or_type != '' and type == '':
        #     判断第一个参数是具体date,ts 或者是type
        if date_or_ts_or_type == '0':
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif date_or_ts_or_type == '1':
            return calendar.timegm(time.gmtime())
        elif len(date_or_ts_or_type) == 13:
            #     这种是timestamp 而且是精确到毫秒的 转换成yyyy-mm-dd hh:mm:dd的时间
            return datetime.fromtimestamp(int(date_or_ts_or_type) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        elif len(date_or_ts_or_type) == 8:
            #     这种是date yyyymmdd的形式 转换成到秒的timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y%m%d")
            time_stamp_str = str(datetime.timestamp(date_obj))
            return time_stamp_str[:-2]
        elif len(date_or_ts_or_type) == 10:
            if '-' in date_or_ts_or_type:
                #         这种是yyyy-mm-dd的形式  转换成到秒的timestamp
                date_obj = datetime.strptime(date_or_ts_or_type, "%Y-%m-%d")
                time_stamp_str = str(datetime.timestamp(date_obj))
                return time_stamp_str[:-2]
            #         return time.mktime(datetime.strptime(date_or_ts_or_type,"%Y-%m-%d").timetuple())
            else:
                #         这种是timestamp 精确到秒的 转换成yyyy-mm-dd hh:mm:dd的时间
                return datetime.fromtimestamp(int(date_or_ts_or_type))
        elif len(date_or_ts_or_type) == 19:
            # yyyy-mm-dd hh:mm:dd 转换成 timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y-%m-%d %H:%M:%S")
            time_stamp_str = str(datetime.timestamp(date_obj))
            return time_stamp_str[:-2]
        elif len(date_or_ts_or_type) == 17:
            # yyyymmdd hh:mm:dd 转换成 timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y%m%d %H:%M:%S")
            time_stamp_str = str(datetime.timestamp(date_obj))
            return time_stamp_str[:-2]
    elif date_or_ts_or_type != '' and type != '':
        if len(date_or_ts_or_type) == 13:
            if type == '0':
                #     这种是timestamp 而且是精确到毫秒的 转换成yyyy-mm-dd hh:mm:dd的时间
                return datetime.fromtimestamp(int(date_or_ts_or_type) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            else:
                return datetime.fromtimestamp(int(date_or_ts_or_type) / 1000).strftime('%Y%m%d %H:%M:%S.%f')[:-3]
        elif len(date_or_ts_or_type) == 8:
            #     这种是date yyyymmdd的形式 转换成到秒的timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y%m%d")
            time_stamp_str = str(datetime.timestamp(date_obj))
            if type == '0':
                return time_stamp_str[:-2]
            else:
                return time_stamp_str[:-2] + '000'
        elif len(date_or_ts_or_type) == 10:
            if '-' in date_or_ts_or_type:
                #         这种是yyyy-mm-dd的形式  转换成到秒的timestamp
                date_obj = datetime.strptime(date_or_ts_or_type, "%Y-%m-%d")
                time_stamp_str = str(datetime.timestamp(date_obj))
                if type == '0':
                    return time_stamp_str[:-2]
                else:
                    return time_stamp_str[:-2] + '000'
            else:
                #         这种是timestamp 精确到秒的 转换成yyyy-mm-dd hh:mm:dd的时间
                if type == '0':
                    return datetime.fromtimestamp(int(date_or_ts_or_type)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return datetime.fromtimestamp(int(date_or_ts_or_type)).strftime('%Y%m%d %H:%M:%S')
                # return datetime.fromtimestamp(int(date_or_ts_or_type))
        elif len(date_or_ts_or_type) == 19:
            # yyyy-mm-dd hh:mm:dd 转换成 timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y-%m-%d %H:%M:%S")
            time_stamp_str = str(datetime.timestamp(date_obj))
            if type == '0':
                return time_stamp_str[:-2]
            else:
                return time_stamp_str[:-2] + '000'
        elif len(date_or_ts_or_type) == 17:
            # yyyymmdd hh:mm:dd 转换成 timestamp
            date_obj = datetime.strptime(date_or_ts_or_type, "%Y%m%d %H:%M:%S")
            time_stamp_str = str(datetime.timestamp(date_obj))
            if type == '0':
                return time_stamp_str[:-2]
            else:
                return time_stamp_str[:-2] + '000'


def loop_list_handle(thislist):
    """
    循环遍历一个list,把里面的元素拼接成字符串
    """
    str_connect = ''
    for x in thislist:
        if ',' in x:
            str_connect += x
        else:
            str_connect += ' ' + x
    return str_connect

def combine_string(str1, str2):
    """
    把两个字符串中的每一行元素都拼接起来.
    """
    try:
        str_conect = ""
        str1_array = str1.split('\n')
        str2_array = str2.split('\n')
        for x, y in map(None, str1_array, str2_array):
            if x is not None and y is not None:
                str_conect += y.strip() + x.strip() + '\n'
            else:
                if x is None:
                    str_conect += y + '\n'
                elif y is None:
                    str_conect += x + '\n'
        return str_conect
    except ValueError:
        return ""


def daterange(start_date, end_date):
    """
    循环遍历开始时间 和 结束时间的每一天, 闭区间.
    https://www.codegrepper.com/code-examples/python/python+loop+through+every+day+of+the+year
    :param start_date:
    :param end_date:
    :return:
    """
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def gen_biangeng_command(date_text):
    """
    生成变更使用的sql
    """
    try:
        str_conect_sql1_0 = """select tmp3.jira_number, tmp3.group_create_time, tmp3.create_user_name,  
case
  when tmp2.leader_username is null then tmp3.create_user_name
  else tmp2.leader_username
end as leader_username,
tmp3.job_name, tmp3.get_online_count from (select tmp.jira_number, tmp.group_create_time, tmp.create_user_name, tmp.job_name, count(*) as get_online_count from
(
    select
    bmrg.jira_number as jira_number,
    bmrg.create_user_name as create_user_name,
    bmrg.name as group_name,
    bmrg.create_time as group_create_time,
    bmrm.name as job_name,
    bmg.name as tag_name
    from
    bddp_meta_review_map bmrm
    join bddp_meta_review_group bmrg on bmrg.id = bmrm.group_id
    join bddp_meta_job bmj on bmj.name = bmrm.name
    left join bddp_meta_map bmm on bmj.id = bmm.object_id and bmm.type = 'JOB'
    left join bddp_meta_group bmg on bmg.id = bmm.group_id and bmg.type = 'TAG'
    where
    bmrg.jira_number is not null
    and bmrm.type = 'JOB'
    and bmrg.jira_number in ('********')
and bmrg.create_time between '"""
        str_conect_sql1_1 = " 00:00:00' and '"
        str_conect_sql1_2 = """ 23:59:59'
  and bmrg.create_user_name in ('gaomiao','liwei38','lvke','wanglei261','zuoxia','dingyue','dengjun05','yangliuqing','leiyifei','lideshun','xuyuanhao','lianenyi','yangjinpeng','zhumenghan','xuzhanxi','aixianbin01','zhanglijia01','xuqianqian','yibaode','chengqihang','liuyongzhang','lucien','a-caoyiwei','a-liufeishuang','a-xiehanzhong','w_chaiyanyang','w_chenhanxiao','w_chenxiangyang1','w_duanshiling','w_goujinliang','w_liujiyue','w_liushiheng','w_liuzhangshuai','w_liyinshan1','w_lumaosheng','w_machuangji','w_shangyijun','w_sunzhenyu2','w_wangpengfei14','w_wangxinyuan5','w_wangzetao1','w_zhangchenyu5','w_zhanglong82','w_zhangzhi231')
  and bmrg.review_status = 'online'
order by
  bmrg.jira_number,bmrg.create_time,bmrm.name desc
  ) tmp group by tmp.job_name 
  ) tmp3 
  left join (
select a.username as member_username ,d.username as leader_username,b.name as 组员部门,c.name as 组长部门 from user a 
inner join dept b on a.dept_id = b.id
inner join dept c on b.pid = c.id
inner join user d on c.id= d.dept_id
where 
b.name like('%组员')
) tmp2 on tmp3.create_user_name = tmp2.member_username  
  union all """

        date_format = '%Y-%m'
        #  如果没有传入日期,使用今天的日期
        if date_text == '':
            begin_date = datetime.today().strftime('%Y-%m')
            begin_date_obj = datetime.strptime(begin_date, '%Y-%m')
        else:
            begin_date = date_text
            begin_date_obj = datetime.strptime(begin_date, date_format)
        year = begin_date_obj.year
        month = begin_date_obj.month
        # 获取指定月份的最后一天的日期  https://stackoverflow.com/questions/42950/how-to-get-the-last-day-of-the-month
        last_day = calendar.monthrange(year,month)[1]
        first_day = 1
        start_date = date(year, month, first_day)
        end_date = date(year, month, last_day)

        str_conect_sql1_all = ''
        for single_date in daterange(start_date, end_date):
            current_date = single_date.strftime("%Y-%m-%d")
            str_conect_sql1_all = str_conect_sql1_all + str_conect_sql1_0 + current_date + str_conect_sql1_1 + current_date + str_conect_sql1_2
        str_conect_sql1_all = "-- 判断条件2:当天同一个打标签任务发两次以上的.(群内通知的) 需要每天的日期执行一遍.\n" + str_conect_sql1_all[:-12]

        str_conect_sql2_0 = """--  判断条件4:有一个打标签的任务的发布历史没有关联群内的jira.
select tmp3.jira_number,tmp3.group_create_time, tmp3.create_user_name, 
case
  when tmp4.leader_username is null then tmp3.create_user_name
  else tmp4.leader_username
end as leader_username,
tmp3.job_name from(        
select tmp.jira_number,tmp.group_create_time, tmp.create_user_name,tmp.job_name from (
    select
    bmrg.jira_number as jira_number,
    bmrg.create_user_name as create_user_name,
    bmrg.name as group_name,
    bmrg.create_time as group_create_time,
    bmrm.name as job_name,
    bmg.name as tag_name
    from
    bddp_meta_review_map bmrm
    join bddp_meta_review_group bmrg on bmrg.id = bmrm.group_id
    join bddp_meta_job bmj on bmj.name = bmrm.name
    left join bddp_meta_map bmm on bmj.id = bmm.object_id and bmm.type = 'JOB'
    left join bddp_meta_group bmg on bmg.id = bmm.group_id and bmg.type = 'TAG'
    where
    bmrg.jira_number is not null
    and bmrm.type = 'JOB'
    and bmrg.create_time between '"""
        str_conect_sql2_1 = " 00:00:00' and '"
        str_conect_sql2_2 = """ 23:59:59'
  and bmrg.review_status = 'online'
  and bmrg.create_user_name in ('gaomiao','liwei38','lvke','wanglei261','zuoxia','dingyue','dengjun05','yangliuqing','leiyifei','lideshun','xuyuanhao','lianenyi','yangjinpeng','zhumenghan','xuzhanxi','aixianbin01','zhanglijia01','xuqianqian','yibaode','chengqihang','liuyongzhang','lucien','a-caoyiwei','a-liufeishuang','a-xiehanzhong','w_chaiyanyang','w_chenhanxiao','w_chenxiangyang1','w_duanshiling','w_goujinliang','w_liujiyue','w_liushiheng','w_liuzhangshuai','w_liyinshan1','w_lumaosheng','w_machuangji','w_shangyijun','w_sunzhenyu2','w_wangpengfei14','w_wangxinyuan5','w_wangzetao1','w_zhangchenyu5','w_zhanglong82','w_zhangzhi231')
order by
  bmrg.jira_number,bmrg.create_time,bmrm.name desc
  ) tmp left join (
select ('********') as jira_number_temp union all
select ('********') as jira_number_temp 
) tmp2 on tmp2.jira_number_temp = tmp.jira_number where tmp2.jira_number_temp is null order by tmp.group_create_time, tmp.create_user_name, tmp.job_name
) tmp3 left join (
select a.username as member_username ,d.username as leader_username,b.name as 组员部门,c.name as 组长部门 from user a 
inner join dept b on a.dept_id = b.id
inner join dept c on b.pid = c.id
inner join user d on c.id= d.dept_id
where 
b.name like('%组员')
) tmp4 on tmp3.create_user_name = tmp4.member_username  
    """
        str_conect_sql2_all = str_conect_sql2_0 + start_date.strftime('%Y-%m-%d') + str_conect_sql2_1 + end_date.strftime('%Y-%m-%d') + str_conect_sql2_2

        str_conect_all = str_conect_sql1_all + '\n\n\n' + str_conect_sql2_all
        return str_conect_all
    except ValueError:
        return ""

def uppercase_string(str1):
    """
    only upper case string
    :param str1:
    :return:
    """
    return str1.upper();

def lowercase_string(str1):
    """
    only lower case string
    :param str1:
    :return:
    """
    return str1.lower();

def judge_have_specify_symbol(str1):
    """
    判断字符串是否含有指定的特殊符号
    :param str1:
    :return:
    """
    # special_characters = '"!@#$%^&*()-+?_=,<>/"'
    special_characters = '"\'()`$'
    # Example: $tackoverflow
    if any(c in special_characters for c in str1):
        return True
    else:
        return False

def specify_symbol_and_escape(str1):
    """
    对字符串中含有的特殊字符进行转义
    :param str1:
    :return:
    """
    special_characters = '"\'()`$'
    for c in str1:
        if c in special_characters:
            str1 = str1.replace(c,'\\' + c)
    return str1

def urlencode(str):
    return urllib.parse.quote(str)

def urldecode(str):
    return urllib.parse.unquote(str)


def get_final_column():
    """
    获取到最终的一列
    a-xiehanzhong,xuzhanxi
    w_liyinshan,gaomiao
    zhumenghan,gaomiao
    以上的两列最终得到的一列是:
    xuzhanxi
    gaomiao
    zhumenghan
    :return:
    """
    clipboard_str = getClipboardData()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    symbol_array = ['-','_']
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            row_array = row.split('\t')
            for column in row_array:
                if not judge_line_contain_array_element(column,symbol_array):
                    str_conect += column + '\n'
                    break
    return str_conect

def get_first_or_last_target_line(str,flag):
    """
    str 为输入的指定的数字,代表取样的每行字符串的个数
    flag default number is 0 represent first target line, otherwise represent last target line
    :param str:
    :param flag:
    :return:
    """
    str_connect = ''
    clipboard_str = getClipboardData()
    array = clipboard_str.decode().split('\n')
    compare_str = ''
    last_line = ''
    if flag is None:
        flag = 0
    for index,rowOrigin in enumerate(array):
        row = rowOrigin.strip()
        sub_str = row[0:int(str)]
        if sub_str != compare_str:
            compare_str = sub_str
            if flag == 0:
                str_connect += row + '\n'
            else:
                if last_line != '':
                    str_connect += last_line + '\n'
        else:
            if index == len(array) - 1 and flag != 0:
                str_connect = str_connect + row
        last_line = row
    return str_connect

def add_row_number():
    """
    add row number to each row for clipboard（1. 2. ...）
    https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    :return:
    """
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for index,row in enumerate(array):
        str_conect += str(index + 1) + '. ' + row + '\n'
    return str_conect

def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e: # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020: # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)

def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)

def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])

def stringpartQ2B(ustring):
    """把字符串中数字和字母全角转半角"""
    return "".join([Q2B(uchar) if is_Qnumber(uchar) or is_Qalphabet(uchar) else uchar for uchar in ustring])

def stringB2Q(ustring):
    """把字符串半角转全角"""
    return "".join([B2Q(uchar) for uchar in ustring])

def stringpartB2Q(ustring):
    """把字符串中数字和字母半角转全角"""
    return "".join([B2Q(uchar) if is_Qnumber(uchar) or is_Qalphabet(uchar) else uchar for uchar in ustring])

def is_number(uchar):
    """判断一个unicode是否是半角数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_Qnumber(uchar):
    """判断一个unicode是否是全角数字"""
    if uchar >= u'\uff10' and uchar <= u'\uff19':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是半角英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def is_Qalphabet(uchar):
    """判断一个unicode是否是全角英文字母"""
    if (uchar >= u'\uff21' and uchar <= u'\uff3a') or (uchar >= u'\uff41' and uchar <= u'\uff5a'):
        return True
    else:
        return False


def row_to_column(symbol):
    """
    row to column
    """
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    content_dict = {}

    for rowOrigin in array:
        row = rowOrigin.strip()
        column_array = row.split(symbol)
        for idx, columnOrigin in enumerate(column_array):
            column = columnOrigin.strip()
            if content_dict.get(idx) is not None:
                column_value = content_dict.get(idx)
                content_dict[idx] = column_value + '\t' + column
            else:
                content_dict[idx] = column

    for item in content_dict:
        print(content_dict[item])

def enhance_combine_string(index):
    """
    把两个字符串中的每一行元素都拼接起来.
    """
    try:
        str1 = 'aaaaa'
        str2 = '''dx_e0_ssc_attendance_ssc_attend_log
dx_e0_ssc_attendance_task_bill_record
dx_e0_ssc_attendance_vacation_accessory'''
        str2 = 'cccc'

        str_conect = ""
        str1_array = str1.split('\n')
        str2_array = str2.split('\n')
        for x, y in map(None, str1_array, str2_array):
            if x is not None and y is not None:
                str_conect += y.strip() + x.strip() + '\n'
            else:
                if x is None:
                    str_conect += y + '\n'
                elif y is None:
                    str_conect += x + '\n'
        return str_conect
    except ValueError:
        return ""

def remove_empty_element_from_array (array):
    lst = []
    for item in array:
        item = item.replace('\n','').strip()
        if item is None or item == '\n' or item == '':
            continue
        else:
            lst.append(item)
    return lst


# ***该类的入口main方法
if __name__ == "__main__":
    array = ['\n','ttt','''sh /home/etluser/task/shell/sh_e0_http_wechat_c2_daily_report_data.sh -param:EXECUTION_ID=55555 -param:CURRENT_FLOW_START_DT=2022-06-04-00:25:21 -param:CURRENT_FLOW_START_DAY=2022-06-04 -param:END_DATEKEY=2022-05-20
                        ''']
    remove_empty_element_from_array(array)
    enhance_combine_string(2)


    text = "电影《２０１２》讲述了２０１２年１２月２１日的世界末日，主人公Ｊａｃｋ以及世界各国人民挣扎求生的经历，灾难面前，尽现人间百态。"
    print("text原文：", text, sep="\n", end="\n")
    text1 = stringQ2B(text)
    print("全角转半角：", text1, sep="\n", end="\n")
    text2 = stringpartQ2B(text)
    print("数字字母全角转半角：", text2, sep="\n", end="\n")

    textt = "电影《2012》讲述了2012年12月21日的世界末日,主人公Jack以及世界各国人民挣扎求生的经历,灾难面前,尽现人间百态。"
    test3 = stringB2Q(textt)
    print("banjiao转quan角：", test3, sep="\n", end="\n")
    text4 = stringpartB2Q(textt)
    print("数字字母banjiao=>quanjiao：", text4, sep="\n", end="\n")

    print(add_blank_line(''))
    row_to_column(' ')

    print(get_first_or_last_target_line('10',2))
    print('=========')
    print(get_first_or_last_target_line('10'))
    print(get_final_column())
    print(add_row_number());

    str = 'Kk@nj&%2021c#'
    encoded = urlencode(str)
    print(encoded)  # '%7B%22name%22%3A%20%22Kinkin%22%7D'

    decoded = urldecode(encoded)
    print(decoded)  # '{"name": "Kinkin"}'

    print(getchar_by_separate_multilines(',/'))
    print(last_index_of('\'',"`shopid` string COMMENT '商铺ID',"))
    print(index_of('\'',"`shopid` string COMMENT '商铺ID',"))
    print(specify_symbol_and_escape('0\'0$"'))

    print(judge_have_specify_symbol('$'))

    print(gen_biangeng_command('2022-01'))

    # **获取匹配正则表达式的字符串
    str_result = get_regular_match_string('"[a-z_0-9]*"')
    print(str_result)

    print(uppercase_string(getClipboardData()))
    print(lowercase_string(getClipboardData()))

    # **处理mysql客户端命令行返回的表格数据(方便粘贴到Excel中)
    print(rowhandle('\t'))

    print(date_convert_each_timestamp('0', ''))
    print(date_convert_each_timestamp('1', ''))
    print(date_convert_each_timestamp('2021-11-11', ''))
    print(date_convert_each_timestamp('2021-11-11', '0'))
    print(date_convert_each_timestamp('2021-11-11', '1'))

    print(date_convert_each_timestamp('2021-11-11 11:11:11', ''))
    print(date_convert_each_timestamp('2021-11-11 11:11:11', '0'))
    print(date_convert_each_timestamp('2021-11-11 11:11:11', '1'))

    print(date_convert_each_timestamp('20211111 11:11:11', ''))
    print(date_convert_each_timestamp('20211111 11:11:11', '0'))
    print(date_convert_each_timestamp('20211111 11:11:11', '1'))

    print(date_convert_each_timestamp('20211111', ''))
    print(date_convert_each_timestamp('20211111', '0'))
    print(date_convert_each_timestamp('20211111', '1'))

    print(date_convert_each_timestamp('1638024862', ''))
    print(date_convert_each_timestamp('1638024862', '0'))
    print(date_convert_each_timestamp('1638024862', '1'))

    print(date_convert_each_timestamp('1638024863123', ''))
    print(date_convert_each_timestamp('1638024863123', '0'))
    print(date_convert_each_timestamp('1638024863123', '1'))

    # print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    # print(get_date_week('2021-11-27',50))
    print(gen_date_week('', 50))

    # **获取剪切板中的日期,并在后面对应周几.
    print(gen_date_week_mapping())

    # **根据传入日期判断今天是周几
    print(date_convert_week_number('2021-11-26'))
    print(date_convert_week_number('20211127'))

    # **判断给定的时间字符串是不是一个合法的时间.只匹配yyyy-mm-dd 和其扩展形式的字符串.
    print(validate_datetime_str2('2021-11-27'))
    print(validate_datetime_str2('20211127'))
    print(validate_datetime_str2('2003-12-23 20:20:20'))

    # **判断一个字符串是否是合法的日期date.
    validate_datetime_str('2003-12-23 20:20:20')

    # **替换指定的字符串
    ttt = replace_char('_', '\t')
    # ttt = replace_char('dx_[a-z]*','00000000',1)
    print(ttt)

    # **删除剪切板中的含有指定字符串的行.
    delete_specify_char_line('_USR,_PWD')

    # **打印当前python的版本
    print(sys.version)

    # **把指定的字符串给到MacOS的剪切板
    send_text_to_clipboard("测试测试测试")

    # **把指定的图片给到MacOS的剪切板
    read_picture_to_clipboard('/Users/kongxiaohan/Desktop/Xnip2021-11-04_23-36-09.jpg')

    # **生成ETL的生产跑数命令
    gen_etl_task_cmd()

    # **获取量个字符串之间的区别
    two_string_difference("BAAA", "AAAB")

    # **获取每一行的字符串出现的次数
    get_same_line_count()

    # **获取指定字符串中指定字符串之间的字符串
    str_result = find_between_all_target_str("title=\"", "\">");
    print(str_result)

    # **多行转换成一行,并用指定的字符串隔开
    str_result = multi_row_to_one_row_with_args('\',\\t');
    print(str_result)

    # **获取
    str_result = get_speciy_column_by_index('|,1');
    print(str_result)

    # **去重和排序剪切板中的行
    str_result = sort_and_remove_duplicate_line();
    print(str_result)

    # **去重剪切板中相同的行
    str_result = remove_duplicate_line();

    # **一行转换成多行
    one_row_to_multi_row("剪切板中一行数据")

    # **为剪切板中的每一行增加前置字符串和后置字符串
    each_row_begin_and_end_add_char('=======', '++++++')

    # **删除剪切板中的空白数据
    remove_blank_line()

    # **对剪切板中的每行按照指定的前缀和后缀(两者逗号隔开)字符串剪切.
    each_row_begin_and_end_substring('./app/,.conf')
