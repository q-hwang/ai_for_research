from literature_review import arxiv_literature_review
from understand_long_file import understand_file

# generate a literature review report by searching for papers on arxiv
report = arxiv_literature_review('quantum computing', max_results=5)
print(report)

# generate a summary of the arxiv API reference about how to search for papers
summary = understand_file('arxiv_API_reference.txt', 'how to use the arxiv API to search for papers')
print(summary)

