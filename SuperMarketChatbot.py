""" 
Assignment 2 - Natural Language Processing

Name - L.W.S. Kularatne
Index No - 21/ENG/069 
Registration No - EN102714

"""

import spacy
from spacy.matcher import PhraseMatcher
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import scrolledtext,messagebox

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Data structure to map items to shelf numbers
shelfMapping = {

    "apples" : "Shelf 1",
    "bananas" : "Shelf 1",
    "mangoes" : "Shelf 1",
    "pineapples" : "Shelf 1",
    "papaya" : "Shelf 1",

    "carrot" : "Shelf 2",
    "beans" : "Shelf 2",
    "cabbage" : "Shelf 2",
    "onions" : "Shelf 2",
    "garlic" : "Shelf 2",
    "tomatoes" : "Shelf 2",
    "brinjals" : "Shelf 2",
    "leeks" : "Shelf 2",
    "capsicum" : "Shelf 2",

    "chicken" : "Shelf 3",
    "fish" : "Shelf 3",
    "pork" : "Shelf 3",
    "sausages" : "Shelf 3",
    "mutton" : "Shelf 3",
    
    "soap" : "Shelf 4",
    "detergent" : "Shelf 4",
    "washing powder" : "Shelf 4",
    "handwash" : "Shelf 4",
    "harpic" : "Shelf 4",
    "air freshener" : "Shelf 4",
    "tile cleaner" : "Shelf 4",

    "bread" : "Shelf 5",
    "bun" : "Shelf 5",
    "hotdog" : "Shelf 5",

    "butter" : "Shelf 6",
    "cheese" : "Shelf 6",
    "yoghurt" : "Shelf 6",
    "curd" : "Shelf 6",
    "french fries" : "Shelf 6",

    "hair oil" : "Shelf 7",
    "shampoo" : "Shelf 7",
    "conditioner" : "Shelf 7",
    "face wash" : "Shelf 7",
    "day cream" : "Shelf 7",
    "night cream" : "Shelf 7",

    "baby soap" : "Shelf 8",
    "baby oil" : "Shelf 8",
    "baby shampoo" : "Shelf 8",
    "diapers" : "Shelf 8",

    "books" : "Shelf 9",
    "pens" : "Shelf 9",
    "pencils" : "Shelf 9",
    "glue" : "Shelf 9",

    "peanuts" : "Shelf 10",
    "biscuits" : "Shelf 10",
    "cassava chips" : "Shelf 10",

    "ginger beer": "Shelf 11",
    "coca cola": "Shelf 11",
    "soda": "Shelf 11",
    "water": "Shelf 11",
    "fanta": "Shelf 11",
    "cream soda": "Shelf 11",

}

# Initialize the PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(item) for item in shelfMapping.keys()]
matcher.add("Items", None, *patterns)

# Global dictionary to store all requested items and their shelf numbers
allRequestedItems = {}

# Function to handle greetings and basic interactions
def handleBasicInteractions(userInput):

    userInput=userInput.lower()
    
    if "hello" in userInput or "hi" in userInput or "hey" in userInput or "hello chatbot" in userInput:
        return "Hello! My name is ShoppingBot. How can I help you today?"
    elif "how are you" in userInput or "how you been doing" in userInput or "how is your day" in userInput:
        return "I am fine and I am happy to assist you!"
    elif "good morning" in userInput:
        return "Good morning! How can I help you?"
    elif "good evening" in userInput:
        return "Good evening! How can I help you?"
    elif "good afternoon" in userInput:
        return "Good afternoon! How can I help you?"
    elif "thank you" in userInput or "thanks" in userInput or "thank you very much" in userInput or "thank you so much" in userInput:
        return "No worries! You are mostly welcome!"
    elif "bye" in userInput or "goodbye" in userInput:
        generateAndShowPDF()
       # root.destroy() # closing chatbot
        return "Goodbye! Have a nice day!"
    else:
        return None
    
# Function to extract items from user input
def extractItems(userInput):
    doc = nlp(userInput)
    matches = matcher(doc)
    items = [doc[start:end].text for match_id, start, end in matches]
    return items

# Function to get shelf numbers for extracted items
def getShelfNumbers(items,shelfMapping):
    response = {}
    for item in items:
        shelfNumber = shelfMapping.get(item.lower(),"Item not found")
        response[item] = shelfNumber
        allRequestedItems[item] = shelfNumber  # Add to global dictionary
    return response

# Function to generate a PDF with the shelf numbers
def generatePDF(shelfNumbers):
    outputFile="Shelf Numbers.pdf"

    c = canvas.Canvas(outputFile,pagesize=letter)
    width,height = letter
    c.drawString(100, height - 100, "Supermarket Shelf Numbers")

    y = height - 150
    for item, shelf in shelfNumbers.items():
        c.drawString(100, y, f"{item}: {shelf}")
        y -= 20

    c.save()
    messagebox.showinfo("PDF generated", f"PDF generated: {outputFile}")


# Function to handle chatbot conversation
def handleConversation():
    userInput = entry.get()
    if userInput.strip() == "":
        return
    
    insertMessage(userInput,sender="You")

    # Checking basic interactions
    response = handleBasicInteractions(userInput)

    if not response:
        # If no basic interaction by customer, check for items
        items = extractItems(userInput)

        if items:
            shelfNumbers = getShelfNumbers(items,shelfMapping)
            response = "\n".join([f"{item}: {shelf}" for item, shelf in shelfNumbers.items()])
            generatePDF(shelfNumbers) # Generate the pdf only if items are found
        else:
            response = "I coudn't find any items. Please try again."


    insertMessage(response,sender="ShoppingBot")

    # Clear the entry widget
    entry.delete(0,tk.END)

 # Function to enable the text widget and insert messages
def insertMessage(message, sender="ShoppingBot"):
    try:
        chatHistory.config(state='normal')
        chatHistory.insert(tk.END, f"{sender}: {message}\n")
        chatHistory.config(state='disabled')
        chatHistory.yview(tk.END)
    except tk.TclError as e:
        print(f"Tkinter Error: {e}")
 
#Function to generate PDF and show message when chatbot ends the conversation
def generateAndShowPDF():
    global allRequestedItems
    generatePDF(allRequestedItems)
    allRequestedItems={} # Resetting the global dictionary after generating the PDF

# Creating the main window
root = tk.Tk()
root.title("Supermarket Chatbot")

#Create and place widgets
chatHistory = scrolledtext.ScrolledText(root, wrap=tk.WORD, state = 'disabled', width = 60, height = 20)
chatHistory.pack(pady=10)

entryFrame = tk.Frame(root)
entryFrame.pack(pady=5)

entry = tk.Entry(entryFrame, width=50)
entry.pack(side=tk.LEFT, padx=5)

submitButton = tk.Button(entryFrame, text="Send", command = handleConversation)
submitButton.pack(side=tk.LEFT)

# Run the GUI event loop
root.mainloop()

