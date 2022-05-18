import numpy as np
import wave

SAMPLE_RATE = 44100                                             # 音频采样率
SAMPLE_TIME = 0.1                                               # 采样时间 0.1s = 100ms
SAMPLE_NUM = int(SAMPLE_RATE * SAMPLE_TIME)                     # 采样点数量
FREQUENCY_LIST = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700] # 口哨频率


def 编码单个字(字):
    x = np.arange(0, SAMPLE_TIME, 1/SAMPLE_RATE)                # x用于生成波形
    wav_data = np.array([])                                     # 存放返回值（一个字的音频数据，总计3*100ms）
    str_encode = str(str常用字.find(字)).zfill(3)                # 将汉字编码为三个数字，不足填充0，如"我"编码为004
    for str_num in str_encode:
        y = np.sin(2*np.pi*FREQUENCY_LIST[int(str_num)]*x)      # 生成和数字对应的波形信号，时长100ms
        wav_data = np.concatenate( (wav_data, y) )              # 把100ms数据串联起来

    return wav_data


def 编码句子(句子):
    wav_data = np.array([])                                     # 存放返回值（一句话的音频数据，总计 字数*300ms）
    for 字 in 句子:
        wav_data = np.concatenate( (wav_data, 编码单个字(字)) )  # 把300ms数据串联起来
        print('已转为音频：', 字)

    return wav_data


if __name__ == '__main__':
    # 1）加载常用汉字
    with open('常用3000字.txt', 'r', encoding='utf8') as f:
        str常用字 =  f.read()

    # 2）由汉字生成不同频率的声音
    str待发送消息 = '不是十个而是十一个'
    wav_data = 编码句子(str待发送消息)

    # 3）将波形数据存为音频文件供播放
    with wave.open('结果.wav', mode ='wb') as f:
        f.setparams((1, 2, SAMPLE_RATE, len(wav_data), "NONE", "NOT COMPRESSED")) # 单通道就行了，要啥自行车啊
        f.writeframes( (wav_data*32768).astype(np.int16) )     # wav_data原幅值为[-1,1]，乘32768可以提高音量
