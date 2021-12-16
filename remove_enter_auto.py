import win32clipboard as w32c
import time
import pyperclip
import wave
import pyaudio
import glob
import random

files=glob.glob("remove_enter_sound/*")
length=len(files)
def PlayWavFie(Filename):
    try:
        wf = wave.open(Filename, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + Filename)
        return 0

    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 音声を再生
    chunk = 256
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()
def monitor(interval_sec, onchange):
	pre_seq = None

	def read():
		try:
			w32c.OpenClipboard()
			return w32c.GetClipboardData()
		except Exception as ex:
			return ex
		finally:
			w32c.CloseClipboard()

	while True:
		seq = w32c.GetClipboardSequenceNumber()

		if pre_seq != seq:
			data = read()
			pre_seq = seq

			onchange(data)

		time.sleep(interval_sec)

def main():
	def onchange(data):
		rand=random.randint(0,length-1)
		if isinstance(data, Exception):
			print("Failed:", data)
		else:
			outputlist=[]
			for str in data.splitlines():
				outputlist.append(str)
			output=''
			for i in range(len(outputlist)):
				output+=outputlist[i]+" "
			if output!=pyperclip.paste()+" ":
				print("出力↓")
				print(output)
				if output.rstrip('\n') != '':
					pyperclip.copy(output)
				print("↑ is copied!")
				# print("再生します。")
				# PlayWavFie(files[rand])

	monitor(2, onchange)

if __name__ == "__main__":
	main()
