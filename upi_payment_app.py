import streamlit as st
import speech_recognition as sr
import pyttsx3
import re
from PIL import Image
from datetime import datetime
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Dummy database for users and their balance
users_db = {"admin": "admin"}
user_balance = {"admin": 1000}
balance_history = {"admin": [(datetime.now(), 1000)]}  # Track initial balance
transaction_history = {"admin": []}
contacts = {"Virat": "1234567890", "Modi": "0987654321"}  # Example contacts
upi_pins = {"admin": "1234"}  # Example UPI PIN for authentication
usage_stats = {"total_commands": 0, "total_payments": 0, "total_amount_transferred": 0}

# Function to capture and process voice input
def capture_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your response...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Increased timeout
            st.write("Processing your response...")
            text = recognizer.recognize_google(audio)
            st.write(f"Heard: {text}")  # Debug line to see what was heard
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that. Please try again.")
            return None
        except sr.RequestError:
            st.write("Sorry, there was an error with the request.")
            return None
        except Exception as e:
            st.write(f"An unexpected error occurred: {e}")
            return None

# Function to detect wake word and process the command
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                st.write(f"Detected: {text}")
                if "hello upi" in text:
                    st.write("Wake word detected! Listening for command...")
                    command = capture_voice()
                    usage_stats["total_commands"] += 1
                    return command
            except sr.UnknownValueError:
                st.write("Sorry, I did not understand that.")
            except sr.RequestError:
                st.write("Sorry, there was an error with the request.")
# Function to respond to balance check commands with TTS
def respond_to_balance_check(username, command):
    balance_commands = [
        "what is my account balance", "check my balance", "how much money do I have",
        "tell me my bank balance", "show me my balance", "i want to see my balance",
        "give me my current balance", "how much is in my account", "what's my balance right now",
        "can you tell me my balance", "what's the balance of my account", "i need to know my balance",
        "show me the balance of my account", "what's in my bank account", "please check my balance",
        "how much is in my account", "i want to check my balance", "how much money is available in my account",
        "get my account balance", "i need my current balance", "what's my available balance",
        "please show my account balance", "tell me how much money i have", "what is my account status",
        "give me the balance in my bank account", "can i get my account balance", "show my current balance",
        "let me know my bank balance", "what's my current account balance", "check my account balance",
        "how much do i have in my account", "give me the balance", "can you show me my balance",
        "what’s the status of my account", "how much is left in my account", "check the balance of my account",
        "show me how much i have", "what’s the balance of my bank account", "give me my account status",
        "i need to check my account balance", "show me my current account balance", "how much is in my bank account",
        "tell me my account balance", "what’s my balance at the moment", "show me my available funds",
        "how much do i have right now", "can you check my balance", "what’s my bank account balance",
        "let me know my account balance", "how much is in my checking account", "what’s my current balance",
        "how much money is in my account", "show me my balance right now", "tell me my current balance",
        "give me the current balance", "i want to know my bank balance", "what’s the balance in my account",
        "can you tell me my account balance", "how much is available in my account", "give me the balance of my account",
        "show my bank balance", "how much money do i currently have", "tell me how much is in my account",
        "check the balance of my bank account", "what’s my balance right now", "give me my balance right now",
        "how much do i have available", "show me the balance in my account", "can you check the balance of my account",
        "i want to see how much is in my account", "what’s my account balance right now",
        "tell me the balance in my bank account", "check my account status", "how much is in my current account",
        "show me the amount in my account", "what’s my current bank balance", "give me my current bank balance",
        "can i see my balance", "how much money do i have in my account", "tell me the amount available in my account",
        "what’s the current amount in my account", "show me how much i have in my account",
        "what’s my available balance right now", "can you show me the balance of my bank account",
        "how much is left in my bank account", "give me my current account balance", "tell me how much i have in my account",
        "check my available funds", "show me my current funds", "how much money is available in my bank account",
        "what’s my account balance at the moment", "i want to know the balance of my account",
        "can you tell me how much is in my bank account", "show me the current balance in my account",
        "what’s my balance today", "give me the balance in my checking account",
        "tell me how much money is in my bank account", "how much do i currently have in my account",
        "show me the balance of my bank account", "can you check how much is in my account"
    ]
    if any(cmd in command.lower() for cmd in balance_commands):
        balance = user_balance[username]
        response = f"Your current balance is {balance}."
        engine.endLoop()  # Ensure the previous run loop is stopped
        engine.say(response)
        engine.runAndWait()
        return response
    return "Command not recognized."

def extract_payment_details(command):
    match = re.search(r'pay\s+Rs\s*(\d+)\s+to\s+(.+)', command, re.IGNORECASE)
    if match:
        amount = int(match.group(1))
        contact_name = match.group(2).strip()
        return amount, contact_name
    return None, None


