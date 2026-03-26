# Project2
# Rule-Based Expert System

## Overview
This project implements a **Rule-Based Expert System** using Python.  
The system simulates human expert reasoning by applying **if–then rules** on a **facts base**.  
It accepts symptoms from the user and uses **forward chaining inference** to derive conclusions.

The system also logs each inference step so users can understand how the final conclusion was reached.


## Objectives
The main objectives of this project are:

- Build a **rule engine** using if–then rules
- Maintain a **facts base** for storing user inputs
- Implement **forward chaining inference**
- Support **multi-step rule chaining**
- Display **reasoning steps (inference log)**
- Provide **diagnosis suggestions based on symptoms**


## Features

- Rule-Based Knowledge System
- Symptom Input from User
- Forward Chaining Inference
- Multi-step Reasoning
- Inference Logging
- Typo-tolerant Symptom Input
- Symptom Suggestion List
- Medical Advice Based on Diagnosis


## System Architecture

The expert system consists of the following components:

1. **Facts Base**
   - Stores user-provided symptoms.

2. **Rule Base**
   - Contains IF–THEN rules used for reasoning.

3. **Inference Engine**
   - Applies forward chaining to derive conclusions.

4. **Explanation Module**
   - Logs which rules were triggered during reasoning.


## How the System Works

1. The user enters symptoms.
2. The symptoms are stored as facts.
3. The rule engine checks rules whose conditions match the facts.
4. If a rule condition is satisfied, the rule fires.
5. The rule produces a new fact.
6. This process continues until no more rules can fire.
7. The system displays:
   - Inference steps
   - Final diagnosis
   - Medical suggestions
