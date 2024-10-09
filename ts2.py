from json import load

with open("./config.json", "r",encoding='utf-8')as file:
    x = load(file)
print(x['MODE'])