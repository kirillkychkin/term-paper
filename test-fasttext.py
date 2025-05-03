import fasttext

model = fasttext.load_model("lid.176.bin")
text = "Bonjour, comment ça va ?"

pred = model.predict(text)
label = pred[0][0].replace("__label__", "")
confidence = pred[1][0]

print(f"Detected language: {label} (confidence: {confidence:.2f})")