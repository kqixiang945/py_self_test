#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import re
import subprocess
import sys
from datetime import datetime

from croniter import croniter

str_job_name = '''dx_e0_dim_d02_zhuge_appid_event_product_mapping
    hv_e1_dwd_dim_dim_d02_zhuge_appid_event_product_mapping
    device_synchro_statistics'''

"""
把多行的字符串转换成一行,并且单引号引上,逗号做分隔符
"""


def multi_row_to_one_row():
    str_conect = ''
    array = str_job_name.split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        str_conect += row + ','
    return str_conect


str_test = "'www.google.com.hk','www.google.com.hk999,'www.google.com.hk','www.google.com.hk','www.google.com.hk','www.google.com.hk'"

"""
把用单引号引上的,且逗号作为分隔符的多个元素,一行整体的字符串转换成多行.
multi_row_to_one_row <=> one_row_to_multi_row 两个方法正好相反
"""


def one_row_to_multi_row(str2):
    str_conect = ''
    array = str2.split(',')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.startswith('\'') and row.endswith('\'') or row.startswith("\"") and row.endswith("\""):
            row = row[1:-1]
        str_conect += row + '\n'
    return str_conect


"""
给每一行增加指定的前缀字符串 和 后缀字符串
"""


def each_row_begin_and_end_add_char(begin_str, end_str):
    str_conect = ''
    array = str_job_name.split('\n')
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            str_conect += begin_str + row + end_str + '\n'
    return str_conect


"""
给每一行增加指定的前缀字符串 和 后缀字符串
"""


def each_row_begin_and_end_add_char2(add_str):
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


"""
获取到操作系统剪贴板中的内容(字符串)
"""


def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    # retcode = p.wait()
    # retcode = p.communicate();
    data = p.stdout.read()
    return data


"""
获取到操作系统剪贴板中的内容(字符串)
"""


def get_clipboard_data():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data, _ = p.communicate()
    if p.returncode:  # pbpaste exited with non-zero status
        raise RuntimeError('pbpaste exited with: %d' % p.returncode)
    return data


"""
写入图片数据到操作系统剪贴板中
"""


def read_picture_to_clipboard(picture_path):
    # subprocess.run(["osascript", "-e", 'set the clipboard to (read (POSIX file "/Users/kongxiaohan/Desktop/Xnip2021-11-04_23-36-09.jpg") as JPEG picture)'])
    # 测试如果是png的图片,仍然使用如下的as JPEG picture 也是可以的.
    subprocess.run(
        ["osascript", "-e", 'set the clipboard to (read (POSIX file \"' + picture_path + '\") as JPEG picture)'])


"""
写入字符串数据到操作系统剪贴板中
"""


def send_text_to_clipboard(data):
    subprocess.run("pbcopy", universal_newlines=True, input=data)


"""
去剪贴板内容中的空行
"""


def remove_blank_line():
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for rowOrigin in array:
        row = rowOrigin.strip()
        if len(rowOrigin) != 0:
            str_conect += row + '\n'
    return str_conect


"""
对剪切板中的内容排序,并且去重
"""


def sort_and_remove_duplicate_line():
    clipboard_str = get_clipboard_data()
    line_array = clipboard_str.decode().split('\n')
    line_set = set(line_array)
    str_conect = ''
    for rowOrigin in sorted(line_set):
        row = rowOrigin.strip()
        if len(rowOrigin) != 0:
            str_conect += row + '\n'
    return str_conect


"""
对剪切板中的内容仅仅去重
"""


def remove_duplicate_line():
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


"""
获取到剪切板中指定的第几列中的数据(传入指定分隔符 + 逗号 + 第几列)
如果什么都不传默认使用"|"作为分隔符, 第一列为目标数据列.
"""


def get_speciy_column_by_index(symbol):
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


"""
sql结果集中 去掉 | ,需要传入分隔符,如果不传默认使用\t
"""


def rowhandle(symbol):
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
            if (row.startswith('|')):
                row = row[1:]
            if (row.endswith('|')):
                row = row[:-1]
            if len(symbol) == 0:
                str_conect += row.replace('|', '\t').replace(' ', '') + '\n'
            else:
                str_conect += row.replace('|', symbol).replace(' ', '') + '\n'
    return str_conect


"""
把多行的字符串转换成一行,传入添加的字符和分隔符这两个参数,逗号分隔. 如果这两个参数不传入,默认是单引号和逗号.
"""


def multi_row_to_one_row_with_args(arg):
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


