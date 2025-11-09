import random, time, tempfile, os, platform, subprocess, wave, math, struct

def play_jeopardy_music(loop=1):
    sample_rate = 44100
    tempo = 0.85
    melody = [
        (659, 0.35), (659, 0.35), (659, 0.35), (523, 0.35),
        (659, 0.35), (784, 0.75), (659, 0.35), (784, 0.35),
        (880, 0.45), (784, 0.45), (659, 0.45), (523, 0.45),
        (440, 0.65), (392, 0.45), (440, 0.45), (523, 0.45),
        (659, 0.75), (523, 0.45), (440, 0.45), (392, 1.2)
    ]
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav = wave.open(temp, "w")
    wav.setparams((1, 2, sample_rate, 0, "NONE", "not compressed"))
    for _ in range(loop):
        for note, dur in melody:
            num_samples = int(sample_rate * dur * tempo)
            for i in range(num_samples):
                value = int(32767.0 * math.sin(2 * math.pi * note * i / sample_rate))
                data = struct.pack("<h", value)
                wav.writeframesraw(data)
    wav.close()
    if platform.system() == "Darwin":
        subprocess.Popen(["afplay", temp.name])
    elif platform.system() == "Windows":
        try:
            import winsound
            winsound.PlaySound(temp.name, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            subprocess.Popen(["powershell", "-c", f"(New-Object Media.SoundPlayer '{temp.name}').PlaySync()"])
    elif platform.system() == "Linux":
        subprocess.Popen(["aplay", temp.name])
    return temp.name

def stop_music(tempfile_name):
    try:
        if tempfile_name and os.path.exists(tempfile_name):
            os.remove(tempfile_name)
    except:
        pass

def add_questions():
    print("=====================================")
    print("        Welcome to THE STUDIER       ")
    print("=====================================\n")
    questions = {}
    try:
        total = int(input("How many questions would you like to add? "))
    except:
        print("Whoopsie, that wasn't expected. Starting over.\n")
        return add_questions()
    print("\nYou can type 'stop' or 'enough' at any time to finish early.\n")
    for i in range(total):
        print(f"Question {i + 1} of {total}:")
        q = input("Enter the question (or type 'stop' to end): ").strip()
        if q.lower() in ["stop", "enough"]:
            print("Okay, ending question entry early.\n")
            break
        a = input("Enter the answer (or type 'stop' to end): ").strip()
        if a.lower() in ["stop", "enough"]:
            print("Okay, ending question entry early.\n")
            break
        questions[q] = a
    print(f"\n{len(questions)} question(s) added successfully!\n")
    return questions

def open_quiz(questions):
    if not questions:
        print("No questions available.\n")
        return
    score = 0
    for q, a in questions.items():
        ans = input(f"{q}\nYour answer: ").strip()
        if ans.lower() in ["stop", "quit", "exit"]:
            print("Exiting quiz early.\n")
            break
        if ans.lower() == a.lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer was: {a}\n")
    print(f"You scored {score}/{len(questions)}.\n")

def true_false_quiz(questions):
    if not questions:
        print("No questions available.\n")
        return
    score = 0
    for q, a in questions.items():
        random_answer = random.choice(list(questions.values()))
        print(f"Statement/Question: {q}")
        print(f"(Claimed answer: {random_answer})")
        guess = input("True or False? ").strip().lower()
        if guess in ["stop", "quit", "exit"]:
            print("Exiting quiz early.\n")
            break
        correct = (random_answer == a)
        if (guess == "true" and correct) or (guess == "false" and not correct):
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer was: {a}\n")
    print(f"You scored {score}/{len(questions)}.\n")

def multiple_choice_quiz(questions):
    if not questions:
        print("No questions available.\n")
        return
    if len(questions) < 4:
        print("Note: Less than 4 questions, generating limited options.\n")
    score = 0
    for q, a in questions.items():
        all_answers = list(questions.values())
        random.shuffle(all_answers)
        options = all_answers[:min(4, len(all_answers))]
        if a not in options:
            options[random.randint(0, len(options) - 1)] = a
        print(f"{q}")
        for i, opt in enumerate(options):
            print(f"{chr(65+i)}. {opt}")
        ans = input("Your answer (A, B, C, D): ").strip().upper()
        if ans.lower() in ["stop", "quit", "exit"]:
            print("Exiting quiz early.\n")
            break
        if ans and ord(ans) - 65 < len(options) and options[ord(ans) - 65] == a:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer was: {a}\n")
    print(f"You scored {score}/{len(questions)}.\n")

def flashcards(questions):
    if not questions:
        print("No questions available.\n")
        return
    print("\nFlashcards Mode. Press Enter to flip, or type 'stop' to quit.\n")
    for q, a in questions.items():
        res = input(f"Q: {q}\n").strip().lower()
        if res in ["stop", "quit", "exit"]:
            print("Returning to main menu...\n")
            return
        print(f"A: {a}\n")
    print("End of flashcards.\n")

def jeopardy(questions):
    print("\n--- JEOPARDY ---")
    print("Rules: Answer questions to earn money. If not enough questions exist, empty spots are free.")
    print("When prompted, type your answer after 'What is', just like in real Jeopardy!\n")
    temp = play_jeopardy_music(loop=3)
    if not questions:
        print("No questions yet, so all spots are free. Returning to menu.")
        stop_music(temp)
        return
    score = 0
    money_values = [100, 200, 300, 400, 500]
    for i, (q, a) in enumerate(questions.items()):
        value = money_values[i % len(money_values)]
        ans = input(f"\nQuestion (${value}): {q}\nWhat is ").strip()
        if ans.lower() in ["stop", "quit", "exit"]:
            print("Returning to main menu...\n")
            stop_music(temp)
            return
        if ans.lower() == a.lower():
            print(f"Correct! +${value}")
            print(f"Answer: What is {a}")
            score += value
        else:
            print(f"Wrong! Answer: What is {a}")
    stop_music(temp)
    print(f"\nYour Jeopardy total winnings: ${score}\n")

def bingo(questions):
    print("\n--- BINGO ---")
    print("Rules: Each correct answer fills a space. Get 5 in a row to win!\n")
    print('Note “Start at the top-left space, fill each row from left to right, then move down to the next row and continue in the same way until the bottom-right space is filled.')
    if not questions:
        print("No questions available.\n")
        return

    grid_size = 5
    total_slots = grid_size * grid_size
    question_list = list(questions.items())
    random.shuffle(question_list)

    grid = [""] * total_slots
    answered = [False] * total_slots
    grid_mapping = {}

    q_idx = 0
    for i in range(total_slots):
        if i == total_slots // 2:
            grid[i] = "FREE"
            answered[i] = True
        elif q_idx < len(question_list):
            grid[i] = str(q_idx + 1)
            grid_mapping[q_idx] = i
            q_idx += 1
        else:
            grid[i] = "FREE"
            answered[i] = True

    def display_grid():
        for i in range(grid_size):
            row = ""
            for j in range(grid_size):
                idx = i * grid_size + j
                cell = "[X]" if answered[idx] else f"[{grid[idx]}]"
                row += cell + " "
            print(row)
        print()

    def check_bingo():
        for i in range(grid_size):
            if all(answered[i*grid_size + j] for j in range(grid_size)):
                return True
        for j in range(grid_size):
            if all(answered[i*grid_size + j] for i in range(grid_size)):
                return True
        if all(answered[i*grid_size + i] for i in range(grid_size)):
            return True
        if all(answered[i*grid_size + (grid_size-1-i)] for i in range(grid_size)):
            return True
        return False

    display_grid()
    bingo_achieved = False

    for q_idx, (q, a) in enumerate(question_list):
        ans = input(f"{q}\nYour answer: ").strip()
        if ans.lower() in ["stop", "quit", "exit"]:
            print("Exiting Bingo early.\n")
            break
        if ans.lower() == a.lower():
            print("Correct! You filled a space!\n")
            answered[grid_mapping[q_idx]] = True
        else:
            print(f"Incorrect! The correct answer was: {a}\n")
        display_grid()
        if not bingo_achieved and check_bingo():
            print("Bingo! You got 5 in a row!\n")
            bingo_achieved = True

    total_filled = sum(answered)
    print(f"You filled {total_filled} spaces.\n")

def magic8ball(questions):
    print("\n--- MAGIC 8 BALL ---")
    print("Shake the 8 ball to get a reversed answer! Type 'exit' to stop.\n")
    if not questions:
        print("No questions available.\n")
        return
    while True:
        q, a = random.choice(list(questions.items()))
        res = input("Shake the 8 ball (press Enter or type 'exit'): ").strip().lower()
        if res in ["exit", "quit", "stop"]:
            print("Exiting Magic 8 Ball...\n")
            break
        print(f"\n{a} is {q}\n")

def view_questions(questions):
    if not questions:
        print("No questions available.\n")
        return
    print("\n--- VIEW QUESTIONS ---")
    for i, (q, a) in enumerate(questions.items(), 1):
        print(f"{i}. Q: {q}\n   A: {a}")
    print()

def edit_questions(questions):
    if not questions:
        print("No questions to edit.\n")
        return questions
    while True:
        print("\n--- EDIT OR DELETE QUESTIONS ---")
        for i, (q, a) in enumerate(questions.items(), 1):
            print(f"{i}. Q: {q}\n   A: {a}")
        print(f"{len(questions)+1}. Add a new question")
        print(f"{len(questions)+2}. Return to menu")
        choice = input("\nChoose a number: ").strip()
        if not choice.isdigit():
            print("Whoopsie, that wasn't expected.\n")
            continue
        choice = int(choice)
        if choice == len(questions) + 1:
            q = input("Enter the new question: ").strip()
            a = input("Enter the new answer: ").strip()
            questions[q] = a
            print("Question added!\n")
        elif choice == len(questions) + 2:
            break
        elif 1 <= choice <= len(questions):
            action = input("Type 'edit' to modify or 'delete' to remove: ").strip().lower()
            key = list(questions.keys())[choice - 1]
            if action == "edit":
                new_q = input("New question (leave blank to keep current): ").strip()
                new_a = input("New answer (leave blank to keep current): ").strip()
                if new_q:
                    questions[new_q] = questions.pop(key)
                    key = new_q
                if new_a:
                    questions[key] = new_a
                print("Question updated!\n")
            elif action == "delete":
                del questions[key]
                print("Question deleted!\n")
            else:
                print("Whoopsie, that wasn't expected.\n")
        else:
            print("Whoopsie, that wasn't expected.\n")
    return questions

def main():
    questions = add_questions()
    while True:
        print("*********NOTES**************")
        print('Typing "Exit" within a program will return to Main Menu')
        print("========= MAIN MENU =========")
        print("1. Open-Ended Quiz")
        print("2. True/False Quiz")
        print("3. Multiple Choice Quiz (needs at least 4 questions for full mode)")
        print("4. Flashcards")
        print("5. Jeopardy Game")
        print("6. Bingo Game (needs at least 25 questions for full mode)")
        print("7. Magic 8 Ball")
        print("8. View Questions")
        print("9. Add/Edit/Delete Questions")
        print("10. Exit (ALL DATA WILL BE ERASED)")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            open_quiz(questions)
        elif choice == "2":
            true_false_quiz(questions)
        elif choice == "3":
            multiple_choice_quiz(questions)
        elif choice == "4":
            flashcards(questions)
        elif choice == "5":
            jeopardy(questions)
        elif choice == "6":
            bingo(questions)
        elif choice == "7":
            magic8ball(questions)
        elif choice == "8":
            view_questions(questions)
        elif choice == "9":
            questions = edit_questions(questions)
        elif choice == "10":
            print("\nGood luck on your exam!\n")
            break
        else:
            print("Whoopsie, that wasn't expected.\n")

if __name__ == "__main__":
    main()
