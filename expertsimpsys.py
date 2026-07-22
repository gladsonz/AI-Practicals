decision_tree = {
    "question":"Engine won't start?",
    "yes":{
        "question":"Battery warning light on?",
        "yes":"Dead or weak battery",
        "no":"Starter motor or ignition problem"
    },
    "no":{
        "question":"High temperature gauge?",
        "yes":"Engine overheating",
        "no":"No clear issue found"
    }
}

def expert(tree):

    if type(tree)==str:
        print("\nDiagnosis:",tree)
        return

    ans=input(tree["question"]+" (y/n): ").lower()

    if ans=="y":
        expert(tree["yes"])
    else:
        expert(tree["no"])

print("Vehicle Expert System")
expert(decision_tree)