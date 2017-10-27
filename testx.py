import Classifier

with open("left.wav", mode='rb') as file:
    buffer = file.read()
print(len(buffer))

classifier = Classifier.Classifier();
result, conf = classifier.run(buffer)
print(result)
print(conf)
