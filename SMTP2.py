#Justin Smith, COMP 431
#I pledge the honor code.
import sys

def isSpace(character):
    if character == " " or character == "\t":
        return True
    return False

def whitespace(line):
    index = 0
    while True:
        if index >= len(line):
            return index
        if not(isSpace(line[index])):
            return index
        index += 1
    #end while

def readCodeResponse(line, state):
    sys.stderr.write(line)
    if len(line) > 3:
        code = line[:3]
        if code == "250" and state != "DATA":
            numWhitespace = whitespace(line[3:])
            return numWhitespace > 0
        elif code == "354" and state == "DATA":
            numWhitespace = whitespace(line[3:])
            return numWhitespace > 0
        return False
    return False

def isValid(state):
    line = sys.stdin.readline()
    codeAccept = readCodeResponse(line, state)
    return codeAccept

def readLine(file):
    lineRead = ""
    while(True):
        character = file.read(1)
        lineRead += character
        if character == '\n' or character == "":
            break
    return lineRead

def isFrom(line):
    if line[:5] == "From:":
        return True
    return False

def isTo(line):
    if line[:3] == "To:":
        return True
    return False

def openFile():
    file = None
    try:
        line = sys.argv[1]
        if line.endswith('\n'):
            line = line[:-1]
        file = open(line, "r")
        return file
    except Exception:
        return file

def main():
    file = openFile()
    if file == None:
        return

    state = "MAIL" # Legal states are "MAIL", "DATA" ,"RCPT", "MESSAGE"

    fileLine = readLine(file)
    while fileLine != "":
        if isFrom(fileLine):
            if state == "MAIL":
                state = "RCPT"
            elif state == "MESSAGE" or state == "RCPT":
                if state == "RCPT":
                    print("DATA")
                    state = "DATA"
                    if not(isValid(state)):
                        print("QUIT")
                        return

                print(".")

                state = "MESSAGE"

                if not(isValid(state)):
                    print("QUIT")
                    return
                
            state = "RCPT"

            print("MAIL FROM:" + fileLine[5:], end = "")
        elif state == "MESSAGE":
            print(fileLine, end = "")
        elif isTo(fileLine):
            print("RCPT TO:" + fileLine[3:], end = "")
        elif state == "RCPT":
            print("DATA")

            state = "DATA"
            if not(isValid(state)):
                print("QUIT")
                return

            state = "MESSAGE"

            print(fileLine, end = "")
        #End if/else

        if state != "MESSAGE" and not(isValid(state)):
            print("QUIT")
            return

        fileLine = readLine(file)
    #End While
    print(".")
    isValid(state)
    print("QUIT")

main()
