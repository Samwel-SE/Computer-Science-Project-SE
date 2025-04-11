
# FUNCTIONS THAT ARE USED BY CLIENTS --------------------------------------------------------------------------------------------------------------------#

# helper function for getting data from the server
def convert_recv_client_data_to_int(str):
    str = str.split(",")
    
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])
    

# converts client_data into strings to be then be encoded and sent to server 
def convert_client_data_to_string(client_data):
    return str(client_data[0]) + "," + str(client_data[1]) + "," + str(client_data[2]) + "," + str(client_data[3]) + "," + str(client_data[4])


# recieves the decoded string list that contains all the strings of every piece of the map and that converts all those strings into integers
def convert_recv_map_data_to_int(decoded_string):
    #array to hold integers
    y_variables = []

    # converts long string into list of strings
    decoded_string = decoded_string.split(",")
    
    # converts every string in that list into integers 
    for i in decoded_string:

        # if there is no integer just ignores that array item
        if not(i):
            pass

        else:
            #appends the integer to the array
            y_variables.append(int(i))

    
    return y_variables





# FUNCTIONS THAT ARE USED BY SERVER ---------------------------------------------------------------------------------------------------------------------#


# puts map data into string form
def convert_map_data_to_string(y_list):
    encoded_string = ""

    for i in y_list: 
        encoded_string = encoded_string + str(i) + ","
    
    encoded_string = encoded_string[:-1]
    
    return encoded_string



# function for sending map data as a string to clients to be decoded
def convert_round_start_data_to_string(client_id, client_data, map_data):
    return str(client_id) + "," + convert_client_position_data_to_string(client_data) + "," + convert_map_data_to_string(map_data)



# encodes the data into string form to send to the clients
def convert_client_position_data_to_string(client_data):
    stringified_data = []

    for i in [0,2]:
        if len(str(client_data[i])) < 4:
            stringified_data.append("0" + str(client_data[i]))

        else:
            stringified_data.append(str(client_data[i]))


    return stringified_data[0] + "," + str(client_data[1]) + "," + stringified_data[1] + "," + str(client_data[3]) + "," + str(client_data[4])
# -----------------------------------------------------------------------------------------------------------------------------------------------#

