from os import path


filename = r"G:\Group_Work\Wyatt_Experiment\NanoSheets\TW\tangbing_sample\ColdTemp\20190516\change_power\1\changepower_001.img"
my_path = path.splitext(filename)
path_list = my_path[0].split('\\')
part_path = ""
for s_path_part in path_list[:-1]:
    part_path = part_path + s_path_part + "\\"
path = part_path + "dac\\" + path_list[-1]
print(path)
