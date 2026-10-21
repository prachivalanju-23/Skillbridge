import random

# d = difficulty (1 Beginner, 2 Intermediate, 3 Advanced), k = keywords used by the mock evaluator
BANK = {
    'Frontend Developer': [
        {'d': 1, 'q': 'What is React?', 'k': ['library', 'component', 'virtual dom', 'user interface', 'javascript']},
        {'d': 1, 'q': 'What is the difference between let, const and var?', 'k': ['scope', 'block', 'reassign', 'hoist']},
        {'d': 2, 'q': 'Explain the useEffect hook and when it runs.', 'k': ['side effect', 'dependency', 'render', 'cleanup', 'mount']},
        {'d': 2, 'q': 'What is the CSS box model?', 'k': ['content', 'padding', 'border', 'margin']},
        {'d': 3, 'q': 'How would you optimise the performance of a slow React app?', 'k': ['memo', 'usecallback', 'lazy', 're-render', 'split']},
        {'d': 3, 'q': 'Explain closures in JavaScript with an example.', 'k': ['function', 'scope', 'outer', 'variable', 'lexical']},
    ],
    'Backend Developer': [
        {'d': 1, 'q': 'What is a REST API?', 'k': ['http', 'resource', 'get', 'post', 'stateless']},
        {'d': 1, 'q': 'What is the role of middleware in a web framework?', 'k': ['request', 'response', 'function', 'route', 'process']},
        {'d': 2, 'q': 'How does JWT authentication work?', 'k': ['token', 'sign', 'secret', 'header', 'verify']},
        {'d': 2, 'q': 'What is the difference between SQL and NoSQL databases?', 'k': ['table', 'document', 'schema', 'scale', 'relational']},
        {'d': 3, 'q': 'How would you design a rate limiter for an API?', 'k': ['limit', 'window', 'redis', 'counter', '429']},
        {'d': 3, 'q': 'What is database indexing and when should you use it?', 'k': ['index', 'query', 'speed', 'search', 'write']},
    ],
    'Full Stack Developer': [
        {'d': 1, 'q': 'What is the difference between frontend and backend?', 'k': ['browser', 'server', 'database', 'interface', 'logic']},
        {'d': 1, 'q': 'What is an API and why do we use it?', 'k': ['request', 'response', 'data', 'endpoint', 'communicate']},
        {'d': 2, 'q': 'How does a React app communicate with a Django backend?', 'k': ['http', 'axios', 'fetch', 'json', 'endpoint']},
        {'d': 2, 'q': 'What is CORS and why is it needed?', 'k': ['origin', 'browser', 'header', 'policy', 'domain']},
        {'d': 3, 'q': 'How would you deploy a React and Django application to production?', 'k': ['build', 'environment', 'hosting', 'database', 'server']},
        {'d': 3, 'q': 'How do you handle authentication across frontend and backend?', 'k': ['token', 'login', 'protect', 'middleware', 'storage']},
    ],
    'Data Analyst': [
        {'d': 1, 'q': 'What is the difference between mean, median and mode?', 'k': ['average', 'middle', 'frequent', 'outlier']},
        {'d': 1, 'q': 'What is a primary key in a database?', 'k': ['unique', 'identify', 'row', 'table']},
        {'d': 2, 'q': 'Explain the difference between INNER JOIN and LEFT JOIN.', 'k': ['match', 'rows', 'null', 'table', 'left']},
        {'d': 2, 'q': 'How do you handle missing data in a dataset?', 'k': ['remove', 'impute', 'mean', 'median', 'null']},
        {'d': 3, 'q': 'How would you choose the right chart for your data?', 'k': ['trend', 'comparison', 'distribution', 'bar', 'line']},
        {'d': 3, 'q': 'What is A/B testing and how do you interpret the result?', 'k': ['control', 'variant', 'significance', 'hypothesis', 'sample']},
    ],
    'AI/ML Engineer': [
        {'d': 1, 'q': 'What is machine learning?', 'k': ['data', 'learn', 'pattern', 'predict', 'model']},
        {'d': 1, 'q': 'What is the difference between supervised and unsupervised learning?', 'k': ['label', 'cluster', 'classification', 'regression']},
        {'d': 2, 'q': 'What is overfitting and how can you prevent it?', 'k': ['training', 'generalize', 'regularization', 'validation', 'data']},
        {'d': 2, 'q': 'What is a confusion matrix?', 'k': ['true positive', 'false positive', 'precision', 'recall', 'classification']},
        {'d': 3, 'q': 'Explain the bias-variance tradeoff.', 'k': ['bias', 'variance', 'underfit', 'overfit', 'complexity']},
        {'d': 3, 'q': 'How does gradient descent work?', 'k': ['loss', 'gradient', 'learning rate', 'minimum', 'iterat']},
    ],
}

ROLES = list(BANK.keys())
LEVELS = ['Beginner', 'Intermediate', 'Advanced']


def generate_question(role, difficulty, asked):
    """Pick an unasked question closest to the wanted difficulty.
    MOCK: to use a real AI later, keep this signature and change the inside."""
    pool = [x for x in BANK[role] if x['q'] not in asked]
    best = min(abs(x['d'] - difficulty) for x in pool)
    chosen = random.choice([x for x in pool if abs(x['d'] - difficulty) == best])
    return {'text': chosen['q'], 'difficulty': chosen['d'], 'keywords': chosen['k']}