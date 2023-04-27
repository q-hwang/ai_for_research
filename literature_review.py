import requests   
import json
import sys
from LLM import complete_text_fast


def search_arxiv(query, max_results=10):       
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.text
    return data
          

def parse_arxiv_data(data):  

    from xml.etree import ElementTree as ET
    root = ET.fromstring(data)
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    result = []
    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text
        result.append({'title': title, 'authors': authors, 'abstract': abstract})
    return result

def generate_summary(prompt, model='Claude'):  
    summary = complete_text_fast(prompt=prompt, max_tokens_to_sample=1000)
    return summary

def arxiv_literature_review(query, max_results=10):

     # Call the arxiv API and get the results 
    xml_data = search_arxiv(query, max_results)
    data = parse_arxiv_data(xml_data)
    
    # Process the results and generate the report
    report = 'Literature Review Report\n\n'
    report += 'Query: {}\n\n'.format(query)
    report += 'List of Papers:\n\n'  
    
    summaries = []
    for idx, paper in enumerate(data):
        title = paper['title']
        authors = ', '.join(paper['authors'])
        abstract = paper['abstract']
        report += 'Title: {}\nAuthors: {}\nAbstract: {}\n\n'.format(title, authors, abstract)  
            
        # Generate a summary of the paper using the LLM
        prompt = 'Please summarize the paper "{}" by {} with the following abstract: {}'.format(title, authors, abstract)
        summary = generate_summary(prompt)
        summaries.append('[{}] Title: {}\n Summary: {}\n\n'.format(idx+1,title, summary))
        report += 'Summary: {}\n\n'.format(summary)
            
    report += 'Conclusion of the Literature Review:\n\n'
    prompt = 'Please provide a overall literature review on the topic "{}" based on the summaries of the papers. Refer to the given paper ids to support each point.\n'.format(query)
    prompt += "".join(summaries)
    conclusion = generate_summary(prompt)
    report += conclusion
        
    return report

if __name__ == '__main__':
    example_query = 'Language model hallucination detection'
    result = arxiv_literature_review(example_query)
    print(result)