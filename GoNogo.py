import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import sys
import csv

"""The Go/NoGo paradigm requires the user to press Enter when a Go symbol appears, or withheld from responding if a NoGo symbol appears"""


def main():
    print('\n📍 Whenever you see 🔲 you must press Enter, while if you see 🔳 you must not press any key')
    Start = input("📍 When you are ready press 's' and Enter to start: ")
    if Start == "s" or Start == "S":
        Data = GoNogo(20, 1)
        Data, FaultyTrials = Faulty_Trials(Data)
        Stats = Statistics(Data)
        results_file(Data, Stats, FaultyTrials)
    else:
        sys.exit('Please press "s" to start')


def GoNogo(Times: int, Timer: int):
    global Data
    Data = []
    if Times > 0 and Timer > 0:
        Trial = 0
        Symbols = ["🔲", "🔳"]
        for _ in range(Times):
            Trial += 1
            Stimuli = random.choices(Symbols, weights=[1, 4], k=1)[0]
            print(Stimuli)
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
            Data.append({"Trial": Trial, "Stimuli": Stimuli,
                        "Answer": Answer, "RT(ms)": Reaction_Time})
    else:
        sys.exit('Times and Timer must be greater than 0')

    return Data


# Data analysis
def Faulty_Trials(Data: list):
    global FaultyTrials
    FaultyTrials = []
    ValidTrials = []

    for trial in Data:
        if trial["Answer"] != "Withheld" and trial["Answer"] != "Pressed":
            FaultyTrials.append(trial)
        else:
            ValidTrials.append(trial)

    Data = ValidTrials
    return Data, FaultyTrials


def Statistics(Data: list):
    global Accuracy, Hit_Rate, Miss_Rate, False_Alarm_Rate, Mean_RT, Stats

    True_positive = 0
    True_negative = 0
    False_positive = 0
    False_negative = 0
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

    Stats = {
        "Accuracy": f"{Accuracy}%",
        "Hit Rate": f"{Hit_Rate}%",
        "Miss Rate": f"{Miss_Rate}%",
        "False Alarm Rate": f"{False_Alarm_Rate}%",
        "Mean RT (ms)": f"{Mean_RT}ms"
    }

    return Stats


# CSV file creation
def results_file(Data: list, Stats: dict, FaultyTrials: list):

    with open('GoNogo_results.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=Data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(trial for trial in Data)

        output_file.write('\n')

        stat_writer = csv.writer(output_file)
        stat_writer.writerow(Stats.keys())
        stat_writer.writerow(Stats.values())

        output_file.write('\n')

        if FaultyTrials:
            faulty_writer = csv.DictWriter(
                output_file, fieldnames=FaultyTrials[0].keys())
            faulty_writer.writeheader()
            faulty_writer.writerows(trial for trial in FaultyTrials if trial)

    print("File created: GoNogo_results.csv")
    return


if __name__ == "__main__":
    main()
