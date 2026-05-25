# =========================================================
# German Dictionary App
# CBSE Class 12 Project
# Technologies Used:
# - Python
# - MySQL
#
# Features:
# 1. Add new words
# 2. View all words
# 3. Search words
# 4. Delete words
# 5. Quiz mode
# 6. English ↔ German translation
# =========================================================


# Import MySQL connector library
import mysql.connector

# Import random module for quiz feature
import random


# =========================================================
# DATABASE CONNECTION
# =========================================================

# Creating connection with MySQL database
# Change password according to your MySQL setup

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="german_dictionary"
)

# Cursor object helps execute SQL queries
cursor = conn.cursor()


# =========================================================
# FUNCTION TO ADD A NEW WORD
# =========================================================

def add_word():

    # Taking input from user
    english = input("Enter English word: ")
    german = input("Enter German word: ")

    # SQL query to insert values into table
    query = """
    INSERT INTO words (english_word, german_word)
    VALUES (%s, %s)
    """

    # Tuple containing values
    values = (english, german)

    # Execute query
    cursor.execute(query, values)

    # Save changes permanently
    conn.commit()

    print("Word added successfully!")


# =========================================================
# FUNCTION TO VIEW ALL WORDS
# =========================================================

def view_words():

    # SQL query to get all records
    query = "SELECT * FROM words"

    cursor.execute(query)

    # fetchall() gets all rows from table
    result = cursor.fetchall()

    print("\n----- WORD LIST -----")

    # Loop through each row
    for row in result:

        # row[0] = id
        # row[1] = english word
        # row[2] = german word

        print(
            "ID:", row[0],
            "| English:", row[1],
            "| German:", row[2]
        )


# =========================================================
# FUNCTION TO SEARCH WORD
# =========================================================

def search_word():

    # User enters any word
    search = input("Enter word to search: ")

    # Query checks both English and German columns
    query = """
    SELECT * FROM words
    WHERE english_word = %s
    OR german_word = %s
    """

    cursor.execute(query, (search, search))

    result = cursor.fetchall()

    # If result list is empty
    if len(result) == 0:
        print("Word not found!")

    else:
        print("\nSearch Results:")

        for row in result:
            print(
                "ID:", row[0],
                "| English:", row[1],
                "| German:", row[2]
            )


# =========================================================
# FUNCTION TO DELETE WORD
# =========================================================

def delete_word():

    # User enters ID of word
    word_id = input("Enter ID to delete: ")

    # SQL query to delete record
    query = "DELETE FROM words WHERE id = %s"

    cursor.execute(query, (word_id,))

    # Save changes
    conn.commit()

    print("Word deleted successfully!")


# =========================================================
# FUNCTION TO UPDATE WORD
# =========================================================

def update_word():

    # User enters ID
    word_id = input("Enter ID to update: ")

    # New values
    new_english = input("Enter new English word: ")
    new_german = input("Enter new German word: ")

    # SQL query to update data
    query = """
    UPDATE words
    SET english_word = %s,
        german_word = %s
    WHERE id = %s
    """

    values = (new_english, new_german, word_id)

    cursor.execute(query, values)

    conn.commit()

    print("Word updated successfully!")


# =========================================================
# FUNCTION FOR QUIZ MODE
# =========================================================

def quiz_mode():

    print("\n===== QUIZ MODE =====")
    print("Type 'exit' anytime to stop the quiz.\n")

    # Ask translation direction ONLY ONCE
    print("1. English → German")
    print("2. German → English")

    choice = input("Enter choice: ")

    # Exit option
    if choice.lower() == "exit":
        return

    # Validate choice
    if choice not in ["1", "2"]:
        print("Invalid choice!")
        return

    # Infinite loop for continuous quiz
    while True:

        # Get all words from database
        query = "SELECT english_word, german_word FROM words"

        cursor.execute(query)

        words = cursor.fetchall()

        # Check if database is empty
        if len(words) == 0:
            print("No words available for quiz!")
            return

        # Random word selection
        random_word = random.choice(words)

        english = random_word[0]
        german = random_word[1]

        # =====================================================
        # English → German
        # =====================================================

        if choice == "1":

            print("\nTranslate to German:")
            print(english)

            answer = input("Your answer: ")

            # Exit quiz
            if answer.lower() == "exit":
                print("Exiting Quiz Mode...")
                break

            if answer.lower() == german.lower():
                print("Correct Answer!")

            else:
                print("Wrong Answer!")
                print("Correct answer is:", german)

        # =====================================================
        # German → English
        # =====================================================

        elif choice == "2":

            print("\nTranslate to English:")
            print(german)

            answer = input("Your answer: ")

            # Exit quiz
            if answer.lower() == "exit":
                print("Exiting Quiz Mode...")
                break

            if answer.lower() == english.lower():
                print("Correct Answer!")

            else:
                print("Wrong Answer!")
                print("Correct answer is:", english)


# =========================================================
# MAIN MENU
# =========================================================

while True:

    print("\n================================")
    print(" GERMAN DICTIONARY APPLICATION ")
    print("================================")

    print("1. Add Word")
    print("2. View Words")
    print("3. Search Word")
    print("4. Delete Word")
    print("5. Update Word")
    print("6. Quiz Mode")
    print("7. Exit")

    # User menu choice
    choice = input("Enter your choice: ")

    # =====================================================
    # Calling functions according to choice
    # =====================================================

    if choice == "1":
        add_word()

    elif choice == "2":
        view_words()

    elif choice == "3":
        search_word()

    elif choice == "4":
        delete_word()

    elif choice == "5":
        update_word()

    elif choice == "6":
        quiz_mode()

    elif choice == "7":

        print("Thank you for using the application!")

        # Close database connection before exiting
        conn.close()

        break

    else:
        print("Invalid choice! Please try again.")