# Function to handle payment commands with TTS
def handle_payment(username, command):
    pay_commands = [
        "pay", "make a payment", "send money", "transfer funds", "pay someone", "pay now",
        "send payment", "transfer money", "make a transfer", "pay the bill", "send cash",
        "process payment", "complete payment", "pay an amount", "make a payment of", "send an amount",
        "transfer an amount", "initiate payment", "execute payment", "send funds", "make a payment to",
        "pay the amount", "transfer to", "send money to", "pay for", "send payment to",
        "make a payment for", "pay bill", "send funds to", "transfer funds to", "complete transfer",
        "initiate transfer", "make payment now", "pay immediately", "transfer money now", "pay instantly",
        "send cash now", "execute transfer", "process payment now", "send an amount now",
        "pay someone now", "make a transfer now", "send funds immediately", "transfer instantly",
        "pay for something", "send money immediately", "process payment immediately", "complete payment now",
        "pay an amount now", "make payment instantly", "send payment immediately", "initiate payment now",
        "execute payment now", "send funds immediately", "make a payment today", "transfer today",
        "pay today", "send payment today", "complete payment today", "process payment today",
        "make payment today", "transfer money today", "pay bill today", "send funds today",
        "pay someone today", "execute transfer today", "process transfer today", "send money today",
        "initiate payment today", "pay for something today", "transfer funds today", "complete transfer today",
        "make payment for today", "send funds for today", "process funds today", "pay amount today",
        "transfer amount today", "send cash today", "make transfer today", "pay the amount today",
        "transfer amount", "send payment amount", "pay immediately", "send payment now", "transfer now",
        "make payment now", "pay instantly", "send money instantly", "process transfer now",
        "complete payment instantly", "send cash instantly", "initiate transfer now", "transfer instantly",
        "pay today", "send money today", "process payment instantly", "complete transfer now",
        "pay for something instantly", "send funds instantly", "transfer today", "complete payment immediately",
        "pay an amount instantly", "make a payment right now", "transfer funds right now", "send money right now",
        "pay the bill now", "process the bill", "send payment for the bill", "transfer bill payment",
        "complete bill payment", "pay for the invoice", "send money for the invoice", "transfer for invoice",
        "complete payment for invoice", "pay the invoice now", "send payment now", "initiate payment for invoice",
        "make payment for invoice", "send funds for invoice", "complete invoice payment", "process invoice payment"
    ]
    # Extract amount and contact from the command
    
    amount, contact_name = extract_payment_details(command)
    st.write(f"Amount: {amount}")
    st.write(f"Contact: {contact_name}")
    
    if any(cmd in command.lower() for cmd in pay_commands):
        if amount and contact_name:
            if contact_name in contacts:
                response = f"Pay {amount} to {contact_name}. Do you confirm this payment?"
                engine.endLoop()  # Ensure the previous run loop is stopped
                engine.say(response)
                engine.runAndWait()
                st.write(response)
                st.write("Please confirm the payment by saying 'Yes' or 'No'.")
                responseword = "Please confirm the payment by saying 'Yes' or 'No'."
                # engine.endLoop()  # Ensure the previous run loop is stopped
                engine.say(responseword)
                engine.runAndWait()
                st.write(responseword)
                confirmation = capture_voice()
                st.write(f"Confirmation: {confirmation}")
                if confirmation:
                    confirmation = confirmation.lower()
                    st.write(f"Confirmation: {confirmation}")
                if "yes" in confirmation:
                    st.write("Please choose how you would like to enter your UPI PIN:")
            
                    with st.form(key='pin_form'):
                        pin_option = st.radio("Enter PIN", ["Voice Input", "Text Input"], key="pin_option")
                        st.form_submit_button("Submit")
            
                    if pin_option == "Voice Input":
                        pin = capture_voice()
                    else:
                        pin = st.text_input("Enter UPI PIN", type="password", key="pin_input")
            
                    # Validate the PIN
                    if pin and pin.strip() == upi_pins.get(username, ""):
                        # Update user balance and balance history
                        user_balance[username] -= amount
                        balance_history[username].append((datetime.now(), user_balance[username]))
                
                        transaction_history[username].append({
                            "type": "Payment",
                            "amount": amount,
                            "contact": contact_name,
                            "status": "Completed",
                            "timestamp": datetime.now()
                        })
                        usage_stats["total_payments"] += 1
                        usage_stats["total_amount_transferred"] += amount
                
                        st.write(f"Payment of {amount} to {contact_name} is successful!")
                        engine.endLoop()
                        engine.say("Payment successful!")
                        engine.runAndWait()
                    else:
                        st.write("Payment failed. Invalid PIN.")
                        engine.endLoop()
                        engine.say("Payment failed. Invalid PIN.")
                        engine.runAndWait()
            
                    st.write("Is there anything else I can do for you?")
                    final_command = capture_voice().lower()
                    if "no" in final_command:
                        st.write("Thank you! Have a great day.")
                        engine.endLoop()
                        engine.say("Thank you! Have a great day.")
                        engine.runAndWait()
                        st.stop()  # Close the app
                else:
                    st.write("Payment not confirmed.")
                    engine.endLoop()
                    engine.say("Payment not confirmed.")
                    engine.runAndWait()
            else:
                with st.form(key='phone_form'):
                    phone_number = st.text_input("Name not found. Please provide the phone number:")
                    submit_phone_button = st.form_submit_button("Submit")
                    # st.write(f"Phone number entered: '{phone_number}'")
                if submit_phone_button:
                    st.write(f"Phone number entered: '{phone_number}'")  # Debug line
                if phone_number:
                    response = f"Pay {amount} to {contact_name} with phone number {phone_number}. Do you confirm this payment?"
                    engine.endLoop()
                    engine.say(response)
                    engine.runAndWait()

                    confirmation = capture_voice().lower()
                    if "yes" in confirmation:
                        st.write("Please choose how you would like to enter your UPI PIN:")

                        with st.form(key='pin_form'):
                            pin_option = st.radio("Enter PIN", ["Voice Input", "Text Input"], key="pin_option")
                            st.form_submit_button("Submit")

                        if pin_option == "Voice Input":
                            pin = capture_voice()
                        else:
                            pin = st.text_input("Enter UPI PIN", type="password", key="pin_input")

                        # Validate the PIN
                        if pin and pin.strip() == upi_pins.get(username, ""):
                            # Update user balance and balance history
                            user_balance[username] -= amount
                            balance_history[username].append((datetime.now(), user_balance[username]))

                            transaction_history[username].append({
                                "type": "Payment",
                                "amount": amount,
                                "contact": contact_name,
                                "phone_number": phone_number,
                                "status": "Completed",
                                "timestamp": datetime.now()
                            })
                            usage_stats["total_payments"] += 1
                            usage_stats["total_amount_transferred"] += amount

                            st.write(f"Payment of {amount} to {contact_name} with phone number {phone_number} is successful!")
                            engine.endLoop()
                            engine.say("Payment successful!")
                            engine.runAndWait()
                        else:
                            st.write("Payment failed. Invalid PIN.")
                            engine.endLoop()
                            engine.say("Payment failed. Invalid PIN.")
                            engine.runAndWait()
                
                        st.write("Is there anything else I can do for you?")
                        final_command = capture_voice().lower()
                        if "no" in final_command:
                            st.write("Thank you! Have a great day.")
                            engine.endLoop()
                            engine.say("Thank you! Have a great day.")
                            engine.runAndWait()
                            st.stop()  # Close the app
                    else:
                        st.write("Payment not confirmed.")
                        engine.endLoop()
                        engine.say("Payment not confirmed.")
                        engine.runAndWait()

