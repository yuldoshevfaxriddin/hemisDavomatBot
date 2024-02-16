users = []
with open('tg-user-id.txt','r') as file:
    all_info = file.read()
    info = all_info.split('\n')

for i in info:
    if len(i) != 0:
        users.append(i.split()[0])
        
print(users)
