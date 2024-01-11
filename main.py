#Console
def console():
    print()

#Error manager
def errorManager(error):
    error_log_file = open("error_log.txt", "a")
    error_log_file.write("\n"+str(error))

# Main function
def main():

    # Check if all libraries are loaded and import them
    try:
        # Import all needed libraries
        from configparser import ConfigParser
        from flask import Flask, request, jsonify
        import subprocess
        from webbrowser import open as open_on_browser
        from threading import Thread
        from os import _exit
        from time import sleep
    except ImportError:
        # Report error and exit
        errorManager("subprocess not installed")
        errorManager("Critical error. Please install all libraries before starting.")
        exit()

    # Initialize ConfigParser
    ConfigParserObj = ConfigParser()

    # Read configurations from the file
    try:
        with open("setup.config") as config_file:
            # Access configuration values
            ConfigParserObj.read_file(config_file)
    except FileNotFoundError:
        errorManager("Config file not found")
        _exit()

    # Flask App
    server = Flask(__name__)

    # GET-request handler
    @server.route("/", methods=["GET"])
    def get_request():
        index_file = open("index.html", "r")
        index_file_content = index_file.read()
        index_file.close()
        return index_file_content

    # POST-request handler
    @server.route("/", methods=["POST"])
    def post_request():
        # Request data
        data = request.get_json()["data"]
        # Use data to control server
        if "type" in data:
            # If asking status
            if data["type"] == "status":
                return jsonify({"data": "Server is online"})
            elif data["type"] == "command":
                response = ""
                if "value" in data:
                    command = data["value"]
                    if command[0]:
                        if command[0][0]:
                            # Get command lenght information
                            section_count = len(command)
                            main_section_word_count = len(command[0])
                            print(section_count+main_section_word_count)
                            # Check if command exist
                            if command[0][0] == "exit" and main_section_word_count == 1 and section_count == 1:
                                # Shut server down
                                response = "Shutting server down..."
                                Shutdown_thread = Thread(target=Shutdown)
                                Shutdown_thread.start()
                            elif command[0][0] == "brute":
                                # Check other variables
                                print("Unready command")
                            elif command[0][0] == "settings":
                                if len(command[0][1]) == 2:
                                    if command[0][1] == "set":
                                        # Set setting value
                                        print("Unready command")
                                    elif command[0][1] == "get":
                                        # Get setting value
                                        print("Unready command")
                                    elif command[0][1] == "clear":
                                        # Clear setting value
                                        print("Unready command")
                                else:
                                    value = data["value"]
                                    values = [" ".join(sublist) if isinstance(sublist, list) else sublist for sublist in value]
                                    response = " ".join(values) + " is not a known command"
                            else:
                                value = data["value"]
                                values = [" ".join(sublist) if isinstance(sublist, list) else sublist for sublist in value]
                                response = " ".join(values) + " is not a known command"
                        else:
                            response = "Invalid request"
                    else:
                        response = "Invalid request"
                return jsonify({"data": response})
            else:
                return jsonify({"data": "Invalid request"})

    # Shutdown function
    def Shutdown():
        sleep(2)
        _exit(0)

    # Server port
    port = ConfigParserObj.get("server", "port")

    # Start control panels server
    if __name__ == "__main__":
        def start_http_server():
            server.run(port=port)
        http_server_thread = Thread(target=start_http_server)
        http_server_thread.start()

    # Open controll panel
    if ConfigParserObj.get("accessibility", "open_site"):
        # URL parameters
        protocol = ConfigParserObj.get("server", "protocol")
        host = ConfigParserObj.get("server", "host")
        open_on_browser(protocol+"://"+host+":"+port)

    # Destroy variables
    protocol = None
    host = None
    port = None
    server = None

if __name__ == "__main__":
    main()