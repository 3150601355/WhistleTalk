import numpy as np
import wave
import scipy.fftpack as fftpack

SAMPLE_RATE = 44100                                     # 音频采样率
SAMPLE_TIME = 0.1                                       # 采样时间 0.1s = 100ms
SAMPLE_NUM = int(SAMPLE_RATE * SAMPLE_TIME)             # 采样点数量
FREQUENCY_LIST = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700] # 口哨频率


# 快速傅里叶变换
def fft(data):
    N = len(data)
    fft_data = fftpack.fft(data)                        # 做fft                     
    abs_fft = np.abs(fft_data)                          # 取模      
    abs_fft = abs_fft/(N/2)                             # fft后弦波分量的振幅放大了N/2倍，除一下以归一化
    half_fft = abs_fft[range(N//2)]                     # 取单边频谱

    return half_fft


def 解码100ms音频数据(wave_data_100_ms):
    fft_ret = fft(wave_data_100_ms)
    for index, freq in enumerate(FREQUENCY_LIST):
        if np.max(fft_ret[int(freq*SAMPLE_TIME) - 2 : int(freq*SAMPLE_TIME) + 2]) > 0.8:
            # print(freq, 'Hz有值')
            return index


def 解码句子(wav_data):
    _100ms_count = len(wav_data) // SAMPLE_NUM          # 包含多少个100ms的音频片段
    print('待解码音频包含', _100ms_count // 3, '个字')    # 3个100ms片段代表一个汉字

    ret = ''
    for i in range(0, _100ms_count, 3):                 # 3个100ms片段构成一个字的序号
        # 解码单个字
        index = 0
        for k in range(3):
            index = index*10 + 解码100ms音频数据(wav_data[i*SAMPLE_NUM + k*SAMPLE_NUM : i*SAMPLE_NUM + (k+1)*SAMPLE_NUM])
        
        print('汉字序号：', index)
        ret += str常用字[index]

    return ret

if __name__ == '__main__':

    # 1）加载常用汉字
    with open('常用3000字.txt', 'r', encoding='utf8') as f:
        str常用字 =  f.read()

    # 2）从声音文件加载波形数据到wav_data
    with wave.open('结果.wav', 'rb') as f:
        wav_data = np.frombuffer(f.readframes(-1), dtype=np.int16)
        wav_data = wav_data/32768

    # 3）从wav_data中解码出文字
    print( 解码句子(wav_data) )
