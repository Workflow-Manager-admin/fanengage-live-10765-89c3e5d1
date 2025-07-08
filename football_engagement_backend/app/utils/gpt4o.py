import openai
import os

# PUBLIC_INTERFACE
def set_gpt_apikey():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key

# PUBLIC_INTERFACE
def generate_yesno_questions(transcript: str, num_questions:int=3) -> list:
    """
    Generate yes/no questions relevant to football commentary using GPT-4o-mini.
    Returns a list of questions.
    """
    set_gpt_apikey()
    prompt = (
        f"Generate {num_questions} interesting yes/no questions for fans, "
        "based on the following football match transcript (commentary), focusing on engagement and match events. "
        "Questions must be answerable by a simple yes or no.\n\n"
        f"TRANSCRIPT:\n{transcript}\n\n"
        "QUESTIONS:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful football engagement assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.8,
        n=1,
    )
    text = response.choices[0].message['content'].strip()
    qlist = []
    for line in text.split('\n'):
        if '?' in line:
            question = line.split('?', 1)[0].strip()
            qlist.append(question + "?")
    return qlist[:num_questions]

# PUBLIC_INTERFACE
def generate_analysis(question: str, results: dict) -> str:
    """
    Generate a short analysis for a question based on user yes/no counts using GPT-4o-mini.
    Args:
        question: The question text.
        results: Dict of {'yes': int, 'no': int}
    Returns:
        str: The analysis/summary.
    """
    set_gpt_apikey()
    prompt = (
        f"Question for fans: {question}\n"
        f"Results: Yes - {results.get('yes', 0)}, No - {results.get('no',0)}\n"
        "Write a 2-3 sentence analysis summarizing what this says about the fans' opinions or excitement about the match."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful football engagement analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
        n=1,
    )
    return response.choices[0].message['content'].strip()
