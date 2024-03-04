from flask import Flask, render_template, request
import csv
from itertools import combinations

app = Flask(__name__)

def negative_match(keyword):
    return f"-{keyword}"

def exact_match(keyword):
    return f"[{keyword}]"

def phrase_match(keyword):
    return f'"{keyword}"'

def process_keywords(keywords, match_type):
    processed_keywords = []
    for keyword in keywords:
        if match_type == 'negative':
            processed_keywords.append(negative_match(keyword).lower())
        elif match_type == 'exact':
            processed_keywords.append(exact_match(keyword).lower())
        elif match_type == 'phrase':
            processed_keywords.append(phrase_match(keyword).lower())
        # Add more custom match types here if needed
    return processed_keywords

def suggest_keywords_mix(keywords):
    phrase_keywords = [keyword for keyword in keywords if '"' in keyword]
    exact_keywords = [keyword for keyword in keywords if '[' in keyword]
    negative_keywords = [keyword for keyword in keywords if '-' in keyword]

    max_combinations = 60
    max_per_type = 20

    best_combinations = []
    for phrase_comb in combinations(phrase_keywords[:max_per_type], 1):
        for exact_comb in combinations(exact_keywords[:max_per_type], 1):
            for negative_comb in combinations(negative_keywords[:max_per_type], 1):
                mix = ' '.join(phrase_comb + exact_comb + negative_comb)
                best_combinations.append(mix)
                if len(best_combinations) >= max_combinations:
                    return best_combinations
    return best_combinations


def export_keywords_to_csv(keywords, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Match Type', 'Keyword'])
        for keyword in keywords:
            writer.writerow([keyword[0], keyword[1]])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords_input = request.form['keywords']
        keywords = [keyword.strip() for keyword in keywords_input.split('\n') if keyword.strip()]
        match_types = ['negative', 'exact', 'phrase']
        
        processed_keywords = {}
        for match_type in match_types:
            processed_keywords[match_type] = process_keywords(keywords, match_type)

        best_mix_keywords = suggest_keywords_mix(keywords)
        return render_template('result.html', processed_keywords=processed_keywords, best_mix_keywords=best_mix_keywords)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    flask run --host=0.0.0.0
