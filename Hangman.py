import random
#ask game master for words to choose from
def masterConsole() ->(list, int):
    print("MASTER CONSOLE")
    wordList = [""]*5
    print("Enter 5 words to choose from")
    
    for i in range(5):
        wordList[i] = input(str(i +1) + ": ")
    
    return (wordList)

def startGame():
    wordList = masterConsole() #generate pool of words from masterConsole method
    attempts = int(input("Enter number of attempts: ")) #number of guesses allowed before console terminates
    word = random.choice(wordList).lower()
    guessedWord = ["*"] * len(word) #guessed word is printed in asterisks and revealed as player guesses correct letters
    
    for x in range(15):
        print("******************************")
    
    print("Welcome To Hangman!")
    print("There are " +  str(len(word)) + " letters, you have " + str(attempts) + " attempts")
    
    print(" ".join(guessedWord))
    while not(''.join(guessedWord) == word) and (attempts > 0):
        letter = input("Guess a letter: ").lower()
        #ensure player only enters a single character(numbers and spaces allowed to make word harder to guess)
        if  (not(letter.isalnum() or letter.isspace())) or (len(letter) > 1):
            print("Please guess 1 letter or number, you can also guess an empty space for phrases")
            #attempts += 1
            continue

        #if player guesses letter more than once, remind them and allow redo
        if letter in guessedWord:
            print("You already guessed this letter, try another one!")
            #attempts += 1
            continue

        #if user guesses correct letter, replace appropriate asterisks with said letter
        if (word.find(letter) >= 0) :
            print("Good guess!")
            for l in range(0, len(word)):
                if word[l] == letter:
                    guessedWord[l] = word[l]
            #attempts += 1
        else:
            print("Incorrect! Try again, guesses left: " + str(attempts - 1))
            attempts -=1

        print(" ".join(guessedWord))
        print()
    if ''.join(guessedWord) == word:
            print("Congratulations you guessed the word!")
            return
    else:
            print("Out of attempts, the word was " + word)
            return
        
        


    
startGame()

    