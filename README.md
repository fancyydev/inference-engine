# inference-engine
## Description
This is a python implementation of an inference engine that uses the and operator to obtain a conclusion using two algorithms: backward chaining and forward chaining.
## Requirements
Here are the recommended versions to use. If you have a different version of Python, feel free to try it. If the program does not work, try using the same version or a similar version.
- Python 3.12.4

## Installation
For this program, you don't need to create a virtual environment because the only package it uses is tkinter, which is a default Python package.
### Download
- **Option 1:** Download the code as a ZIP file directly from the repository.
- **Option 2:** Use Git Bash to clone the repository with the following command.
```bash
git clone https://github.com/fancyydev/inference-engine.git
```
## Running the program
To run and test the inference engine using the terminal, navigate to the project directory and execute:
```
python .\engine.py
```

## Explanation

### Indications
Inference Engine Program 

**Description:**

Create a program that allows evaluating a production system through the algorithms of forward-chaining and backward-chaining. 

**Inputs:** 
- The production system to evaluate (set of rules) (it can be captured or edited in a text file; in both cases, the syntax for its capture must be indicated to the user). 
- Any number of antecedents (1 to n) connected only by the logical connector and (and, conjunction) may be used, and there will only be one consequent per rule. 
- The initial fact base. 
- The goal. 
- The option of the mechanism by which the goal will be evaluated (forward chaining or backward-chaining). 
- It will be left open for the user to make changes to these input elements. 

**Process and intermediate outputs:** 

As the process of verifying and validating that the goal has been derived from the production system in question progresses, the status of the sets and elements involved in the process (conflict set, selected rule, fired rule, goal, new goals, fact base) must be displayed according to the chaining selected for this evaluation. 

**Output:** 
- Indicate whether the validation of the goal was successful or unsuccessful. 
- Indicate the rules that were fired to achieve the stated goal.

### Algorithms
**Forward-Chaining**

This algorithm repeatedly applies the rules from the Knowledge Base (BC) until no new facts (NH) are generated. A rule can be applied if all the clauses in its antecedent are satisfied, considering the content of the Fact Base (BH). In other words, a rule fires if all its antecedents are contained within the BH. Each time a rule is applied, the results of the actions from its consequent are stored as new facts in the BH.

Pseudocode:
```
ForwardChainingAlgorithm
Start
    BC = TotalRules;
    BH = InitialFacts;
    Goal = GoalObjective;
    CC = Match(Antecedents(BC), BH);
    while NotEmpty(CC) and NotContained(Goal, BH) do
    Start
        R = Resolve(CC);
        Remove(R, CC);
        Remove(R, BC);
        NH = Apply(R, BH);
        Update(BH, NH);
        if NotContained(Goal, BH)
            CC = Match(Antecedents(BC), BH);
    End
    if Contained(Goal, BH)
        if yes, return "success";
    else return "failure";
End
```

**Backward-Chaining**

This algorithm works inversely to the forward-chaining algorithm. In this case, it initially analyzes the rules whose consequent matches the Goal (Meta). If the antecedents of such a rule are contained in the Fact Base (BH), the rule fires, and the goal is stored in the BH. Otherwise, if some or all the antecedents are not present in the BH, these antecedents now become new sub-goals (NM) to be searched for and satisfied. Once satisfied, they are added to the BH, allowing the original goal to be validated.

Pseudocode:
```

BackwardChainingAlgorithm
Start
    BH = InitialFacts;
    Goal = GoalObjective;
    if Verify(Goal, BH)
        if yes, return "success";
    else
        return "failure";
End

Procedure Verify(Goal, BH): boolean
Start
    BC = TotalRules;
    verified = false;
    if Contains(Goal, BH)
        if yes, return true;
    else Start
        CC = Match(Consequents(BC), Goal);
        while NotEmpty(CC) and Not(verified) do
        Start
            if Contains(Goal, Antecedents(CC[0]))
                if yes
                    Remove(CC[0], CC);
                    Remove(CC[0], BC);
            
            R = Resolve(CC);
            Remove(R, CC);
            NM = ExtractAntecedents(R);
            verified = true;
            while NotEmpty(NM) and verified do
            Start
                Goal = SelectGoal(NM);
                Remove(Goal, NM);
                verified = Verify(Goal, BH);
                if verified
                    if yes, Add(Goal, BH);
                else
                    Update(BH, Goal);
            End
        End
        Return(verified);
    End
End
```


### Glosary
- BH (Initial Facts): The set of facts that are known or assumed to be true at the start of the process.

- BC (Knowledge Base): The complete set of production rules available in the system. These rules are used to derive new facts or validate the goal.

- CC (Conflict Set): A set of rules from the knowledge base whose antecedents match the current facts in the fact base (BH).

- Goal (Meta): The target or objective that needs to be verified or derived from the production system.

- R (Selected Rule): The rule chosen from the conflict set (CC) for evaluation or firing during the process.

- NM (New Goals): A set of sub-goals composed of the antecedents of the selected rule (R). These antecedents must be satisfied (contained in BH) for the rule to fire.

- NH (New Facts): New facts derived by applying a selected rule (R) to the current fact base (BH). These are added to the fact base after firing the rule.

- verified: A boolean variable that indicates the success or failure of the search for the goal in the production system. It represents the result of the evaluation, determining whether the goal was derived from the production system.