# Streamlit UI
st.title("UPI Payment Simulation with Voice Assistance")

# Display voice assistant icon
image = Image.open("voice_icon.jpg")  # Ensure you have a voice assistant icon image
st.image(image, width=100)

# Placeholder for user authentication (for demo purposes)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def sign_up(username, password):
    if username in users_db:
        st.sidebar.error("Username already exists. Please choose a different one.")
    else:
        users_db[username] = password
        user_balance[username] = 1000  # Give new users an initial balance
        transaction_history[username] = []
        balance_history[username] = [(datetime.now(), 1000)]  # Initialize balance history
        upi_pins[username] = "1234"  # Set a default PIN for the new user
        st.sidebar.success("User registered successfully! Please log in.")

def log_in(username, password):
    if username in users_db and users_db[username] == password:
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        st.sidebar.success(f"Logged in as {username}")
    else:
        st.sidebar.error("Invalid username or password")

if not st.session_state['authenticated']:
    st.sidebar.title("User Authentication")
    auth_mode = st.sidebar.radio("Choose mode", ["Login", "Sign Up"])

    if auth_mode == "Sign Up":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Sign Up"):
            sign_up(new_username, new_password)

    elif auth_mode == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            log_in(username, password)
else:
    st.header(f"Welcome, {st.session_state['username']}")

    # Display balance and transaction history
    st.subheader("Balance")
    st.write(f"Current balance: {user_balance[st.session_state['username']]}")
    
    st.subheader("Transaction History")
    history = transaction_history.get(st.session_state['username'], [])
    if history:
        for txn in history:
            st.write(txn)
    else:
        st.write("No transactions yet.")

    # Button to view payment history
    st.subheader("Payment History")
    payment_history = [txn for txn in transaction_history.get(st.session_state['username'], []) if "Paid" in txn]
    if payment_history:
        for payment in payment_history:
            st.write(payment)
    else:
        st.write("No payment history available.")
    
    # Display balance history
    st.subheader("Balance History")
    balance_hist = balance_history.get(st.session_state['username'], [])
    if balance_hist:
        for timestamp, balance in balance_hist:
            st.write(f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}, Balance: {balance}")
    else:
        st.write("No balance history available.")
    
    # Display usage statistics
    st.subheader("Usage Statistics")
    st.write(f"Total Commands Processed: {usage_stats['total_commands']}")
    st.write(f"Total Payments Made: {usage_stats['total_payments']}")
    st.write(f"Total Amount Transferred: {usage_stats['total_amount_transferred']}")

    if st.button("Start Voice Command"):
        command = listen_for_commands()
        st.write(f"Command: {command}")
        
        if "pay" in command.lower():
            handle_payment(st.session_state['username'], command)
        else:
            response = respond_to_balance_check(st.session_state['username'], command)
            st.write(response)

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = ""
        st.sidebar.success("Logged out successfully")
