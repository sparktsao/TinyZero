import re
import random
import ast
import operator

def extract_answer(solution_str):
    """Extracts the answer label from the provided solution string."""
    match = re.search(r'<answer>(.*?)</answer>', solution_str, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_answer(solution_str):
    """Extract the equation from the solution string."""
    # Remove everything before the first "Assistant:"
    if "Assistant:" in solution_str:
        solution_str = solution_str.split("Assistant:")[-1]
    elif "<|im_start|>assistant" in solution_str:
        solution_str = solution_str.split("<|im_start|>assistant")[-1]
    
    endofprompt = "(end of assistant example)\n<|im_end|>"
    if endofprompt in solution_str:
        print("SPARK:[do use END OD PROMPT to clean response]")
        solution_str = solution_str.split(endofprompt, 1)[1]
    #    return None, None
    #solution_str = solution_str.split('\n')[-1]
    # remove <|endoftext|>
    if "<|endoftext|>" in solution_str:
        location_of_end = solution_str.find("<|endoftext|>")
        solution_str = solution_str[:location_of_end]

    #answer_pattern = r'<answer>(.*?)</answer>'
    answer_pattern = r'<answer>\s*(.*?)\s*</answer>'
    match = re.finditer(answer_pattern, solution_str)
    matches = list(match)
    if matches:
        final_answer = matches[-1].group(1).strip()
        final_answer = final_answer.strip().replace("(","").replace(")","").replace("Final classification:","").strip()
    else:
        final_answer = None
    return solution_str, final_answer

def extract_plan(solution_str):
    """Extracts the plan section from the solution string."""
    match = re.search(r'<plan>(.*?)</plan>', solution_str, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_reasoning(solution_str):
    """Extracts the reasoning section from the solution string."""
    match = re.search(r'<validation>(.*?)</validation>', solution_str, re.DOTALL)
    return match.group(1).strip() if match else None

def compute_score(solution_str, ground_truth, format_score=0.1, correct_score=1.0):
    """Scoring function for scam evaluation task.
    
    Args:
        solution_str: The solution text containing <plan>, <reasoning>, and <answer>.
        ground_truth: Dictionary containing the expected answer label (SCAM/NORMAL/need more evidence).
        format_score: The score for correct format but incorrect answer.
        correct_score: The score for the correct answer.
    
    Returns:
        Score (0, format_score, or correct_score) based on correctness.
    """
    expected_answer = ground_truth.get('label')
    lena = len(solution_str)
    solution_str_extract, extracted_answer = extract_answer(solution_str)
    lenb = len(solution_str_extract)
    len_prompt = lena - lenb
    prompt = solution_str[:len_prompt]
    if solution_str_extract is None:
        print("extract_answer fail!!!!!!")
        print(solution_str)
        return 0
    else:
        solution_str = solution_str_extract # update
    extracted_plan = extract_plan(solution_str)
    extracted_reasoning = extract_reasoning(solution_str)
    
    do_print = random.randint(1, 8) == 1
    
    if do_print:
        print(f"--------------------------------")
        print(f"Prompt String:", {prompt})
        print(f"Solution String:", {solution_str})
        print(f"--------------------------------")
        print(f"Expected Answer: {expected_answer}")
        print(f"Extracted Answer: {extracted_answer}")
        print(f"--------------------------------")
        print(f"Extracted Plan: {extracted_plan}")
        print(f"Extracted validation: {extracted_reasoning}")
    
    # Validate the presence of required sections
    if not extracted_answer or not extracted_plan or not extracted_reasoning:
        if do_print:
            print("Missing required sections in the response")
        return 0
    
    extracted_answer = extracted_answer.strip().lower()
    expected_answer = expected_answer.strip().lower()
    
    # Validate correctness of the answer
    if extracted_answer == expected_answer:
        if do_print:
            print("Correct scam evaluation answer")
        return correct_score
    else:
        if do_print:
            print("Incorrect scam evaluation answer")
        return format_score
