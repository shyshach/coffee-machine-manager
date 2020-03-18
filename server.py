import socket
import json
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(50)

# menu = beverage: time elapsed to do it
with open("menu.json") as menu_json:
    menu = json.load(menu_json)

# addons = "milk":amount, "sugar":amount
with open("addons.json") as addons_json:
    addons = json.load(addons_json)

while True:
    try:
        client_socket, client_address = s.accept()
        print(f"Connection from {client_address} has been established.")
        res = f"""
{', '.join(list(menu.keys()))}
There is only {addons['sugar']} spoons of sugar 
There is only {addons['milk']} doses of milk
What would u like?
"""
        client_socket.send(bytes(str(res), "utf-8"))

        choice = client_socket.recv(1024).decode('utf-8')
        #print(choice)
        if choice in list(menu.keys()):
            client_socket.send(bytes(str("how many spoons of shugar do you want?(just enter a number) if it won't be "
                                         "enough for you pls type 'help' "), "utf-8"))
            response = client_socket.recv(1024).decode('utf-8')
            if response == "help":
                client_socket.send(bytes(str("& contacts of maintenance  firm &"), "utf-8"))
            elif int(response) < addons['sugar']:
                # updating sugar amount
                addons["sugar"] -= int(response)
                client_socket.send(bytes(str("how many doses of milk do you want?(just enter a number) "), "utf-8"))
                milk_amount = int(client_socket.recv(1024).decode('utf-8'))
                if milk_amount < addons['milk']:
                    #updating milk amount
                    addons["milk"] -= int(milk_amount)
                    client_socket.send(bytes(str(f"It will be ready in {menu[choice]} seconds"), "utf-8"))
                    time.sleep(menu[choice])# brewing
                    client_socket.send(bytes(str(choice+" is ready"), "utf-8"))
    except Exception as ex:
        print(ex)
    client_socket.close()
