import re

def safe_eval_survey(formula_str):
    """
    Safely evaluates basic algebraic mathematical expressions representing 
    indirect attainment survey inputs (e.g. '((46/50)*3+(4/50)*2)').
    Only permits mathematical operators, parentheses, decimal numbers, and whitespaces.
    """
    if not formula_str:
        return 0.0
        
    formula_str = str(formula_str).replace('=', '').strip()
    
    # Safe validation using whitelist characters
    allowed_chars = set("0123456789.+-*/() ")
    if not all(c in allowed_chars for c in formula_str):
        return 0.0
        
    try:
        # Evaluate in an isolated context with absolutely no builtins
        val = eval(formula_str, {"__builtins__": None}, {})
        return float(val)
    except Exception:
        return 0.0

def calculate_co_attainment(students, survey_inputs):
    """
    Performs pure Python calculations of direct, indirect, and combined CO attainments.
    Useful for populating the database and rendering Chart.js visualizations dynamically.
    """
    total_students = len(students)
    if total_students == 0:
        return {
            'student_count': 0,
            'direct': 0.0,
            'attainments': {f"CO{i}": {'direct': 0.0, 'indirect': 0.0, 'final': 0.0} for i in range(1, 6)}
        }
        
    # Calculate direct levels for each student based on their marks sum
    direct_levels = []
    for s in students:
        tot_mark = round(s['viva_10'] + s['day_to_day_10'] + s['int_10'] + s['lab_project_10'] + s['end_sem_60'], 0)
        
        # Threshold logic: >=80 is Level 3, >=60 is Level 2, <60 is Level 1
        if tot_mark >= 80:
            lvl = 3
        elif tot_mark >= 60:
            lvl = 2
        else:
            lvl = 1
        direct_levels.append(lvl)
        
    # Direct Attainment Average (same for all COs in this LAB scheme)
    direct_avg = sum(direct_levels) / total_students
    
    # Calculate outcomes for each of the 5 COs
    co_outcomes = {}
    for i in range(1, 6):
        co_key = f"CO{i}"
        survey_formula = survey_inputs.get(co_key, "0")
        indirect_val = safe_eval_survey(survey_formula)
        
        final_val = 0.8 * direct_avg + 0.2 * indirect_val
        
        co_outcomes[co_key] = {
            'direct': round(direct_avg, 4),
            'indirect': round(indirect_val, 4),
            'final': round(final_val, 4)
        }
        
    return {
        'student_count': total_students,
        'direct_avg': round(direct_avg, 4),
        'attainments': co_outcomes
    }
