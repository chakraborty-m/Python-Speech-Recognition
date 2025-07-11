import wave
# Audio file formats:
# .mp3
# .flac
# .wav

# Audio signal parameters
# - number of channels
# - sample width
# - framerate/ sample_rate: 44,100 Hz
# - number of frames
# - values of a frame

obj = wave.open("01-basics/output.wav", "rb")
print("Number of channels", obj.getnchannels())
print("sample width", obj.getsampwidth())
print("frame rate", obj.getframerate())
print("Number of frames", obj.getnframes())
print("parameters", obj.getparams())

t_audio = obj.getnframes()/obj.getframerate()
print(t_audio)

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))

obj.close()

obj_new = wave.open("01-basics/output_new.wav","wb")
obj_new.setnchannels(1)
obj_new.setsampwidth(2)
obj_new.setframerate(16000.0)

obj_new.writeframes(frames)
obj_new.close()