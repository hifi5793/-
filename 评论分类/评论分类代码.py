
import os
import socket


def classify(small_file):
    # 创建socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 主动去连接IP为43.153.68.85,端门为80的进程
    client.connect(('43.153.68.85', 80))
    start = '我有一些电商评论，你帮我分四个类：好评、差评、中立、不明确。好评、差评、中立、不明确分别对应只回复“G”、“B”、“N"、“U”.不要回复任何多余的内容！'
    data1 = start.encode('utf-8')
    client.sendall(data1)
    # 接收服务端的反馈数语
    reca_data = client.recv(1024)
    print(reca_data.decode('utf-8'))
    # 打开文档开始起飞

    with open(small_file, encoding='utf-8') as f:
        for line in f:
            data_line = '评论:' + line
            # 对教据进行编码式转换,不然报错
            data_line = data_line.encode('utf-8')
            client.sendall(data_line)
            # 接收服务端的反馈数语
            rec_data = "o"
            while True:
                rec_data = client.recv(1024)
                if rec_data != "o":
                    break
            print(rec_data.decode('utf-8'))
    # 服务器退出
    f.close()
    client.sendall(b'quit')
    client.close()


def split_file(filename, threshold=300):
    # 初始化计数器和文件序号
    count = 0
    file_num = 0
    # 初始化当前小文件的行列表
    lines = []
    # 打开大文件
    with open(filename, 'r', encoding='utf-8') as f:
        # 循环读取大文件的每一行
        for line in f:
            # 将当前行添加到行列表中
            lines.append(line)
            # 计算行列表中所有行的中文字符数量
            total_count = sum([len([c for c in l if '\u4e00' <= c <= '\u9fff']) for l in lines])
            # 如果超过了阈值
            if total_count > threshold:
                # 将行列表中的所有行保存到一个新的小文件中
                with open(f'{os.path.splitext(filename)[0]}_{file_num}.txt', 'w', encoding='utf-8') as small_file:
                    small_file.writelines(lines[:-1])
                    name = f"{os.path.splitext(filename)[0]}_{file_num}.txt"
                    print(name)
                    classify(f'{os.path.splitext(filename)[0]}_{file_num}.txt')
                # 更新计数器和文件序号，并清空行列表
                count = 0
                file_num += 1
                lines = [lines[-1]]
            # 如果当前行中文字符数量未超过阈值，则继续添加到行列表中
            else:
                count += 1
    # 处理最后一个小文件，如果行列表不为空
    if lines:
        with open(f'{os.path.splitext(filename)[0]}_{file_num}.txt', 'w', encoding='utf-8') as small_file:
            small_file.writelines(lines)
        print("Finished splitting.")


# 示例用法
split_file(r"C:\Users\phq\Desktop\test\1111.txt", threshold=300)