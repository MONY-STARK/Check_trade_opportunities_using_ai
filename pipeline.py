# pipeline.py

import os
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from google import genai
from dotenv import load_dotenv

load_dotenv()


class TradePipeline:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3-flash-preview"



    def search_sector(self, sector: str) -> list:
        query = f"India {sector} sector trade opportunities 2024"
        results = DDGS().text(query, max_results=5)
        return results


    def extract_text_from_url(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0"
            })
            soup = BeautifulSoup(response.text, "lxml")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return " ".join(lines)[:2000]

        except:
            return ""

   

    def collect_data(self, sector: str) -> str:
        search_results = self.search_sector(sector)
        all_text = ""

        for result in search_results:
            all_text += f"\nSource: {result['title']}\n"
            all_text += f"Summary: {result['body']}\n"

            full_text = self.extract_text_from_url(result["href"])
            if full_text:
                all_text += f"Details: {full_text}\n"

            all_text += "---\n"

        return all_text



    def generate_report(self, sector: str, data: str) -> str:
        prompt = f"""
You are a senior trade analyst specializing in Indian markets.

Based on the following real data collected from the web:

{data}

Generate a detailed markdown report for India's {sector} sector.

Use EXACTLY this structure:

# {sector.title()} Sector — India Trade Opportunity Report

## Executive Summary
[3-4 lines about the sector]

## Current Market Trends
- [trend 1 with numbers]
- [trend 2 with numbers]
- [trend 3 with numbers]
- [trend 4 with numbers]
- [trend 5 with numbers]

## Trade Opportunities
### Opportunity 1: [Name]
- Type: Export / Import / Investment
- Market Size: [number]
- Target Markets: [countries]
- Why Now: [reason]

### Opportunity 2: [Name]
[same structure]

### Opportunity 3: [Name]
[same structure]

## Risks & Challenges
| Risk | Severity | How to Handle |
|------|----------|---------------|
| [risk 1] | High/Medium/Low | [solution] |
| [risk 2] | High/Medium/Low | [solution] |
| [risk 3] | High/Medium/Low | [solution] |

## Government Policies & Support
- [policy 1]
- [policy 2]
- [policy 3]

## Recommendations
1. Short term (0-6 months): [action]
2. Medium term (6-18 months): [action]
3. Long term (18+ months): [action]

Be specific. Use real numbers from the data provided.
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text

        except Exception as e:
            error_msg = str(e)

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                return f"# {sector.title()} Sector Report\n\n## ⚠️ Quota Exceeded\n\nGemini API quota exceeded. Please wait 30 seconds and try again."

            return f"# Error\n\nFailed to generate report: {error_msg}"

   

    def analyze(self, sector: str) -> str:
        print(f"Collecting data for: {sector}")
        data = self.collect_data(sector)

        print(f"Generating report...")
        report = self.generate_report(sector, data)

        return report