import socket


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


with open(r"C:\Users\phq\Desktop\test\1111.txt", encoding='utf-8') as f:
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