import datetime as dt 
import webbrowser as wb
import subprocess
print("FRIDAY IS ONLINE")
def greet():
    print("hello sir")
def status():
    print("all systems are operational")
def shutdown():
    print("shutting down sir")
def open_website(domain):
    wb.open(f"https://www.{domain}.com/")
    print("browser opened")
def date_time():
    current_time = dt.datetime.now()
    format_time = current_time.strftime("%I:%M %p")
    print(f"current time is {format_time}")

def open_application(application):
    process = applications.get(application)
    if process is not None:
        
        subprocess.run(process)
    else:
        print("no path for this yet")


commands = {
    "hello": greet,
    "status":status, 
    "time": date_time, 
    "exit": shutdown,
    }

applications = {
    "calculator": r"C:\Windows\System32\calc.exe",
    "notepad": r"C:\Windows\notepad.exe"
}

while True:
    
    query = input("whats your query")
    strip_query = query.strip()
    lower_query = strip_query.lower()
    split_query = lower_query.split()
         
    
    functions = commands.get(lower_query)
    if len(split_query) == 2:
        if split_query[0] == "open" and split_query[1] in applications:
                open_application(split_query[1])
                continue
        elif split_query[0] == "open": 
            open_website(split_query[1])
            continue
        else:
            print("i dont know this cmd yet")
            continue
    if functions is not None:
        functions()
        if functions == shutdown:
            break
    else:
        print("i dont know this cmd yet")
    