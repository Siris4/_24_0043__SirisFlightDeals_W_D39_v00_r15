#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

# TODO: Authenticate with a Bearer Token
# TODO: Ensure all sensitive data is extracted and created into an Environment Variable, above here.

from pprint import pprint
from datetime import datetime, timedelta
from data_manager_W_D39_v00_r15 import DataManager
from flight_search_W_D39_v00_r15 import FlightSearch
from notification_manager_W_D39_v00_r15 import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()  # needs () because it is a Class
flight_search = FlightSearch()
notification_manager = NotificationManager()

# fetch sheet data:
sheet_data = data_manager.get_request_for_getting_destination_data()
print("Fetched sheet data structure - Sheet Data after fetching, and before any Updates: ")
pprint(sheet_data)

origin_iata_code = "SAN"  #original city to fly from


#  5. In main.py check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one
#  to the FlightSearch class to get the corresponding IATA code
#  for that city using the Flight Search API.
#  You should use the code you get back to update the sheet_data dictionary.
# def iataCode_Checking():
for row in sheet_data:
    # global flight_search
    # check if "iatacode" for the row is empty:
    if row.get("iataCode") == "":
        print(f"iataCode data is empty for {row['city']}, UPDATING ROW...")
        # use the flightsearch class to get the corresponding iata code for the city:
        iata_code = flight_search.get_destination_code(row["city"])
        # update the "iatacode" in the row with the new value:
        row["iataCode"] = iata_code
        # iata_code = iata_code
        # return iata_code

print("\nSheet Data After Updates: ")
pprint(sheet_data)

# update the google sheet via sheety api if any changes were made:
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

now = datetime.now()
# print(now)
tomorrow = now + timedelta(days=1)
six_months_from_today = now + timedelta(days=181)


for destination in sheet_data:
    city_name = destination['city']
    iata_code = destination['iataCode']
    sheet_lowest_price = destination['lowestPrice']  # Assuming this is how the key is named and it's correctly populated.

    if iata_code:  # Proceed only if 'iataCode' is present.
        flight = flight_search.check_flights(origin_iata_code, iata_code, from_time=tomorrow, to_time=six_months_from_today)

        if flight:  # Assuming `flight` is None if no flight is found.
            print(f"Results for {city_name}:")
            print(f"\tSheet's Lowest Price: ${sheet_lowest_price}")
            print(f"\tSearch's Lowest Price: ${flight.price}")

            if flight.price < sheet_lowest_price:
                print(f"\tALERT: New lower price found for {city_name}: ${flight.price} (Sheet: ${sheet_lowest_price})")
                # Here, you might want to send a notification or update the sheet.
            else:
                print(f"\tNo lower price found for {city_name} than the sheet price: ${sheet_lowest_price}.")

        else:
            print(f"\tNo flight results found for {city_name}.")
    else:
        print(f"Missing IATA code for {city_name}.")


#initial code5:
# for destination in sheet_data:
#     if "iataCode" in destination and destination["iataCode"]:
#         flight = flight_search.check_flights(origin_iata_code, destination["iataCode"], from_time=tomorrow, to_time=six_months_from_today)
#
#         if flight:
#             sheet_lowest_price = destination.get("Lowest Price", "not set")  # Keep it as is, or use a sensible default
#             print(f"{destination['city']} - Sheet Lowest Price: ${sheet_lowest_price}, Search Lowest Price: ${flight.price}")
#
#             # Ensure that sheet_lowest_price is numeric before comparison
#             try:
#                 sheet_lowest_price = float(sheet_lowest_price)
#                 if flight.price < sheet_lowest_price:
#                     print(f"ALERT: New lower price found for {destination['city']}: ${flight.price} (Sheet: ${sheet_lowest_price})")
#                     # Add your notification logic here
#                 else:
#                     print(f"No lower price found for {destination['city']} than the sheet price: ${sheet_lowest_price}.")
#             except ValueError:
#                 print(f"Cannot compare prices for {destination['city']} due to non-numeric value in sheet: ${sheet_lowest_price}")
#         else:
#             print(f"No flight results found for {destination['city']}.")
#     else:
#         print(f"Missing IATA code for {destination['city']}.")


# initial code4:
# for destination in sheet_data:
#     if "iataCode" in destination and destination["iataCode"]:
#         flight = flight_search.check_flights(origin_iata_code, destination["iataCode"], from_time=tomorrow,
#                                              to_time=six_months_from_today)
#
#         # Convert the "Lowest Price" from the sheet to a float for comparison
#         sheet_lowest_price = float(destination["Lowest Price"])
#
#         if flight:
#             print(
#                 f"{destination['city']} - Sheet Lowest Price: ${sheet_lowest_price}, Search Lowest Price: ${flight.price}")
#
#             if flight.price < sheet_lowest_price:
#                 print(
#                     f"ALERT: New lower price found for {destination['city']}: ${flight.price} (Sheet: ${sheet_lowest_price})")
#                 notification_manager.send_an_SMS_text(
#                     message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
#             else:
#                 print(f"No lower price found for {destination['city']} than the sheet price: ${sheet_lowest_price}.")
#         else:
#             print(f"No flight results found for {destination['city']}.")
#     else:
#         print(f"Missing IATA code for {destination['city']}.")

# initial code3:
# for destination in sheet_data:
#     if "iataCode" in destination and destination["iataCode"]:
#         flight = flight_search.check_flights(origin_iata_code, destination["iataCode"], from_time=tomorrow,
#                                              to_time=six_months_from_today)
#
#         if flight:
#             print(f"Lowest price for {destination['city']}: ${flight.price}")
#             # ensure "Lowest Price" is a number and use it directly in comparison
#             lowest_price = float(destination.get("Lowest Price", float('inf')))   # keep it as a float
#
#             if flight.price < lowest_price: # direct comparison without conversion
#                 notification_manager.send_an_SMS_text(
#                     message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
#             else:
#                 print(
#                     f"No cheaper flight found for {destination['city']} than the lowest price in the sheet: ${lowest_price}.")
#         else:
#             print(f"No flight results found for {destination['city']}.")
#     else:
#         print(f"Missing IATA code for {destination['city']}.")

# initial code2:
# for destination in sheet_data:
#     if "iataCode" in destination and destination["iataCode"]:
#         flight = flight_search.check_flights(origin_iata_code, destination["iataCode"], from_time=tomorrow,
#                                              to_time=six_months_from_today)
#
#         # Ensure "Lowest Price" is a number and use it directly in comparison
#         lowest_price = float(destination.get("Lowest Price", float('inf')))  # Keep it as float
#
#         if flight and flight.price < lowest_price:  # Direct comparison without conversion
#             notification_manager.send_an_SMS_text(
#                 message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
#         else:
#             print(f"No cheaper flight found for {destination['city']}.")
#     else:
#         print(f"Missing IATA code for {destination['city']}.")

# initial code1:
for destination in sheet_data:
    flight = flight_search.check_flights(origin_iata_code, destination["iataCode"], from_time=tomorrow, to_time=six_months_from_today)

    if flight.price < destination["Lowest Price"]:
        notification_manager.send_an_SMS_text(message=f"Low price alert from SirisFlightDeals! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")



# elif not sheet_data[0]["iataCode"] == "":
#     print()
#     print("Data was found inside the first row of the IATA Code Column")
# # iataCode_Checking()