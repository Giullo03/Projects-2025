# Go/NoGo task: implementation and data analysis
### Video Demo: <>
#### Description:
The Go/NoGo task is a type of task used in cognitive sciences to assert the subjects' reaction time to certain stimuli. Each user is askedto press a specific button whenever a specific stimuli appears on screen (Go stimuli), but responses must be withhold for any other stimuli (NoGo stimuli).

This project implements the same task using python in order to directly collect data from users and immediately carry out analysis on such data. In particular the following measures are calculated:
- Acccuracy: the proportion of right answers given across all trials
- Hit_Rate: the proportion of right answers given to Go stimuli across all Go stimuli
- Miss_Rate: the proportion of wrong answers given to Go stimuli (withhelding response) across all Go stimuli
- False_Alarm_Rate: the proportion of wrong answers given to NoGo stimoli (pressing the button when a NoGo stimuli appears) across all NoGo stimuli
- Mean_RT: the mean of all reaction times to Go stimuli

The program begins with asking the user to press "s" ("S" is also accepted) when they are ready to start the task

```
print('\n📍 Whenever you see 🔲 you must press Enter, while if you see 🔳 you must not press any key')

Start = input("📍 When you are ready press 's' and Enter to start: ") 
```

Then the **GoNoGo function** is called, which starts by generating either Go or NoGo stimuli via weighted random generation. The number of stimuli generated can be decided by modifying the Times variable.
```
Symbols = ["🔲", "🔳"]
        for _ in range(Times):
            Trial += 1
            Stimuli = random.choices(Symbols, weights=[1, 4], k=1)[0]
            print(Stimuli)
```

The `inputimeout module` is implemented to give the user only a n second window to respond to the stimuli, where n can be decided by modifying the Timer variable. If the user presses Enter the answer will be memorizedas "Pressed", while if the user withheld the response (hence waits for the n seconds window to close) the answer will be memorized as "Withheld".
The time module is used to calculate the time passed between the moment the stimuli is given and the the moment th euser answers. This way,if the stimuli was a Go stimuli, we can calculate the reaction time:
```
start_Time = time.time()
            try:
                Answer = inputimeout(prompt="Answer: ", timeout=Timer)
                if Answer == "":
                    Answer = "Pressed"
            except TimeoutOccurred:
                Answer = "Withheld"
            end_Time = time.time()

            if Stimuli == "🔲":
                Reaction_Time = round((end_Time - start_Time)*1000, 1)
            else:
                Reaction_Time = ""
```

Data for each trials are stored in a dictionary called Data, containing: the number of the trial, the type of stimuli for that trial, the answer given to that trials, the reaction time (if any) in milliseconds:

```
Data.append({"Trial": Trial, "Stimuli": Stimuli,
                        "Answer": Answer, "RT(ms)": Reaction_Time})Data.append({"Trial": Trial, "Stimuli": Stimuli,
                        "Answer": Answer, "RT(ms)": Reaction_Time})
```

The **FaultyTrials function** collects faulty trials and valid trials in two different lists. Faulty trials are trials where the user has answered neither by pressing Enter or by waiting for the n seconds window to close. Only the valid trials list is then used to carry out data analysis.

The **Statistics function** performs statistical analysis to compute the measures listed above. It first comput the number of True Positive (right answers to Go stimuli), True Negative (right answers to NoGo stimuli), False Positive (wrong answers to Go stimuli), False Negative (wrong answers to NoGo stimuli). It then uses such data to compute the mentioned measures.
```
for trial in Data:
        if trial["Stimuli"] == "🔳" and trial["Answer"] == "Withheld":
            True_negative += 1
        if trial["Stimuli"] == "🔲" and trial["Answer"] != "Withheld":
            True_positive += 1
        if trial["Stimuli"] == "🔳" and trial["Answer"] != "Withheld":
            False_positive += 1
        if trial["Stimuli"] == "🔲" and trial["Answer"] == "Withheld":
            False_negative += 1

    try:
        Accuracy = round(((True_negative + True_positive)/(True_negative +
                                                           True_positive+False_negative+False_positive))*100, 2)
        Hit_Rate = round(
            (True_positive/(True_positive + False_negative)) * 100, 2)
        Miss_Rate = round(
            (False_negative/(True_positive + False_negative)) * 100, 2)
        False_Alarm_Rate = round(
            (False_positive/(True_negative + False_positive)) * 100, 2)
        Total_RT = [trial["RT(ms)"]
                    for trial in Data if trial["Stimuli"] == "🔲"]
        Mean_RT = round((sum(Total_RT)/len(Total_RT)), 1)
    except ZeroDivisionError:
        sys.exit("Error: Some trials may be invalid or missing")
```

The statistics are stored as a dictionary:
```
Stats = {
        "Accuracy": f"{Accuracy}%",
        "Hit Rate": f"{Hit_Rate}%",
        "Miss Rate": f"{Miss_Rate}%",
        "False Alarm Rate": f"{False_Alarm_Rate}%",
        "Mean RT (ms)": f"{Mean_RT}ms"
    }
```

Finally the **Result_file function** creates a GoNogo_results.csv file where the results of the data anlysis are reported, along with the list of all the faulty trials removed.
