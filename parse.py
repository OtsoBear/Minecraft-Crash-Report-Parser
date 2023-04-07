import re

def parse_crashlog(crashlog):
    # Split the crashlog into lines
    lines = crashlog.split("\n")

    # Check that the first line is the crash report header
    if not lines or lines[0] != "---- Minecraft Crash Report ----":
        raise ValueError("Invalid crashlog format")

    # Initialize the output dictionary
    result = {}

    # Find the index where the system details start
    details_start = next((i for i, line in enumerate(lines) if line == "-- System Details --"), None)
    if details_start is None:
        raise ValueError("System details not found")

    # Parse the random message
    result["randomMessage"] = re.search(r"// (.*)", lines[1]).group(1)

    # Parse the time stamp
    result["timeStamp"] = re.search(r"Time: (.*)", lines[3]).group(1)

    # Parse the description
    result["description"] = re.search(r"Description: (.*)", lines[4]).group(1)

    # Parse the error message and possible cause
    error_line = lines[6]
    result["errorMessage"] = error_line
    if "OutOfMemoryError" in error_line:
        result["possibleCause"] = "Ran out of RAM, allocate more memory to Minecraft"
    elif "ServerHangWatchdog detected that a single server tick took" in error_line:
        result["possibleCause"] = """'max-tick-time' in server.properties file is too little. Change to -1 to disable"""
    else:
        result["possibleCause"] = "Unknown"

    # Parse the error stack trace
    stack_start = 7
    stack_end = next((i for i, line in enumerate(lines[stack_start:], start=stack_start) if not line), None)
    if stack_end is None:
        raise ValueError("Error stack trace not found")
    result["errorStackTrace"] = "\n".join(lines[stack_start:stack_end])

    # Parse the system details
    for i in range(details_start+2, len(lines)):
        line = lines[i]
        if line.startswith("--"):
            break
        elif line.startswith("Minecraft Version: "):
            result["minecraftVersion"] = line.split(": ", 1)[1]
        elif line.startswith("Operating System: "):
            match = re.search(r"Operating System: (.*)", line)
            if match is not None:
                result["operatingSystem"] = match.group(1)
        elif line.startswith("Java Version: "):
            result["javaVersion"] = line.split(": ", 1)[1]
        elif line.startswith("Memory: "):
            match = re.search(r"Memory: (.*?) / (.*?) up to (.*)", line)
            if match is not None:
                result["memoryUsed"] = match.group(1)
                result["memoryAvailable"] = match.group(2)
                result["memoryMax"] = match.group(3)

    return result


import os

# Get the absolute file path
file_path = os.path.abspath("C:/Users/otsov/Dropbox/My PC (LAPTOP-V2VGKB34)/Documents/StuffThatIncludeCoding/Random Coding/chatreport-parser/crash.txt")

# Open the file using the absolute file path
with open(file_path, "r") as file:
    file_contents = file.read()
    
def format_error_message(data):
    # Extract the values from the dictionary
    message = data['randomMessage']
    timestamp = data['timeStamp']
    description = data['description']
    error = data['errorMessage']
    cause = data['possibleCause']
    stack_trace = data['errorStackTrace']

    # Build the HTML table
    table = "<table>"
    table += "<tr><td style='width: 30%'>Message:</td><td style='width: 70%'>{}</td></tr>".format(message)
    table += "<tr><td>Timestamp:</td><td>{}</td></tr>".format(timestamp)
    table += "<tr><td>Description:</td><td>{}</td></tr>".format(description)
    table += "<tr><td>Error:</td><td>{}</td></tr>".format(error)
    table += "<tr><td>Cause:</td><td>{}</td></tr>".format(cause)
    table += "<tr><td></td><td></td></tr>"
    table += "<tr><td>Stack Trace:</td><td><button id='stack-trace-button' onclick='toggleStackTrace();'><span>Show Stack Trace</span></button><pre id='stack-trace' style='display:none;font-size: 80%'>{}</pre></td></tr>".format(stack_trace)
    table += "</table>"
    
    toggleStackTrace = """
    function toggleStackTrace() {
      var stackTrace = document.getElementById('stack-trace');
      var button = document.getElementById('stack-trace-button');
      if (stackTrace.style.display === 'none') {
        stackTrace.style.display = 'block';
        button.innerHTML = 'Hide Stack Trace';
      } else {
        stackTrace.style.display = 'none';
        button.innerHTML = 'Show Stack Trace';
      }
    }
    """
    table += "<script>{}</script>".format(toggleStackTrace)
    return table

parseddata = parse_crashlog(file_contents)
#print(parseddata)
#print(format_error_message(parseddata))
def give_final_table():
    format_error_message(parseddata)

"""
with open('example.html', 'w') as f:
    # write some HTML content to the file
    f.write(format_error_message(parseddata))

# open the file in a web browser
import webbrowser
webbrowser.open('example.html')"""