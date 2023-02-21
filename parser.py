import datetime
import sys
from subprocess import *


def get_timedate():
    date_time = datetime.datetime.now()
    return date_time.strftime("%d-%m-%Y-%H-%M-scan.txt")


def open_file(file_name):
    result = run(["cat", f"{file_name}"], stdout=PIPE, encoding='utf-8').stdout
    print(result)


def get_data_ps_aux():
    raw_data_by_lines = Popen(['ps', 'aux'], stdout=PIPE, encoding='utf-8').stdout.readlines()
    headers = [h for h in ' '.join(raw_data_by_lines[0].strip().split()).split() if h]
    fullfilment = map(lambda line: line.strip().split(None, len(headers) - 1), raw_data_by_lines[1:])
    data_dict = [dict(zip(headers, line)) for line in fullfilment]
    return data_dict


def parce_to_file(file_name):
    data = get_data_ps_aux()
    users = set()
    cpu = []
    mem = []
    maxRSS = int(data[0]["RSS"])
    minRSS = int(data[0]["RSS"])
    maxCPU = float(data[0]["%CPU"])
    minCPU = float(data[0]["%CPU"])
    user_proccesses_dict = {data[0]["USER"]: 0}
    for i in data:
        users.add(i["USER"])
        cpu.append(float(i["%CPU"]))
        mem.append(int(i["RSS"]))
        if i["USER"] in user_proccesses_dict:
            user_proccesses_dict[i["USER"]] = user_proccesses_dict[i["USER"]] + 1
        else:
            user_proccesses_dict[i["USER"]] = 1
        if float(i["%CPU"]) >= maxCPU:
            maxCPU = float(i["%CPU"])
            maxCPU_proces = i
        else:
            minCPU = float(i["%CPU"])
            minCPU_proces = i
        if int(i["RSS"]) >= maxRSS:
            maxRSS = int(i["RSS"])
            maxRSS_proces = i
        else:
            minRSS = int(i["RSS"])
            minRSS_proces = i

    with open(file_name, "w") as file:
        sys.stdout = file
        print("Отчёт о состоянии системы:")
        print("Пользователи системы: ", ', '.join(map(str, users)))
        print("Всего процессов запущено:", len(data))
        print("Пользовательские процессы:",
              str(user_proccesses_dict).replace("{", "").replace("'", "").replace("}", ""))
        print("Всего памяти используется:", sum(mem), "b")
        print("Всего CPU используется:", sum(cpu), "%")
        print("Больше всего памяти использует:", maxRSS_proces["COMMAND"][:20])
        print("Меньше всего памяти использует:", minRSS_proces["COMMAND"][:20])
        print("Больше всего CPU использует:", maxRSS_proces["COMMAND"][:20])
        print("Меньше всего CPU использует:", minRSS_proces["COMMAND"][:20])
    sys.stdout = sys.__stdout__


if __name__ == '__main__':
    file_name_ = get_timedate()
    parce_to_file(file_name_)
    open_file(file_name_)
