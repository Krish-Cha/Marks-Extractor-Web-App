from django.shortcuts import render

# Create your views here.

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def extract_marks_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example selectors (replace these with real selectors after inspecting the result page)
        name = soup.select_one(".candidate-name").text.strip() if soup.select_one(".candidate-name") else "N/A"
        roll = soup.select_one(".roll-number").text.strip() if soup.select_one(".roll-number") else "N/A"

        subjects = []
        total_marks = 0

        for row in soup.select("table tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                subject = cols[0].text.strip()
                marks = int(cols[1].text.strip())
                subjects.append({"subject": subject, "marks": marks})
                total_marks += marks

        return {
            "name": name,
            "roll": roll,
            "subjects": subjects,
            "total": total_marks
        }
    except Exception as e:
        print("Error:", e)
        return None

def index(request):
    result_data = None
    if request.method == "POST":
        url = request.POST.get("result_url")
        result_data = extract_marks_from_url(url)
    return render(request, 'index.html', {'result_data': result_data})
