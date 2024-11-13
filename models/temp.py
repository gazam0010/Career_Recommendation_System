import json

# Sample JSON data
quiz_json = '''
{
  "quiz": [
    {
      "question": "Which of the following is NOT a core concept in Artificial Intelligence?",
      "options": ["Machine Learning", "Deep Learning", "Natural Language Processing", "Quantum Physics"]
    },
    {
      "question": "What does AI stand for?",
      "options": ["Artificial Intelligence", "Advanced Intelligence", "Applied Informatics", "Algorithmic Innovation"]     
    },
    {
      "question": "Which programming language is widely used in AI development?",
      "options": ["Python", "Java", "C++", "All of the above"]
    },
    {
      "question": "What is a common application of AI in the computer industry?",
      "options": ["Cybersecurity threat detection", "Software development automation", "Data center optimization", "All of the above"]
    },
    {
      "question": "What type of learning algorithm uses labeled data to train a model?",
      "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "None of the above"]
    },
    {
      "question": "A neural network is a type of:",
      "options": ["Machine Learning model", "Data structure", "Programming language", "Algorithm"]
    },
    {
      "question": "Which of the following is an example of a supervised learning task?",
      "options": ["Image classification", "Clustering", "Dimensionality reduction", "Anomaly detection"]
    },
    {
      "question": "In the context of AI, what does NLP stand for?",
      "options": ["Natural Language Processing", "Neural Language Programming", "Network Logic Processing", "None of the above"]
    },
    {
      "question": "What is a common challenge in AI development?",
      "options": ["Data scarcity", "Computational cost", "Model interpretability", "All of the above"]
    },
    {
      "question": "Which of these is NOT a typical area of application for AI in the computer industry?",
      "options": ["Hardware design", "Operating system development", "Spreadsheet creation", "Network management"]
    }
  ]
}
'''

# Parse the JSON string
quiz_dict = json.loads(quiz_json)

# Print the parsed dictionary
print(quiz_dict)
