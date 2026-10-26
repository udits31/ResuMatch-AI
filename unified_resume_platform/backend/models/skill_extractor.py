"""NLP skill extraction via a skills taxonomy + spaCy PhraseMatcher (regex fallback)."""

import re

# Canonical skill -> list of surface forms (aliases/synonyms), grouped by category.
SKILLS_TAXONOMY = {
    "programming_languages": {
        "python": ["python"],
        "java": ["java"],
        "javascript": ["javascript", "js", "ecmascript"],
        "typescript": ["typescript", "ts"],
        "c++": ["c++", "cpp"],
        "c#": ["c#", "c sharp", "csharp"],
        "c": ["c programming", "c language"],
        "go": ["golang", "go lang"],
        "rust": ["rust"],
        "ruby": ["ruby"],
        "php": ["php"],
        "scala": ["scala"],
        "kotlin": ["kotlin"],
        "swift": ["swift"],
        "r": ["r programming", "rstats", "r language"],
        "matlab": ["matlab"],
        "sql": ["sql"],
        "bash": ["bash", "shell scripting", "shell script"],
    },
    "web_frameworks": {
        "react": ["react", "react.js", "reactjs"],
        "angular": ["angular", "angularjs"],
        "vue": ["vue", "vue.js", "vuejs"],
        "node.js": ["node.js", "nodejs", "node js"],
        "django": ["django"],
        "flask": ["flask"],
        "fastapi": ["fastapi"],
        "spring boot": ["spring boot", "spring"],
        "express": ["express", "express.js", "expressjs"],
        "next.js": ["next.js", "nextjs"],
        "html": ["html", "html5"],
        "css": ["css", "css3"],
        "sass": ["sass", "scss"],
        "tailwind": ["tailwind", "tailwind css"],
        "graphql": ["graphql"],
        "rest api": ["rest api", "restful api", "rest apis", "rest"],
        "grpc": ["grpc"],
    },
    "cloud_devops": {
        "aws": ["aws", "amazon web services"],
        "azure": ["azure", "microsoft azure"],
        "gcp": ["gcp", "google cloud", "google cloud platform"],
        "docker": ["docker", "containerization", "containers"],
        "kubernetes": ["kubernetes", "k8s"],
        "terraform": ["terraform"],
        "jenkins": ["jenkins"],
        "ci/cd": ["ci/cd", "ci cd", "continuous integration", "continuous delivery"],
        "git": ["git", "github", "gitlab", "version control"],
        "linux": ["linux", "unix"],
        "ansible": ["ansible"],
        "prometheus": ["prometheus"],
        "grafana": ["grafana"],
        "microservices": ["microservices", "microservice"],
        "serverless": ["serverless"],
    },
    "data_ml": {
        "machine learning": ["machine learning", "ml"],
        "deep learning": ["deep learning"],
        "artificial intelligence": ["artificial intelligence", "ai"],
        "natural language processing": ["natural language processing", "nlp"],
        "computer vision": ["computer vision"],
        "data analysis": ["data analysis", "data analytics"],
        "data science": ["data science"],
        "tensorflow": ["tensorflow"],
        "pytorch": ["pytorch"],
        "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
        "keras": ["keras"],
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "spark": ["spark", "apache spark", "pyspark"],
        "hadoop": ["hadoop"],
        "tableau": ["tableau"],
        "power bi": ["power bi", "powerbi"],
        "excel": ["excel", "microsoft excel"],
        "statistics": ["statistics", "statistical analysis"],
    },
    "databases": {
        "mysql": ["mysql"],
        "postgresql": ["postgresql", "postgres"],
        "mongodb": ["mongodb", "mongo"],
        "redis": ["redis"],
        "cassandra": ["cassandra"],
        "elasticsearch": ["elasticsearch"],
        "oracle": ["oracle db", "oracle database"],
        "sqlite": ["sqlite"],
        "dynamodb": ["dynamodb"],
    },
    "messaging": {
        "kafka": ["kafka", "apache kafka"],
        "rabbitmq": ["rabbitmq"],
    },
    "methodologies": {
        "agile": ["agile"],
        "scrum": ["scrum"],
        "kanban": ["kanban"],
        "devops": ["devops"],
        "tdd": ["tdd", "test driven development"],
        "project management": ["project management"],
    },
    "soft_skills": {
        "leadership": ["leadership", "team leadership"],
        "communication": ["communication"],
        "problem solving": ["problem solving", "problem-solving"],
        "teamwork": ["teamwork", "collaboration"],
        "mentoring": ["mentoring", "mentorship"],
        "stakeholder management": ["stakeholder management"],
    },
}


def _flatten_taxonomy():
    flat = {}
    for category in SKILLS_TAXONOMY.values():
        for canonical, aliases in category.items():
            flat[canonical] = aliases
    return flat


class SkillExtractor:
    def __init__(self):
        self.skills = _flatten_taxonomy()
        self._nlp = None
        self._matcher = None
        self._regex = None
        self._backend = None
        self._setup()

    def _setup(self):
        try:
            import spacy
            from spacy.matcher import PhraseMatcher
            try:
                nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "ner", "lemmatizer", "attribute_ruler"])
            except OSError:
                nlp = spacy.blank("en")  # model not downloaded; tokenizer still works
            matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
            for canonical, aliases in self.skills.items():
                matcher.add(canonical, [nlp.make_doc(alias) for alias in aliases])
            self._nlp = nlp
            self._matcher = matcher
            self._backend = "spacy"
            print("[ok] SkillExtractor using spaCy PhraseMatcher")
            return
        except Exception as e:
            print(f"[warn] spaCy unavailable for skill extraction, using regex fallback: {e}")

        self._regex = {}
        for canonical, aliases in self.skills.items():
            self._regex[canonical] = [
                re.compile(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", re.IGNORECASE)
                for alias in aliases
            ]
        self._backend = "regex"

    @property
    def backend(self):
        return self._backend

    def extract(self, text):
        if not text:
            return []

        found = set()
        if self._backend == "spacy":
            doc = self._nlp.make_doc(text)  # tokenization only -> fast
            for match_id, _start, _end in self._matcher(doc):
                found.add(self._nlp.vocab.strings[match_id])
        else:
            for canonical, patterns in self._regex.items():
                if any(p.search(text) for p in patterns):
                    found.add(canonical)

        return sorted(found)


_EXTRACTOR = None

def get_skill_extractor():
    global _EXTRACTOR
    if _EXTRACTOR is None:
        _EXTRACTOR = SkillExtractor()
    return _EXTRACTOR
