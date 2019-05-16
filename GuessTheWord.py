def user_login():
    import json
    username = input("Enter your username: ")
    print("\nHello " + username + "!")
    with open('users.json', 'r+') as users_dict:
        users = json.load(users_dict)
    global points
    if username in users['users']:
        points = users['points'][username]
    else:
        points = 0
        users["users"].append(username)
        users["points"].update({username: points})
        with open('users.json', 'w') as users_dict:
            json.dump(users, users_dict)
    return username


def user_input_word():
    user_word = input("Guessed it?? \n")
    return user_word


def pick_a_word():
    import json
    from random import randint
    with open('words.json') as data_file:
        words = json.load(data_file)
        words = tuple(words['project'])
    x = randint(0, len(words) - 1)
    return words[x]


def save_points(username, points):
    import json
    with open('users.json') as users_dict:
        users = json.load(users_dict)
        users['points'][username] = points
    with open('users.json', 'w') as users_dict:
        json.dump(users, users_dict)


def print_leaderboard():
    import json
    with open('users.json') as users_dict:
        users = json.load(users_dict)
        values = list(users['points'].values())
        values.sort(reverse=True)
        keys = list(users['points'].keys())
        x = 1
        print("\n LEADERBOARD \n -----------")
        for value in values:
            for key in keys:
                if value == users['points'].get(key):
                    print(x, '-', key, value, 'points')
            x += 1

def instructions_setup():
    print("\nWhile playing the game note! \n - If you have troubles guessing the word and you want a hint type \'hint\'.")
    print(" - All the hidden words in this game are lowercase")
    print(" - If you want to pass to the next word, type \'pass\' (-1 points).")
    print(" - If you want to end the game, type \'end\'.")
    print("\nLet's start!\n----------------------")


def main():

    print("GUESS THE WORD")
    username = user_login()
    global points
    print("Dear", username + ", currently you have", points, "points.")
    instructions_setup()
    used_words = set()

    secret_word = pick_a_word()
    print(username + "!", "Currently you have", points, "points.")
    print("\n" + "Definition: " + secret_word['definition'])
    input_word = user_input_word()

    while input_word != "end":
        while secret_word['the_word'] not in used_words:
            if input_word == "hint":
                print("\n" + "Definition: " + secret_word['definition'] + "\n" + "Hint: " + secret_word['hint'])
                input_word = user_input_word()
            if input_word == secret_word['the_word']:
                points += 2
                used_words.add(secret_word['the_word'])
                print("---------\nRight", username + "!", "You have got", points, "points. \n")
            elif input_word == "pass":
                points -= 1
                print("---------\nThe secret word was \'" + secret_word['the_word'] + "\'")
                used_words.add(secret_word['the_word'])
                print("\n" + username + "!", "Currently you have", points, "points. \n")
            elif input_word == "end":
                break
            else:
                print("---------\nNope! Try again please. \n\nDefinition: " + secret_word['definition'])
                input_word = user_input_word()
                while input_word not in ["hint", "pass", "end", secret_word['the_word']]:
                    print("---------\nNope! Try again please. \n\n" + "Definition: " + secret_word['definition'])
                    input_word = user_input_word()
        if input_word == "end":
            break
        secret_word = pick_a_word()
        print("Definition: " + secret_word['definition'])
        input_word = user_input_word()

    print("---------\n", username + "!", "You had", points, "points.")

    save_points(username, points)
    print_leaderboard()


main()