"""
获取到指定字符,在指定字符串中的索引位置,如果不存在返回-1
"""


def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1


"""
对剪切板中的每行按照指定的前缀和后缀(两者逗号隔开)字符串剪切.
"""


def each_row_begin_and_end_substring(spec_str):
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


"""
校验指定的字符串是不是合法的date_time字符串
"""


def validate_datetime_str(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S.%f')
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


"""
校验指定的字符串是不是合法的date_time字符串
"""


def validate_datetime_str2(date_text):
    try:
        datetime.fromisoformat(date_text)
    except ValueError:
        return -1


"""
根据传入的正则表达式,获取匹配的字符
"""


def get_regular_match_string(regular_express):
    clipboard_str = get_clipboard_data()
    array = clipboard_str.decode().split('\n')
    str_conect = ''
    for rowOrigin in array:
        row = rowOrigin.strip()
        if row.strip() != '':
            match_list = re.findall(regular_express, row, re.M | re.I)
            if len(match_list) > 0:
                for match_str in match_list:
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


"""
获取每一行出现次数.
"""


def get_same_line_count():
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


"""
去除行之间的重复元素
"""


def remove_different_line_same_part():
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


"""
获取两个字符串的不同之处
"""


def two_string_difference(str1, str2):
    if str1 is None:
        return str2
    if str2 is None:
        return str1
    at = index_of_difference(str1, str2)
    if at == -1:
        return ""
    return str2[at:len(str2)]


"""
两个字符串在哪个位置不同
"""


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


"""
删除含有指定字符的行
"""


def delete_specify_char_line(specify_chars):
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


"""
判断一行字符串中是否包含指定数组中的某个元素.
"""


def judge_line_contain_array_element(line, specify_char_array):
    for specify_char in specify_char_array:
        specify_char = specify_char.strip()
        if line != '':
            if specify_char in line:
                return True
    return False


"""
替换str1 为str2.
flag为是否是正则模式.
"""


def replace_char(str1, str2, flag=0):
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


"""
分隔字符串
"""


def split_element():
    aaa = ',,\t'
    array = aaa.split(',', 1)
    print(array)


# ***该类的入口main方法
if __name__ == "__main__":

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
    print(gen_etl_task_cmd())

    # **获取量个字符串之间的区别
    print(two_string_difference("BAAA", "AAAB"))

    # **获取每一行的字符串出现的次数
    get_same_line_count()

    # **获取指定字符串中指定字符串之间的字符串
    str_result = find_between_all_target_str("title=\"", "\">");
    print(str_result)

    # **多行转换成一行,并用指定的字符串隔开
    str_result = multi_row_to_one_row_with_args('\',\\t');
    print(str_result)

    # **获取匹配正则表达式的字符串
    str_result = get_regular_match_string("XM[0-9]*-[0-9]*");
    print(str_result)

    # **获取
    str_result = get_speciy_column_by_index('|,1');
    print(str_result)

    # **去重和排序剪切板中的行
    str_result = sort_and_remove_duplicate_line();
    print(str_result)

    # **去重剪切板中相同的行
    str_result = remove_duplicate_line();
    print(str_result)

    now = datetime.datetime.now()
    # sched = '1 15 1,15 * *'    # at 3:01pm on the 1st and 15th of every month
    sched = '0 23 */2 * *'  # at 3:01pm on the 1st and 15th of every month
    cron = croniter.croniter(sched, now)
    for i in range(34):
        nextdate = cron.get_next(datetime.datetime)
        print(nextdate)
    # tt = run()
    # tt = one_row_to_multi_row(str2)
    # tt = each_row_begin_and_end_add_char('=======','++++++')
    # tt = each_row_begin_and_end_add_char2('======= , ++++++')
    # tt = rowhandle('\t')
    # tt = remove_blank_line()
    # tt = each_row_begin_and_end_substring('./app/,.conf')
    # print(tt)
    # sentence = 'Python programming is fun.'
    # # Substring is searched in 'gramming is fun.'
    # print(sentence.index('ing000'))
    # validate_datetime_str('2003-12-23 20:20:20.123')
    # validate_datetime_str('2003-12-23 20:20:20')
    # datetime.fromisoformat('2011-11-04')
    validate_datetime_str2('2003-12-23 20:20:20.123')

    text = 'gfgfdAAA1234ZZZuijAAA1299999ZZZjk'
    m = re.findall('AAA(.+?)ZZZ', text)
    if m:
        found = m.group(1)
        print(m.group(1))
        print(m.group(2))
