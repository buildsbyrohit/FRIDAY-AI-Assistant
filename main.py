import datetime as dt 

print("FRIDAY IS ONLINE")
def greet():
    print("hello sir")
def status():
    print("all systems are operational")
def shutdown():
    print("shutting down sir")
def date_time():
    current_time = dt.datetime.now()
    format_time = current_time.strftime("%I:%M %p")
    print(f"current time is {format_time}")
commands = {
    "hello": greet,
    "status":status, 
    "time": date_time, 
    "exit": shutdown
    }

while True:
    
    query = input("whats your query")
    strip_query = query.strip()
    lower_query = strip_query.lower()

    functions = commands.get(lower_query)
    if functions is not None:
        functions()
        if functions == shutdown:
            break
    else:
        print("i dont know this cmd yet")
    
    

    

