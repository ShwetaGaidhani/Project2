from typing import Set, List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
import difflib


VALID_SYMPTOMS = [
"fever","cough","sore_throat","runny_nose","headache","fatigue",
"body_ache","shortness_of_breath","sneezing","chills",
"loss_of_smell","loss_of_taste","nausea","vomiting",
"diarrhea","chest_pain","dizziness","high_fever",
"dry_cough","muscle_pain"
]


@dataclass
class Rule:
    conditions: List[str]
    conclusions: List[str]
    description: str


class ExpertSystem:

    def __init__(self):
        self.facts: Set[str] = set()
        self.rules: List[Rule] = []
        self.inference_log: List[Dict] = []
        self.derived_facts: Set[str] = set()
        self.rules_applied = 0
        self.iterations = 0

    def add_fact(self, fact: str):
        fact = fact.lower().replace(" ","_")
        self.facts.add(fact)

    def remove_fact(self, fact: str):
        fact = fact.lower().replace(" ","_")
        self.facts.discard(fact)
        self.derived_facts.discard(fact)

    def add_rule(self, conditions: List[str], conclusions: List[str], description: str):
        rule = Rule(
            [c.lower() for c in conditions],
            [c.lower() for c in conclusions],
            description
        )
        self.rules.append(rule)

    def check_conditions(self, rule: Rule):
        return all(cond in self.facts for cond in rule.conditions)

    def log(self, message: str):
        self.inference_log.append({
            "time": datetime.now().isoformat(),
            "message": message
        })

    def forward_chaining(self):

        self.derived_facts.clear()
        self.inference_log.clear()

        print("\nStarting inference")
        print("Initial facts:", ", ".join(self.facts))

        new_fact = True

        while new_fact:

            new_fact = False
            self.iterations += 1

            for i, rule in enumerate(self.rules,1):

                if self.check_conditions(rule):

                    for conclusion in rule.conclusions:

                        if conclusion not in self.facts:

                            self.facts.add(conclusion)
                            self.derived_facts.add(conclusion)
                            new_fact = True
                            self.rules_applied += 1

                            print(f"Rule {i} -> {conclusion}")

                            self.log(
                                f"{rule.conditions} -> {conclusion}"
                            )

        print("\nInference finished")

        self.print_summary()

    def print_summary(self):

        print("\nSummary")
        print("Iterations:",self.iterations)
        print("Rules applied:",self.rules_applied)
        print("Derived facts:",len(self.derived_facts))
        print("All facts:",",".join(self.facts))

    def get_diagnosis(self) -> List[Tuple[str,str]]:

        diagnoses=[]

        if "flu" in self.facts:
            diagnoses.append(("Flu",
            "Rest, drink fluids, and monitor temperature."))

        if "common_cold" in self.facts:
            diagnoses.append(("Common Cold",
            "Usually resolves in few days with rest."))

        if "viral_infection" in self.facts:
            diagnoses.append(("Viral Infection",
            "Supportive care recommended."))

        if "bacterial_infection" in self.facts:
            diagnoses.append(("Bacterial Infection",
            "Consult doctor for antibiotics."))

        if "covid_risk" in self.facts:
            diagnoses.append(("Possible COVID Symptoms",
            "Isolate and consider medical testing."))

        if "food_poisoning" in self.facts:
            diagnoses.append(("Food Poisoning",
            "Drink fluids and consult doctor if severe."))

        if "cardiac_risk" in self.facts:
            diagnoses.append(("Heart Risk",
            "Seek immediate medical attention."))

        return diagnoses

    def print_diagnosis(self):

        result=self.get_diagnosis()

        print("\nDiagnosis")

        if not result:
            print("No clear diagnosis")
        else:
            for i,(title,desc) in enumerate(result,1):
                print(f"{i}. {title} - {desc}")

    def export_log(self):

        with open("inference_log.txt","w") as f:

            for entry in self.inference_log:

                f.write(
                    f"{entry['time']} - {entry['message']}\n"
                )

        print("Log exported to inference_log.txt")

    def reset(self):

        self.facts.clear()
        self.derived_facts.clear()
        self.inference_log.clear()
        self.iterations=0
        self.rules_applied=0


def initialize_medical_knowledge_base(es):

    es.add_rule(["fever","cough"],["respiratory_infection"],"Respiratory infection")

    es.add_rule(["respiratory_infection","sore_throat"],["flu"],"Flu case")

    es.add_rule(["fever","headache","body_ache"],["viral_infection"],"Viral infection")

    es.add_rule(["runny_nose","sore_throat"],["common_cold"],"Common cold")

    es.add_rule(["viral_infection","fatigue"],["flu"],"Flu progression")

    es.add_rule(["cough","shortness_of_breath"],["severe_respiratory_issue"],"Respiratory distress")

    es.add_rule(["severe_respiratory_issue"],["severe_condition"],"Severe condition")

    es.add_rule(["fever","severe_condition"],["critical_condition"],"Critical case")

    es.add_rule(["sore_throat","fever"],["possible_bacterial_throat_infection"],"Bacterial throat infection")

    es.add_rule(["possible_bacterial_throat_infection"],["bacterial_infection"],"Bacterial infection")

    es.add_rule(["fever","chills"],["infection"],"General infection")

    es.add_rule(["dry_cough","loss_of_smell"],["covid_like_symptoms"],"Covid symptoms")

    es.add_rule(["covid_like_symptoms","fever"],["covid_risk"],"Covid risk")

    es.add_rule(["vomiting","diarrhea"],["food_poisoning"],"Food poisoning")

    es.add_rule(["chest_pain","shortness_of_breath"],["cardiac_risk"],"Heart risk")


def smart_input(symptom):

    symptom=symptom.lower().replace(" ","_")

    match=difflib.get_close_matches(symptom,VALID_SYMPTOMS,n=1,cutoff=0.6)

    if match:
        return match[0]

    return None


def interactive_mode():

    es=ExpertSystem()

    initialize_medical_knowledge_base(es)

    print("Rule Based Expert System")

    while True:

        print("\n1 Add symptom")
        print("2 Remove symptom")
        print("3 View symptoms")
        print("4 Run diagnosis")
        print("5 Export log")
        print("6 Reset system")
        print("7 Load example")
        print("8 Show symptoms list")
        print("9 Exit")

        choice=input("Choice: ")

        if choice=="1":

            symptom=input("Enter symptom: ")

            s=smart_input(symptom)

            if s:
                es.add_fact(s)
                print("Added:",s)
            else:
                print("Unknown symptom")

        elif choice=="2":

            es.remove_fact(input("Symptom to remove: "))
            print("Removed")

        elif choice=="3":

            if not es.facts:
                print("No symptoms")
            else:
                for f in es.facts:
                    tag="derived" if f in es.derived_facts else "input"
                    print(f"{f} ({tag})")

        elif choice=="4":

            if not es.facts:
                print("Add symptoms first")
            else:
                es.forward_chaining()
                es.print_diagnosis()

        elif choice=="5":

            es.export_log()

        elif choice=="6":

            es.reset()
            print("System reset")

        elif choice=="7":

            es.reset()

            for s in ["fever","cough","sore_throat"]:
                es.add_fact(s)

            print("Example loaded")

        elif choice=="8":

            print("\nAvailable symptoms:")
            for s in VALID_SYMPTOMS:
                print("-",s)

        elif choice=="9":

            print("Exit")
            break


if __name__=="__main__":
    interactive_mode()