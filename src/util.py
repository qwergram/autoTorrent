
def tprint(*args, **kwargs):
    "Used for printing to terminal as terminal may not support all characters"
    try:
        print(*args, **kwargs)
    except UnicodeError:
        print("[Unable to print data]")