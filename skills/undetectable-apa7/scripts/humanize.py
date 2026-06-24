"""
Humanizer — Humanización de texto académico para evitar detección por IA.

Transforma texto generado por IA para que sea indistinguible de texto humano
mediante variación de longitud de oraciones, rotación de vocabulario,
inserción de hedging, y diversificación de aperturas de oraciones.

Basado en investigación académica sobre señales de detección:
- Perplexity (baja en IA → vocabulario predecible)
- Burstiness (baja en IA → longitudes de oración uniformes)
- Diversidad léxica (baja en IA → palabras repetidas)
- Densidad de hedging (baja en IA → certeza excesiva)
- Aperturas de oración (monótonas en IA → siempre sujeto primero)

Requiere solo biblioteca estándar de Python.
"""

import re
import random
import math
import string


class Humanizer:
    """
    Transforma texto para reducir detectabilidad por clasificadores de IA.

    Utiliza múltiples técnicas basadas en investigación académica sobre
    señales de detección: burstiness, perplexity, diversidad léxica,
    patrones sintácticos y adaptación al género textual.

    Uso básico:
        h = Humanizer()
        texto_humanizado = h.humanize(texto_original)
        reporte = h.check_detectability(texto_humanizado)
    """

    # =========================================================================
    # AI-TRIGGER WORDS BY ERA
    # =========================================================================
    # Palabras y frases que los detectores de IA asocian fuertemente con
    # texto generado por modelos de lenguaje. Organizadas por período en que
    # eran más comunes en los training data de los LLMs.

    # 2023 – mediados 2024: palabras sobre-representadas en GPT-3.5/GPT-4
    TRIGGER_WORDS_2023_2024 = {
        "delve": ["examine", "explore", "investigate", "study", "analyze"],
        "crucial": ["essential", "important", "key", "fundamental", "central"],
        "pivotal": ["critical", "decisive", "key", "central", "important"],
        "intricate": ["complex", "detailed", "elaborate", "sophisticated", "nuanced"],
        "tapestry": ["range", "variety", "collection", "array", "set"],
        "testament": ["evidence", "reflection", "indication", "demonstration", "proof"],
        "meticulous": ["careful", "thorough", "rigorous", "systematic", "precise"],
        "garner": ["attract", "obtain", "receive", "accumulate", "gather"],
        "vibrant": ["dynamic", "active", "lively", "robust", "flourishing"],
        "landscape": ["context", "field", "area", "domain", "environment"],
        "interplay": ["interaction", "relationship", "connection", "dynamic", "exchange"],
        "underscoring": ["emphasizing", "highlighting", "stressing", "reinforcing", "pointing to"],
        "multifaceted": ["complex", "multi-dimensional", "varied", "diverse", "many-sided"],
    }

    # mediados 2024 – mediados 2025: segunda ola de palabras señal
    TRIGGER_WORDS_2024_2025 = {
        "bolster": ["support", "strengthen", "reinforce", "buttress", "shore up"],
        "foster": ["encourage", "promote", "cultivate", "nurture", "stimulate"],
        "enhance": ["improve", "strengthen", "augment", "refine", "upgrade"],
        "showcasing": ["demonstrating", "presenting", "displaying", "featuring", "exhibiting"],
        "highlighting": ["emphasizing", "stressing", "pointing out", "drawing attention to"],
        "dynamic": ["changing", "evolving", "active", "fluid", "shifting"],
        "align with": ["correspond to", "match", "reflect", "be consistent with", "fit"],
    }

    # 2025+: palabras que saturaron los detectores más recientes
    TRIGGER_WORDS_2025 = {
        "transformative": ["far-reaching", "significant", "substantial", "profound", "far-reaching"],
        "leverage": ["use", "apply", "employ", "utilize", "harness"],
        "paradigm": ["framework", "model", "approach", "perspective", "viewpoint"],
        "actionable": ["practical", "usable", "concrete", "applicable", "implementable"],
        "synergy": ["collaboration", "cooperation", "combined effect", "partnership", "coordination"],
        "nuanced understanding": ["detailed understanding", "deeper insight", "sophisticated view"],
        "rapid evolution": ["fast change", "quick development", "swift transformation"],
        "foster innovation": ["encourage new ideas", "stimulate creativity", "drive progress"],
        "cutting-edge": ["advanced", "leading", "state-of-the-art", "modern", "innovative"],
        "game-changer": ["major change", "significant shift", "turning point", "breakthrough"],
    }

    # Frases de alta señal en cualquier época (marcadores discursivos
    # sobre-representados en IA)
    HIGH_SIGNAL_PHRASES = {
        "Furthermore,": [
            "Additionally,", "Also,", "Beyond this,", "In addition,",
            "Along these lines,",
        ],
        "Moreover,": [
            "Besides,", "Further,", "What is more,", "Additionally,",
            "In a similar vein,",
        ],
        "In addition,": [
            "Beyond this,", "Also,", "Additionally,", "Along with this,",
            "Coupled with this,",
        ],
        "Consequently,": [
            "As a result,", "Thus,", "Hence,", "Because of this,",
            "Following from this,",
        ],
        "Nevertheless,": [
            "Even so,", "Nonetheless,", "Despite this,", "Regardless,",
            "Still,",
        ],
        "In today's world": [
            "Today,", "Currently,", "In contemporary contexts,",
            "At present,", "In modern settings,",
        ],
        "In recent years": [
            "Over the past few years,", "Recently,", "In the last decade,",
            "Since the early 2000s,", "A growing body of research shows that",
        ],
        "It is important to note that": [
            "It should be noted that", "One should consider that",
            "Importantly,", "Of note,", "Worth noting is that",
        ],
    }

    # "Not only... but also" se maneja por separado con una regex específica

    # =========================================================================
    # HEDGING PHRASES
    # =========================================================================
    # Los humanos usan lenguaje mitigado (hedging). La IA tiende a afirmar
    # con certeza absoluta. Insertar hedging reduce significativamente la
    # detectabilidad.

    # Cortos (insertar antes del verbo o después de coma)
    HEDGING_SHORT = [
        "perhaps", "arguably", "often", "frequently", "relatively",
        "somewhat", "broadly", "generally", "possibly", "may", "might",
        "could",
    ]

    # Largos (insertar al inicio de oración)
    HEDGING_LONG = [
        "to some degree",
        "to some extent",
        "it could be argued that",
        "it is plausible that",
        "one might suggest that",
        "in many cases",
        "tends to",
        "in some instances",
        "to a certain extent",
        "as a general rule",
        "on the whole",
        "for the most part",
        "a growing number of",
        "in large part",
        "it seems reasonable to suggest",
        "there is evidence to suggest",
        "one could argue",
        "it may be the case that",
        "taken together",
        "in broad terms",
    ]

    # Lista completa unificada
    HEDGING_ALL = HEDGING_SHORT + HEDGING_LONG

    # =========================================================================
    # SENTENCE OPENER ALTERNATIVES
    # =========================================================================
    # La IA tiende a empezar las oraciones con el sujeto.
    # Los humanos varían las aperturas con frases introductorias.

    SENTENCE_OPENERS = [
        "Interestingly,",
        "Notably,",
        "Of particular interest,",
        "From a different perspective,",
        "An alternative view suggests that",
        "What is less understood is",
        "In practice,",
        "Historically,",
        "Across various contexts,",
        "Despite these considerations,",
        "At the same time,",
        "For instance,",
        "In contrast,",
        "By comparison,",
        "A related concern is",
        "Equally important,",
        "Another dimension of this",
        "On a related note,",
        "It is also worth noting that",
        "Particular attention should be given to",
        "Looking beyond this,",
        "A similar pattern emerges with",
        "This becomes especially relevant when",
        "One way to approach this is",
        "Rather than focusing solely on",
        "The implications of this are",
        "From yet another angle,",
        "An important corollary is",
        "A parallel line of inquiry suggests",
        "Counter to this view,",
        "Shifting focus slightly,",
        "A more detailed examination reveals",
        "Setting aside this issue for a moment,",
        "On balance,",
        "A less explored aspect is",
    ]

    # =========================================================================
    # TRANSITION ALTERNATIVES
    # =========================================================================
    # Variedad de transiciones para evitar patrones repetitivos.

    TRANSITION_ALTERNATIVES = {
        "therefore": [
            "thus", "hence", "accordingly", "consequently", "as such",
            "because of this", "for this reason", "as a result",
        ],
        "however": [
            "nevertheless", "nonetheless", "even so", "yet", "still",
            "that said", "on the other hand", "conversely",
        ],
        "for example": [
            "for instance", "as an example", "to illustrate",
            "by way of illustration", "consider the case of",
        ],
        "in conclusion": [
            "to conclude", "in closing", "ultimately", "overall",
            "taken together", "all things considered", "in summary",
        ],
        "first": [
            "to begin with", "first and foremost", "initially",
            "the first point concerns", "one important aspect",
        ],
        "finally": [
            "lastly", "ultimately", "in the final analysis",
            "as a final point", "to close",
        ],
    }

    # =========================================================================
    # PERPLEXITY MAP: High-frequency English words → sophisticated synonyms
    # =========================================================================
    # Used by inject_perplexity and break_ngram_repetition to replace
    # overly common words with less frequent alternatives, increasing
    # perplexity and reducing AI predictability.

    PERPLEXITY_MAP = {
        "big": ["substantial", "considerable", "sizeable", "ample"],
        "important": ["consequential", "noteworthy", "momentous", "salient"],
        "change": ["shift", "transformation", "modification", "reconfiguration"],
        "use": ["employ", "utilize", "leverage", "deploy"],
        "show": ["demonstrate", "illustrate", "reveal", "exhibit"],
        "make": ["produce", "generate", "constitute", "formulate"],
        "find": ["discover", "identify", "uncover", "detect"],
        "need": ["require", "necessitate", "warrant", "demand"],
        "way": ["approach", "method", "mechanism", "avenue"],
        "part": ["component", "element", "facet", "constituent"],
        "many": ["numerous", "multiple", "countless", "manifold"],
        "different": ["distinct", "divergent", "contrasting", "heterogeneous"],
        "very": ["particularly", "exceptionally", "remarkably", "profoundly"],
        "really": ["genuinely", "substantially", "decidedly", "unquestionably"],
        "good": ["sound", "robust", "compelling", "constructive"],
        "new": ["novel", "emerging", "contemporary", "unprecedented"],
        "old": ["longstanding", "entrenched", "conventional", "established"],
        "great": ["profound", "far-reaching", "substantial", "immense"],
        "hard": ["challenging", "arduous", "demanding", "formidable"],
        "help": ["facilitate", "enable", "scaffold", "assist"],
        "try": ["attempt", "endeavor", "pursue", "undertake"],
        "think": ["contend", "posit", "maintain", "assert"],
        "know": ["recognize", "acknowledge", "appreciate", "discern"],
        "look": ["examine", "scrutinize", "survey", "consider"],
        "idea": ["concept", "notion", "construct", "paradigm"],
        "study": ["investigation", "examination", "inquiry", "analysis"],
        "result": ["outcome", "finding", "product", "consequence"],
        "problem": ["challenge", "issue", "obstacle", "difficulty"],
        "thing": ["aspect", "dimension", "phenomenon", "characteristic"],
    }

    # =========================================================================
    # FUNCTION WORD VARIATIONS: Verbose prepositional phrases → concise forms
    # =========================================================================
    # Replacing verbose function-word constructs with simpler alternatives
    # reduces the predictability gap between AI and human writing.

    FUNCTION_WORD_VARIATIONS = {
        "in relation to": ["regarding", "concerning", "with respect to", "about"],
        "with regard to": ["regarding", "concerning", "about", "on the matter of"],
        "in order to": ["to", "so as to", "for the purpose of"],
        "due to the fact that": ["because", "since", "as", "given that"],
        "in the context of": ["within", "in", "amid", "as part of"],
        "on the basis of": ["based on", "from", "using", "grounded in"],
    }

    # =========================================================================
    # TOP 100+ COMMON ENGLISH WORDS (function words + high-frequency)
    # =========================================================================
    # Used for perplexity estimation: a high ratio of these words indicates
    # low-perplexity (AI-like) text.

    TOP_COMMON_WORDS = frozenset({
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her",
        "she", "or", "an", "will", "my", "one", "all", "would", "there",
        "their", "what", "so", "up", "out", "if", "about", "who", "get",
        "which", "go", "me", "when", "make", "can", "like", "time", "no",
        "just", "him", "know", "take", "people", "into", "year", "your",
        "good", "some", "could", "them", "see", "other", "than", "then",
        "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first",
        "well", "way", "even", "new", "want", "because", "any", "these",
        "give", "day", "most", "us", "every", "last", "long", "much",
        "own", "old", "right", "same", "too", "such", "here", "where",
        "down", "still", "should", "each", "may", "said", "great",
        "between", "own", "ever", "never", "under", "while", "might",
        "another", "still", "must", "often", "always", "yet", "very",
        "really", "thing", "much", "many", "need", "find", "part",
        "show", "change", "help", "hand", "high", "place", "life",
        "world", "case", "week", "company", "system", "question",
    })

    # =========================================================================
    # GENRE ADAPTATION CONFIGURATIONS
    # =========================================================================
    # Diferentes géneros textuales tienen diferentes patrones de escritura.
    # Estudio CMU 2025 (PNAS): los LLMs no adaptan la voz al género.

    GENRE_CONFIGS = {
        "academic": {
            "sentence_target_mean": 22,
            "sentence_target_std": 8,
            "hedging_intensity": 0.5,
            "max_paragraph_sentences": 6,
            "min_paragraph_sentences": 3,
            "description": "Escritura formal con estructura argumentativa clásica",
        },
        "argumentative": {
            "sentence_target_mean": 18,
            "sentence_target_std": 10,
            "hedging_intensity": 0.3,
            "max_paragraph_sentences": 8,
            "min_paragraph_sentences": 3,
            "description": "Tono persuasivo con afirmaciones más directas",
        },
        "narrative": {
            "sentence_target_mean": 14,
            "sentence_target_std": 12,
            "hedging_intensity": 0.2,
            "max_paragraph_sentences": 10,
            "min_paragraph_sentences": 2,
            "description": "Estilo descriptivo con variación rítmica",
        },
        "informative": {
            "sentence_target_mean": 20,
            "sentence_target_std": 9,
            "hedging_intensity": 0.4,
            "max_paragraph_sentences": 7,
            "min_paragraph_sentences": 2,
            "description": "Exposición clara con equilibrio entre precisión y naturalidad",
        },
    }

    # =========================================================================
    # ABBREVIATION PROTECTION
    # =========================================================================
    # Abreviaciones comunes en texto académico que no deben confundirse
    # con final de oración.

    ABBREVIATIONS = (
        r"\b(?:"
        r"Dr|Prof|Sr|Jr|St|Sra|Srta|Mr|Mrs|Ms"
        r"|vol|no|p|pp|ed|trans|rev|dept|fig|vs|etc|al"
        r"|e\.g|i\.e|viz|cf|ca|approx|est|min|max"
        r"|Inc|Ltd|Co|Corp|Univ|Assn|Dept"
        r"|Capt|Sgt|Lt|Col|Gen"
        r"|ch|sec|par|para|eq|ref|chap|app|appx"
        r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
        r")"
    )

    _ABBREV_PATTERN = re.compile(ABBREVIATIONS + r"\.(?=\s|\()", re.IGNORECASE)

    # =========================================================================
    # INIT
    # =========================================================================

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def humanize(self, text, style="academic", intensity=0.7, domain_terms=None):
        """
        Aplica el pipeline completo de humanización al texto de entrada
        en un cascade de 3 pasadas para máximo efecto anti-detección.

        Pasada 1 (intensity × 1.2, cap 0.95): transformaciones profundas
        Pasada 2 (intensity × 0.5): refuerzo de burstiness y hedging
        Pasada 3 (condicional): ajuste fino de aperturas si domain_terms
                                y score > 15

        Args:
            text: str, texto a humanizar.
            style: str, uno de "academic", "argumentative",
                   "narrative", "informative".
            intensity: float 0.0-1.0, qué tan agresivamente aplicar
                       las transformaciones (0 = nada, 1 = máximo).
            domain_terms: list of str or None, términos específicos
                          del dominio para inyección.

        Returns:
            str, texto humanizado.
        """
        if not text or not text.strip():
            return text

        def _clamp(val, lo, hi):
            return max(lo, min(hi, val))

        # =====================================================================
        # PASADA 1: Transformación profunda (intensity × 1.2, cap 0.95)
        # =====================================================================
        p1 = _clamp(intensity * 1.2, 0.0, 0.95)

        text = self.adapt_to_genre(text, style)

        if random.random() < p1 and domain_terms:
            text = self.inject_domain_vocabulary(text, domain_terms, p1)

        if random.random() < p1:
            text = self.inject_perplexity(text, p1)

        if random.random() < p1:
            text = self.vary_sentence_lengths(text)

        if random.random() < p1:
            text = self.break_ngram_repetition(text, p1)

        if random.random() < p1:
            text = self.vary_syntactic_structures(text, p1)

        if random.random() < p1:
            text = self.rotate_vocabulary(text)

        if random.random() < p1:
            text = self.vary_function_words(text, p1)

        if random.random() < p1:
            text = self.add_hedging(text, p1)

        if random.random() < p1:
            text = self.vary_sentence_openers(text)

        if random.random() < p1:
            text = self.vary_paragraph_structure(text, p1)

        if random.random() < p1:
            text = self.add_writing_quirks(text, p1)

        # =====================================================================
        # PASADA 2: Refuerzo (intensity × 0.5)
        # =====================================================================
        p2 = _clamp(intensity * 0.5, 0.0, 1.0)

        if random.random() < p2:
            text = self.vary_sentence_lengths(text)

        if random.random() < p2:
            text = self.add_hedging(text, p2)

        # =====================================================================
        # PASADA 3: Ajuste fino condicional
        # =====================================================================
        if domain_terms:
            score_info = self.check_detectability(text)
            score = score_info.get("detectability_score", 100)
            if score > 15:
                if random.random() < p1 * 0.5:
                    text = self.vary_sentence_openers(text)
                if random.random() < p1 * 0.5:
                    text = self.vary_syntactic_structures(text, p1 * 0.5)

        return text.strip()

    def analyze_text(self, text):
        """
        Análisis completo del texto para señales de detección de IA.

        Devuelve un dict con:
          - perplexity_score: proporción de palabras comunes (inverso)
          - burstiness_score: desviación estándar de longitudes de oración
          - burstiness_level: "low", "medium", "high"
          - vocabulary_diversity: type-token ratio
          - avg_sentence_length: media de palabras por oración
          - ngram_repeat_rate: tasa de repetición de 3-gramas
          - function_word_deviation: desviación de distribución esperada
          - detectability_score: 0-100 (mayor = más IA-like)
          - verdict: texto descriptivo del resultado

        Args:
            text: str, texto a analizar.

        Returns:
            dict con métricas de detectabilidad.
        """
        report = self.check_detectability(text)

        if "error" in report:
            return report

        return {
            "perplexity_score": report.get("common_word_ratio", 0),
            "burstiness_score": report.get("std_sentence_length", 0),
            "burstiness_level": report.get("burstiness", "unknown"),
            "vocabulary_diversity": report.get("vocabulary_diversity", 0),
            "avg_sentence_length": report.get("avg_sentence_length", 0),
            "ngram_repeat_rate": report.get("ngram_repeat_rate", 0),
            "function_word_deviation": report.get("function_word_deviation", 0),
            "detectability_score": report.get("detectability_score", 0),
            "verdict": report.get("verdict", "unknown"),
        }

    def check_detectability(self, text):
        """
        Analiza el texto en busca de señales de detección de IA.

        Calcula 8 métricas y las combina en un puntaje compuesto (0-100):

        | Señal | Peso máximo | Descripción |
        |-------|-------------|-------------|
        | Burstiness | 20 pts | Bajo = oraciones uniformes |
        | Palabras gatillo | 15 pts | Alta densidad = IA |
        | Diversidad vocabular | 10 pts | Baja = vocabulario repetitivo |
        | Hedging | 10 pts | Bajo = certeza excesiva |
        | Variedad aperturas | 5 pts | Baja = mismo patrón sintáctico |
        | Perplejidad | 15 pts | Alta proporción de common words = IA |
        | N-grama | 15 pts | Alta repetición de n-gramas = IA |
        | Palabras funcionales | 10 pts | Desviación en artículos/preposiciones |

        Args:
            text: str, texto a analizar.

        Returns:
            dict con todas las métricas y el veredicto.
        """
        sentences = self._split_sentences(text)
        words = text.split()
        total_words = len(words)
        total_sentences = len(sentences)

        if total_sentences == 0 or total_words == 0:
            return {
                "error": "empty text",
                "detectability_score": 0,
                "verdict": "insufficient text",
            }

        # --- Longitudes de oración ---
        sent_lengths = [len(s.split()) for s in sentences]
        avg_sent_len = sum(sent_lengths) / total_sentences
        if total_sentences > 1:
            std_sent_len = self._std_dev(sent_lengths, avg_sent_len)
        else:
            std_sent_len = 0

        # --- Palabras gatillo ---
        trigger_count = self._count_trigger_words(text)
        trigger_density = trigger_count / total_words

        # --- Diversidad vocabulario (type-token ratio) ---
        cleaned_words = [
            w.lower().strip(string.punctuation)
            for w in words
            if w.strip(string.punctuation)
        ]
        if cleaned_words:
            unique_words = len(set(cleaned_words))
            vocab_diversity = unique_words / len(cleaned_words)
        else:
            vocab_diversity = 1.0

        # --- Hedging ---
        hedging_count = self._count_hedging_occurrences(text)
        hedging_density = hedging_count / total_words if total_words > 0 else 0

        # --- Diversidad de aperturas ---
        openers_sample = min(total_sentences, 20)
        if openers_sample > 0:
            first_words = []
            for s in sentences[:openers_sample]:
                s = s.strip()
                first_word = s.split()[0] if s.split() else ""
                first_words.append(first_word)
            unique_first = len(set(first_words))
            opener_diversity = unique_first / openers_sample
        else:
            opener_diversity = 1.0

        # --- Perplejidad: proporción de TOP_COMMON_WORDS ---
        # A mayor proporción de palabras comunes → menor perplejidad → más IA-like
        common_word_count = sum(
            1 for w in cleaned_words if w in self.TOP_COMMON_WORDS
        )
        common_word_ratio = common_word_count / len(cleaned_words) if cleaned_words else 0.5

        # --- N-grama repetition rate (3-gramas) ---
        # Cuántos 3-gramas se repiten versus únicos
        ngram_size = 3
        ngram_counts = {}
        for i in range(len(cleaned_words) - ngram_size + 1):
            ngram = tuple(cleaned_words[i:i + ngram_size])
            if all(ngram):
                ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1
        total_ngrams = sum(ngram_counts.values())
        unique_ngrams = len(ngram_counts)
        if total_ngrams > 0:
            ngram_repeat_rate = 1.0 - (unique_ngrams / total_ngrams)
        else:
            ngram_repeat_rate = 0.0

        # --- Función word variance: article_ratio y prep_ratio ---
        article_pattern = re.compile(r"\b(the|a|an)\b", re.IGNORECASE)
        prep_pattern = re.compile(
            r"\b(of|in|to|for|with|on|at|by|from|as|into|through|"
            r"during|before|after|above|below|between|under)\b",
            re.IGNORECASE,
        )
        article_count = len(article_pattern.findall(text))
        prep_count = len(prep_pattern.findall(text))
        article_ratio = article_count / total_words if total_words > 0 else 0
        prep_ratio = prep_count / total_words if total_words > 0 else 0
        # Valores esperados para texto humano: ~0.06 artículos, ~0.09 preposiciones
        article_dev = abs(article_ratio - 0.06)
        prep_dev = abs(prep_ratio - 0.09)
        func_word_dev = (article_dev + prep_dev) * 2.0  # 0 = cerca de humano

        # --- Puntaje compuesto ---
        score = 0.0

        # 1. Burstiness (max 20 pts)
        if std_sent_len < 5:
            score += 20
        elif std_sent_len < 8:
            score += 12
        elif std_sent_len < 11:
            score += 6

        # 2. Densidad de palabras gatillo (max 15 pts)
        if trigger_density > 0.025:
            score += 15
        elif trigger_density > 0.012:
            score += 9
        elif trigger_density > 0.005:
            score += 3

        # 3. Diversidad vocabulario (max 10 pts)
        if vocab_diversity < 0.45:
            score += 10
        elif vocab_diversity < 0.55:
            score += 6
        elif vocab_diversity < 0.65:
            score += 3

        # 4. Densidad de hedging (max 10 pts)
        if hedging_density < 0.003:
            score += 10
        elif hedging_density < 0.008:
            score += 5
        elif hedging_density < 0.015:
            score += 2

        # 5. Diversidad de aperturas (max 5 pts)
        if opener_diversity < 0.3:
            score += 5
        elif opener_diversity < 0.5:
            score += 3

        # 6. Perplejidad: proporción de palabras comunes (max 15 pts)
        # >70% common words = baja perplejidad = IA-like
        if common_word_ratio > 0.70:
            score += 15
        elif common_word_ratio > 0.62:
            score += 9
        elif common_word_ratio > 0.55:
            score += 4

        # 7. N-grama repetition rate (max 15 pts)
        if ngram_repeat_rate > 0.20:
            score += 15
        elif ngram_repeat_rate > 0.12:
            score += 9
        elif ngram_repeat_rate > 0.06:
            score += 4

        # 8. Función word variance (max 10 pts)
        if func_word_dev > 0.10:
            score += 10
        elif func_word_dev > 0.06:
            score += 6
        elif func_word_dev > 0.03:
            score += 3

        final_score = min(int(score), 100)

        # Veredicto (umbrales más estrictos: <10 = humano)
        if final_score >= 50:
            verdict = "High detectability (AI-like)"
        elif final_score >= 25:
            verdict = "Moderate detectability"
        elif final_score >= 10:
            verdict = "Low detectability"
        else:
            verdict = "Likely human-like"

        return {
            "detectability_score": final_score,
            "avg_sentence_length": round(avg_sent_len, 1),
            "std_sentence_length": round(std_sent_len, 1),
            "burstiness": (
                "low" if std_sent_len < 6
                else "medium" if std_sent_len < 10
                else "high"
            ),
            "trigger_word_count": trigger_count,
            "trigger_word_density": round(trigger_density, 4),
            "vocabulary_diversity": round(vocab_diversity, 3),
            "hedging_count": hedging_count,
            "hedging_density": round(hedging_density, 4),
            "opener_diversity": round(opener_diversity, 3),
            "common_word_ratio": round(common_word_ratio, 3),
            "ngram_repeat_rate": round(ngram_repeat_rate, 3),
            "function_word_deviation": round(func_word_dev, 3),
            "sentence_count": total_sentences,
            "word_count": total_words,
            "verdict": verdict,
        }

    # =========================================================================
    # TRANSFORMATION METHODS
    # =========================================================================

    def inject_domain_vocabulary(self, text, domain_terms=None, intensity=0.5):
        """
        Inserta términos de dominio específico en posiciones naturales
        dentro del texto para aumentar la especificidad contextual.

        Si se proporcionan domain_terms, se inserta uno aleatorio en
        aproximadamente el 30% de las oraciones en una posición
        gramaticalmente natural (antes del verbo o después de coma).

        Args:
            text: str, texto a modificar.
            domain_terms: list of str o None, términos específicos del dominio.
            intensity: float 0.0-1.0, qué tan agresivamente insertar.

        Returns:
            str, texto con terminología de dominio insertada.
        """
        if not text or not text.strip() or not domain_terms:
            return text

        sentences = self._split_sentences(text)
        if len(sentences) < 2:
            return text

        fraction = intensity * 0.3
        num_to_modify = max(1, int(len(sentences) * fraction))
        num_to_modify = min(num_to_modify, len(sentences))
        modify_indices = set(random.sample(range(len(sentences)), num_to_modify))

        result = []
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if not sent:
                continue

            if i in modify_indices and len(sent.split()) >= 6:
                term = random.choice(domain_terms)
                # Insertar antes del verbo principal o después de la primera coma
                verb_m = re.search(
                    r"\b(is|are|was|were|has|have|had|will|would|can|could|"
                    r"shall|should|may|might|plays|shows|indicates|suggests|"
                    r"demonstrates|reveals|represents|constitutes|involves|"
                    r"reflects|provides|offers|yields)\b",
                    sent, re.IGNORECASE,
                )
                comma_m = re.search(r",\s+", sent)
                if verb_m and random.random() < 0.6:
                    pos = verb_m.start()
                    sent = sent[:pos] + term + " " + sent[pos:]
                elif comma_m:
                    pos = comma_m.end()
                    sent = sent[:pos] + term + ", " + sent[pos:]

            result.append(sent)

        return " ".join(result)

    def inject_perplexity(self, text, intensity=0.7):
        """
        Reemplaza palabras de alta frecuencia en el texto con alternativas
        menos comunes (del PERPLEXITY_MAP), aumentando la perplejidad
        general y reduciendo la predecibilidad del texto.

        Afecta aproximadamente al 35% de las oraciones, reemplazando
        palabras elegibles con ~40% de probabilidad por palabra.

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0, agresividad de las sustituciones.

        Returns:
            str, texto con mayor diversidad léxica.
        """
        if not text or not text.strip():
            return text

        sentences = self._split_sentences(text)
        if len(sentences) < 2:
            return text

        fraction = intensity * 0.35
        num_to_modify = max(1, int(len(sentences) * fraction))
        num_to_modify = min(num_to_modify, len(sentences))
        modify_indices = set(random.sample(range(len(sentences)), num_to_modify))

        result = []
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if not sent:
                continue

            if i in modify_indices:
                words = sent.split()
                new_words = []
                for w in words:
                    cleaned = w.strip(string.punctuation).lower()
                    if cleaned in self.PERPLEXITY_MAP and random.random() < 0.4:
                        replacement = random.choice(self.PERPLEXITY_MAP[cleaned])
                        # Preserve capitalization
                        if w[0].isupper():
                            replacement = replacement[0].upper() + replacement[1:]
                        new_words.append(replacement)
                    else:
                        new_words.append(w)
                sent = " ".join(new_words)

            result.append(sent)

        return " ".join(result)

    def break_ngram_repetition(self, text, intensity=0.7, window=120, n=3):
        """
        Detecta y rompe repeticiones de n-gramas (por defecto 3-gramas)
        en una ventana deslizante, reemplazando una palabra de cada
        repetición con un sinónimo de PERPLEXITY_MAP.

        El texto de IA tiende a repetir las mismas construcciones de
        3 palabras (3-gramas) con más frecuencia que el texto humano.

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0, agresividad.
            window: int, tamaño de ventana deslizante en caracteres.
            n: int, tamaño del n-grama a detectar.

        Returns:
            str, texto con repeticiones de n-gramas reducidas.
        """
        if not text or not text.strip():
            return text

        words = text.split()
        if len(words) < n * 3:
            return text

        # Construir n-gramas como tuplas de palabras (lowercase)
        ngrams_seen = {}
        modified_positions = set()

        for i in range(len(words) - n + 1):
            ngram = tuple(w.lower().strip(string.punctuation) for w in words[i:i + n])

            # Saltar si algún elemento del n-grama está vacío
            if not all(ngram):
                continue

            if ngram in ngrams_seen:
                prev_pos = ngrams_seen[ngram]
                # Solo procesar si está dentro de la ventana
                if i - prev_pos < window and random.random() < intensity:
                    # Elegir posición aleatoria dentro del n-grama para modificar
                    replace_idx = random.randint(0, n - 1)
                    word_to_replace = ngram[replace_idx]
                    if word_to_replace in self.PERPLEXITY_MAP:
                        abs_idx = i + replace_idx
                        if abs_idx not in modified_positions:
                            replacement = random.choice(
                                self.PERPLEXITY_MAP[word_to_replace]
                            )
                            # Preservar capitalización
                            if words[abs_idx][0].isupper():
                                replacement = replacement[0].upper() + replacement[1:]
                            words[abs_idx] = replacement
                            modified_positions.add(abs_idx)
            else:
                ngrams_seen[ngram] = i

        return " ".join(words)

    def vary_syntactic_structures(self, text, intensity=0.7):
        """
        Aplica una variedad de transformaciones sintácticas a las
        oraciones para evitar el patrón rígido sujeto-verbo-objeto
        típico de la IA.

        8 plantillas aplicadas a ~35% de las oraciones (excepto la primera):
          1. Adverbio frontal (Fronted adverbial)
          2. Voz pasiva (heurística simple)
          3. Inserción de aposición
          4. Frase de participio al inicio
          5. Inicio con conjunción (And/But/Yet/So)
          6. Frase preposicional frontal
          7. Estilo cleft-like
          8. Inicio con transición tradicional

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0.

        Returns:
            str, texto con estructuras sintácticas variadas.
        """
        if not text or not text.strip():
            return text

        sentences = self._split_sentences(text)
        if len(sentences) < 3:
            return text

        candidate_indices = list(range(1, len(sentences)))
        fraction = intensity * 0.35
        num_to_vary = max(1, int(len(candidate_indices) * fraction))
        num_to_vary = min(num_to_vary, len(candidate_indices))
        vary_indices = set(random.sample(candidate_indices, num_to_vary))

        # Palabras de transición para la plantilla 8
        transition_starts = [
            "Furthermore,", "Moreover,", "In addition,", "Consequently,",
            "Nevertheless,", "As a result,", "Therefore,", "Thus,",
        ]

        CONJUNCTION_STARTS = ["And", "But", "Yet", "So"]
        FRONTED_ADVERBIALS = [
            "Interestingly,", "Notably,", "Significantly,", "Crucially,",
            "Importantly,", "Strikingly,", "Surprisingly,", "Consequently,",
        ]
        FRONTED_PREPOSITIONALS = [
            "In this context,", "Within this framework,", "From this perspective,",
            "Under these conditions,", "Across these cases,", "In several instances,",
        ]

        result = [sentences[0].strip()]
        for i in range(1, len(sentences)):
            sent = sentences[i].strip()
            if not sent:
                continue

            if i in vary_indices and len(sent.split()) >= 6:
                words = sent.split()
                choice = random.random()

                # 1. Fronted adverbial
                if choice < 0.125:
                    adv = random.choice(FRONTED_ADVERBIALS)
                    sent = adv + " " + sent[0].lower() + sent[1:]

                # 2. Passive flip heuristic
                elif choice < 0.25:
                    # Buscar patrón "X verb(s) Y" → "Y is verb-ed by X"
                    passive_m = re.search(
                        r"\b(is|are|was|were|has been|have been)\s+(\w+ed)\s+",
                        sent, re.IGNORECASE,
                    )
                    if passive_m:
                        # Mantener como está — ya es pasiva
                        pass
                    else:
                        adv = random.choice(FRONTED_ADVERBIALS)
                        sent = adv + " " + sent[0].lower() + sent[1:]

                # 3. Appositive insertion
                elif choice < 0.375:
                    noun_phrase_m = re.search(
                        r"\b(an?|the|this|these|those|some|many|several)\s+"
                        r"(\w+)\s+",
                        sent, re.IGNORECASE,
                    )
                    if noun_phrase_m and random.random() < 0.5:
                        appositive = random.choice([
                            "a key factor", "an important element",
                            "a notable example", "a critical component",
                            "a significant aspect",
                        ])
                        pos = noun_phrase_m.end()
                        sent = (sent[:pos] + appositive + ", "
                                + sent[pos:])

                # 4. Participial phrase start
                elif choice < 0.5:
                    participles = [
                        "Building on this,", "Considering this,",
                        "Drawing from this,", "Examining this further,",
                        "Taking a broader view,", "Viewing this differently,",
                    ]
                    part = random.choice(participles)
                    sent = part + " " + sent[0].lower() + sent[1:]

                # 5. Conjunction start
                elif choice < 0.625:
                    conj = random.choice(CONJUNCTION_STARTS)
                    sent = conj + " " + sent[0].lower() + sent[1:]

                # 6. Fronted prepositional
                elif choice < 0.75:
                    prep = random.choice(FRONTED_PREPOSITIONALS)
                    sent = prep + " " + sent[0].lower() + sent[1:]

                # 7. Cleft-like
                elif choice < 0.875:
                    # "It is X that..." construction
                    first_noun_m = re.match(
                        r"\b(?:an?|the|this|these|those|some|many)\s+(\w+)",
                        sent, re.IGNORECASE,
                    )
                    if first_noun_m:
                        noun = first_noun_m.group(0)
                        rest = sent[first_noun_m.end():].strip()
                        sent = "It is " + noun + " that" + rest
                    else:
                        adv = random.choice(FRONTED_ADVERBIALS)
                        sent = adv + " " + sent[0].lower() + sent[1:]

                # 8. Traditional transition start
                else:
                    trans = random.choice(transition_starts)
                    sent = trans + " " + sent[0].lower() + sent[1:]

            result.append(sent)

        return " ".join(result)

    def vary_function_words(self, text, intensity=0.7):
        """
        Reemplaza frases preposicionales verbose del texto con
        alternativas más concisas usando FUNCTION_WORD_VARIATIONS.

        Además:
        - Elimina algunos artículos ("the") antes de sustantivos abstractos.
        - Convierte construcciones "there is/are" a forma directa.

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0.

        Returns:
            str, texto con palabras funcionales variadas.
        """
        if not text or not text.strip():
            return text

        result = text

        # 1. Reemplazar frases verbose del mapeo
        for phrase, alternatives in self.FUNCTION_WORD_VARIATIONS.items():
            if random.random() < intensity:
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                result = pattern.sub(lambda m: random.choice(alternatives), result)

        # 2. Eliminar "the" antes de sustantivos abstractos (~20% de ocurrencias)
        abstract_nouns = [
            "research", "literature", "evidence", "knowledge", "understanding",
            "education", "society", "nature", "history", "science", "art",
            "technology", "development", "progress", "democracy", "culture",
        ]
        for noun in abstract_nouns:
            if random.random() < intensity * 0.2:
                pattern = re.compile(
                    r"\bthe\s+(?=" + re.escape(noun) + r"\b)", re.IGNORECASE
                )
                result = pattern.sub("", result)

        # 3. Convertir "there is/are" a forma directa (~30%)
        def _replace_there(m):
            if random.random() < intensity * 0.3:
                rest = m.group(2)
                return rest[0].upper() + rest[1:] if rest else m.group(0)
            return m.group(0)

        result = re.sub(
            r"(?i)\bThere\s+(is|are)\s+(.+)",
            _replace_there,
            result,
        )

        return result

    def add_writing_quirks(self, text, intensity=0.5):
        """
        Añade "imperfecciones" naturales de la escritura humana:
        - Contracciones en ~15% de las oraciones
        - Incisos con em-dash en ~8% de las oraciones elegibles

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0.

        Returns:
            str, texto con marcas de naturalidad humana.
        """
        if not text or not text.strip():
            return text

        sentences = self._split_sentences(text)
        if len(sentences) < 3:
            return text

        contraction_map = {
            "cannot": "can't",
            "do not": "don't",
            "does not": "doesn't",
            "did not": "didn't",
            "will not": "won't",
            "would not": "wouldn't",
            "could not": "couldn't",
            "should not": "shouldn't",
            "have not": "haven't",
            "has not": "hasn't",
            "had not": "hadn't",
            "is not": "isn't",
            "are not": "aren't",
            "was not": "wasn't",
            "were not": "weren't",
            "it is": "it's",
            "that is": "that's",
            "there is": "there's",
            "there are": "there are",
            "I am": "I'm",
            "I will": "I'll",
            "I would": "I'd",
            "I have": "I've",
            "they are": "they're",
            "we are": "we're",
        }

        result = []
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            words = sent.split()

            # Contracciones en ~15% de las oraciones
            if random.random() < intensity * 0.15:
                for full, contraction in contraction_map.items():
                    pattern = re.compile(r"\b" + re.escape(full) + r"\b", re.IGNORECASE)
                    if pattern.search(sent):
                        sent = pattern.sub(contraction, sent, count=1)
                        break

            # Inciso con em-dash en ~8% de oraciones con suficiente longitud
            if (random.random() < intensity * 0.08
                    and len(words) >= 12
                    and "—" not in sent):
                # Insertar inciso después de 3-6 palabras
                insert_pos = random.randint(3, min(6, len(words) - 4))
                aside_opts = [
                    "a significant consideration",
                    "an important nuance",
                    "as it were",
                    "notably",
                    "importantly",
                    "in many respects",
                    "arguably",
                    "to some degree",
                    "in practice",
                ]
                aside = random.choice(aside_opts)
                words_list = sent.split()
                before = " ".join(words_list[:insert_pos])
                after = " ".join(words_list[insert_pos:])
                sent = before + " — " + aside + " — " + after

            result.append(sent)

        return " ".join(result)

    def vary_paragraph_structure(self, text, intensity=0.6):
        """
        Varía las aperturas de los párrafos para evitar uniformidad
        estructural. Divide el texto por doble salto de línea y
        modifica el inicio de ~40% de los párrafos usando 5 plantillas.

        Args:
            text: str, texto a modificar.
            intensity: float 0.0-1.0.

        Returns:
            str, texto con aperturas de párrafo variadas.
        """
        if not text or not text.strip():
            return text

        paragraphs = re.split(r"\n\n+", text.strip())
        if len(paragraphs) < 2:
            return text

        candidate_indices = list(range(1, len(paragraphs)))
        num_to_vary = max(1, int(len(candidate_indices) * intensity * 0.4))
        num_to_vary = min(num_to_vary, len(candidate_indices))
        vary_indices = set(random.sample(candidate_indices, num_to_vary))

        templates = [
            "Although {}, it is important to note that",
            "While {},",
            "Despite {}, a closer examination reveals that",
            "An important question that arises is whether",
            "To understand this further, consider that",
        ]

        result = []
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue

            if i in vary_indices:
                # Extraer la primera oración del párrafo
                first_sent_match = re.match(r"([^.!?]+[.!?])", para)
                if first_sent_match:
                    first_sent = first_sent_match.group(1)
                    rest = para[len(first_sent):].strip()
                    # Elegir plantilla y adaptar
                    template = random.choice(templates)
                    if "{}" in template:
                        # Templates like "Although {}, it is important..."
                        first_lower = first_sent[0].lower() + first_sent[1:]
                        if first_lower.endswith("."):
                            first_lower = first_lower[:-1]
                        new_opening = template.replace("{}", first_lower)
                        if rest:
                            para = new_opening + ". " + rest
                        else:
                            para = new_opening + "."
                    else:
                        # Standalone template (no placeholder)
                        para = template + " " + first_sent[0].lower() + first_sent[1:]

            result.append(para)

        return "\n\n".join(result)

    def vary_sentence_lengths(self, text):
        """
        Ajusta la distribución de longitudes de oración para imitar
        el patrón humano (3 pasadas).

        Los humanos mezclan naturalmente oraciones cortas (8-12 palabras),
        medias (18-25) y largas (30+). El texto de IA tiende a longitudes
        uniformes.

        Primera pasada:
        - Oraciones >28 palabras → dividir en 2-3 oraciones
        - Oraciones <8 palabras (adyacentes) → fusionar

        Segunda pasada: fusionar oraciones medias consecutivas (12-25
        palabras) que reducen la variabilidad.

        Tercera pasada: si std_dev < 8.0, forzar más variación dividiendo
        otra larga o fusionando medias.
        """
        sentences = self._split_sentences(text)
        if len(sentences) < 3:
            return text

        # --- Pasada 1: dividir largas y fusionar cortas ---
        result = []
        i = 0
        while i < len(sentences):
            sent = sentences[i].strip()
            if not sent:
                i += 1
                continue

            word_count = len(sent.split())

            # Oración larga: dividir (umbral reducido de 35 a 28)
            if word_count > 28:
                parts = self._split_long_sentence(sent)
                for p in parts:
                    p = p.strip()
                    if p:
                        result.append(p)

            # Oración corta con siguiente disponible: fusionar
            elif word_count < 8 and i + 1 < len(sentences):
                next_sent = sentences[i + 1].strip()
                if next_sent:
                    stem = sent.rstrip(".!?")
                    next_start = next_sent[0].lower() + next_sent[1:]
                    merged = stem + ", " + next_start
                    result.append(merged)
                    i += 1  # saltar la siguiente
                else:
                    result.append(sent)
            else:
                result.append(sent)

            i += 1

        # --- Pasada 2: fusionar medias consecutivas (12-25 palabras) ---
        if len(result) >= 3:
            merged_result = []
            j = 0
            while j < len(result):
                sent = result[j].strip()
                if not sent:
                    j += 1
                    continue
                wc = len(sent.split())
                # Si es media y hay siguiente también media
                if (12 <= wc <= 25 and j + 1 < len(result)
                        and 12 <= len(result[j + 1].split()) <= 25
                        and random.random() < 0.4):
                    next_sent = result[j + 1].strip()
                    stem = sent.rstrip(".!?")
                    next_start = next_sent[0].lower() + next_sent[1:]
                    merged = stem + ", " + next_start
                    merged_result.append(merged)
                    j += 1  # saltar la siguiente
                else:
                    merged_result.append(sent)
                j += 1
            result = merged_result

        # --- Pasada 3: forzar std_dev si es necesario ---
        if len(result) >= 4:
            lengths = [len(s.split()) for s in result if s.strip()]
            if lengths:
                mean_len = sum(lengths) / len(lengths)
                std_len = self._std_dev(lengths, mean_len)
                if std_len < 8.0:
                    # Encontrar la oración más larga y dividirla
                    longest_idx = max(range(len(result)), key=lambda k: len(result[k].split()) if result[k].strip() else 0)
                    longest_sent = result[longest_idx].strip()
                    if longest_sent and len(longest_sent.split()) > 20:
                        parts = self._split_long_sentence(longest_sent)
                        if len(parts) > 1:
                            result[longest_idx:longest_idx + 1] = parts

                    # Recalcular y si aún es baja, fusionar medias
                    lengths2 = [len(s.split()) for s in result if s.strip()]
                    if lengths2:
                        mean2 = sum(lengths2) / len(lengths2)
                        std2 = self._std_dev(lengths2, mean2)
                        if std2 < 8.0 and len(result) >= 3:
                            # Buscar medias consecutivas y fusionar
                            for k in range(len(result) - 1):
                                if k >= len(result) - 1:
                                    break
                                s1 = result[k].strip()
                                s2 = result[k + 1].strip()
                                if s1 and s2:
                                    w1 = len(s1.split())
                                    w2 = len(s2.split())
                                    if 10 <= w1 <= 28 and 10 <= w2 <= 28:
                                        stem = s1.rstrip(".!?")
                                        next_start = s2[0].lower() + s2[1:]
                                        result[k] = stem + ", " + next_start
                                        result.pop(k + 1)
                                        break

        return " ".join(result)

    def rotate_vocabulary(self, text):
        """
        Reemplaza palabras y frases gatillo de IA por alternativas
        más naturales.

        Procesa todas las eras de palabras gatillo + frases de alta
        señal. Usa reemplazo aleatorio para evitar patrones fijos.
        """
        result = text

        # --- Reemplazar frases de alta señal (multi-palabra) ---
        for phrase, alternatives in self.HIGH_SIGNAL_PHRASES.items():
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)

            def _make_phrase_replacer(alts):
                return lambda m: random.choice(alts)

            result = pattern.sub(
                _make_phrase_replacer(alternatives), result
            )

        # --- "Not only... but also" -> "both X and Y" ---
        result = re.sub(
            r"(?i)not only\s+(.+?)\s+but also",
            lambda m: "both {} and".format(m.group(1)),
            result,
        )

        # --- Reemplazar palabras gatillo individuales ---
        all_triggers = {}
        all_triggers.update(self.TRIGGER_WORDS_2023_2024)
        all_triggers.update(self.TRIGGER_WORDS_2024_2025)
        all_triggers.update(self.TRIGGER_WORDS_2025)

        for word, alternatives in all_triggers.items():
            if " " in word:
                # Frase multi-palabra
                pattern = re.compile(re.escape(word), re.IGNORECASE)
            else:
                # Palabra individual: búsqueda de palabra completa
                pattern = re.compile(
                    r"\b" + re.escape(word) + r"\b", re.IGNORECASE
                )

            def _make_word_replacer(alts):
                return lambda m: random.choice(alts)

            result = pattern.sub(
                _make_word_replacer(alternatives), result
            )

        return result

    def add_hedging(self, text, intensity=0.7):
        """
        Inserta frases de mitigación (hedging) para reducir la certeza
        aparente y asemejarse a la escritura humana.

        Los humanos usamos lenguaje mitigado naturalmente;
        la IA sobreafirma la certeza.

        Tres estrategias:
        1. Hedging largo al inicio de oración (~30%)
        2. Hedging corto antes del verbo (~40%)
        3. Hedging después de la primera coma (~30%)
        """
        sentences = self._split_sentences(text)
        if len(sentences) < 3:
            return text

        # Cuántas oraciones modificar basado en intensidad
        fraction = intensity * 0.3  # hasta 30% de las oraciones
        num_to_hedge = max(1, int(len(sentences) * fraction))
        num_to_hedge = min(num_to_hedge, len(sentences))
        hedge_indices = set(
            random.sample(range(len(sentences)), num_to_hedge)
        )

        result = []
        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if not sent:
                continue

            if i in hedge_indices:
                sent = self._apply_hedging_to_sentence(sent)

            result.append(sent)

        return " ".join(result)

    def vary_sentence_openers(self, text):
        """
        Diversifica las aperturas de oración para evitar patrones
        sintácticos repetitivos.

        La IA tiende a empezar todas las oraciones con el sujeto.
        Los humanos usan una variedad más amplia de frases introductorias.

        Solo se modifican ~40% de las oraciones (excluyendo la primera)
        para evitar un aspecto sobre-ingenierizado.
        """
        sentences = self._split_sentences(text)
        if len(sentences) < 3:
            return text

        # Elegir ~40% de las oraciones (excepto la primera)
        candidate_indices = list(range(1, len(sentences)))
        num_to_vary = max(1, int(len(candidate_indices) * 0.4))
        num_to_vary = min(num_to_vary, len(candidate_indices))
        vary_indices = set(
            random.sample(candidate_indices, num_to_vary)
        )

        result = [sentences[0].strip()]  # primera intacta

        for i in range(1, len(sentences)):
            sent = sentences[i].strip()
            if not sent:
                continue

            if i in vary_indices and len(sent.split()) >= 5:
                new_opener = random.choice(self.SENTENCE_OPENERS)
                sent = new_opener + " " + sent[0].lower() + sent[1:]

            result.append(sent)

        return " ".join(result)

    def adapt_to_genre(self, text, genre="academic"):
        """
        Adapta el texto a los patrones de escritura del género
        especificado.

        Basado en estudio CMU 2025 (PNAS) que demostró que los LLMs
        no adaptan la voz al género textual de forma natural.

        Args:
            text: str, texto a adaptar.
            genre: str, "academic", "argumentative", "narrative",
                   "informative".

        Returns:
            str, texto adaptado al género.
        """
        config = self.GENRE_CONFIGS.get(genre, self.GENRE_CONFIGS["academic"])

        # Ajustes específicos por género
        if genre == "narrative":
            # Más transiciones temporales
            text = self._apply_genre_transitions(text, [
                (r"\btherefore\b", "because of this"),
                (r"\bhowever\b", "still"),
            ])
        elif genre == "argumentative":
            # Más transiciones contrastivas
            text = self._apply_genre_transitions(text, [
                (r"\bfor example\b", "consider"),
            ])
        elif genre == "informative":
            # Transiciones directas, menos variación
            pass
        # "academic": mantener transiciones académicas estándar

        return text

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================

    def _split_sentences(self, text):
        """
        Divide el texto en oraciones, protegiendo abreviaciones
        comunes para evitar falsos positivos.

        Las abreviaciones como "Dr.", "et al.", "vol." no deben
        confundirse con final de oración.
        """
        if not text:
            return []

        # Proteger abreviaciones reemplazando el punto con marcador
        protected = self._ABBREV_PATTERN.sub(
            lambda m: m.group(0).replace(".", "\x00"), text
        )

        # Dividir en puntuación final + espacio
        raw = re.split(r"(?<=[.!?])\s+", protected.strip())

        # Restaurar puntos y limpiar
        sentences = [
            s.replace("\x00", ".").strip()
            for s in raw
            if s.strip()
        ]
        return sentences

    def _split_long_sentence(self, sentence):
        """
        Divide una oración larga en varias más cortas en puntos
        de quiebre lógicos.

        Orden de intentos:
        1. Punto y coma
        2. Clausula "which" / "that"
        3. Coma antes de conjunción (and, but, or)
        4. Mitad aproximada (fallback)
        """
        # Intento 1: punto y coma
        if ";" in sentence:
            parts = sentence.split(";")
            result = []
            for i, part in enumerate(parts):
                part = part.strip()
                if part:
                    if i < len(parts) - 1:
                        result.append(part[0].upper() + part[1:] + ".")
                    else:
                        result.append(part)
            if len(result) > 1:
                return result

        # Intento 2: cláusula "which"
        m = re.search(r",\s+which\s+", sentence)
        if m:
            first = sentence[: m.start()].strip() + "."
            rest = sentence[m.start() :].strip()
            second = rest[0].upper() + rest[1:]
            return [first, second]

        # Intento 3: cláusula "that"
        m = re.search(r",\s+that\s+", sentence)
        if m:
            first = sentence[: m.start()].strip() + "."
            rest = "It " + sentence[m.start() :].strip()
            return [first, rest]

        # Intento 4: coma antes de conjunción
        m = re.search(r",\s+(and|but|or|yet|so)\s+", sentence)
        if m:
            first = sentence[: m.start()].strip() + "."
            rest = sentence[m.end() :].strip()
            if rest:
                second = rest[0].upper() + rest[1:] + "."
                return [first, second]

        # Fallback: dividir aproximadamente a la mitad
        words = sentence.split()
        if len(words) >= 6:
            mid = len(words) // 2
            first = " ".join(words[:mid]) + "."
            rest = " ".join(words[mid:])
            if rest:
                rest = rest[0].upper() + rest[1:]
            return [first, rest]

        # Si no se puede dividir, devolver la original
        return [sentence]

    def _apply_hedging_to_sentence(self, sentence):
        """
        Aplica una estrategia de hedging a una oración individual.

        Elige aleatoriamente entre:
        - Estrategia A (30%): hedging largo al inicio
        - Estrategia B (40%): hedging corto antes del verbo
        - Estrategia C (30%): hedging después de la primera coma
        """
        words = sentence.split()
        if len(words) < 5:
            return sentence

        choice = random.random()

        # --- Estrategia A: Hedging largo al inicio ---
        if choice < 0.3:
            hedge = random.choice(self.HEDGING_LONG)
            # Capitalizar hedge y ajustar la oración
            hedge_capped = hedge[0].upper() + hedge[1:]
            if hedge_capped.endswith(","):
                return hedge_capped + " " + sentence[0].lower() + sentence[1:]
            else:
                return hedge_capped + ", " + sentence[0].lower() + sentence[1:]

        # --- Estrategia B: Hedging corto antes del verbo ---
        elif choice < 0.7:
            hedge = random.choice(self.HEDGING_SHORT)
            return self._insert_before_verb(sentence, hedge)

        # --- Estrategia C: Después de la primera coma ---
        else:
            comma_m = re.search(r",\s+", sentence)
            if comma_m:
                hedge = random.choice(self.HEDGING_SHORT)
                pos = comma_m.end()
                return sentence[:pos] + hedge + " " + sentence[pos:]
            else:
                # Sin coma: insertar antes del verbo
                hedge = random.choice(self.HEDGING_SHORT)
                return self._insert_before_verb(sentence, hedge)

    def _insert_before_verb(self, sentence, hedge):
        """
        Inserta una palabra/mitigador antes del verbo principal.

        Busca el primer verbo conjugado o auxiliar y lo antecede.
        """
        verb_patterns = [
            r"\b(is|are|was|were)\b",
            r"\b(has|have|had)\b",
            r"\b(does|do|did)\b",
            r"\b(will|would|can|could|should|may|might)\b",
            r"\b(plays|plays|shows|indicates|suggests)\b",
            r"\b(demonstrates|reveals|represents|constitutes)\b",
            r"\b(comprises|includes|involves|reflects)\b",
        ]

        for pattern in verb_patterns:
            m = re.search(pattern, sentence, re.IGNORECASE)
            if m:
                pos = m.start()
                return sentence[:pos] + hedge + " " + sentence[pos:]

        # Fallback: posición aleatoria temprana (después de 2-4 palabras)
        words = sentence.split()
        if len(words) >= 5:
            insert_at = random.randint(2, min(4, len(words) - 1))
            return (
                " ".join(words[:insert_at])
                + ", "
                + hedge
                + ", "
                + " ".join(words[insert_at:])
            )

        return sentence

    def _count_trigger_words(self, text):
        """
        Cuenta ocurrencias de todas las palabras/frases gatillo
        en el texto.

        Incluye las tres eras + frases de alta señal.
        """
        count = 0
        text_lower = text.lower()

        all_triggers = {}
        all_triggers.update(self.TRIGGER_WORDS_2023_2024)
        all_triggers.update(self.TRIGGER_WORDS_2024_2025)
        all_triggers.update(self.TRIGGER_WORDS_2025)

        for word in all_triggers:
            if " " in word:
                count += len(re.findall(re.escape(word), text_lower))
            else:
                count += len(
                    re.findall(r"\b" + re.escape(word) + r"\b", text_lower)
                )

        for phrase in self.HIGH_SIGNAL_PHRASES:
            count += len(re.findall(re.escape(phrase), text_lower))

        return count

    def _count_hedging_occurrences(self, text):
        """
        Cuenta ocurrencias de frases de hedging en el texto.
        """
        count = 0
        text_lower = text.lower()
        for phrase in self.HEDGING_ALL:
            if " " in phrase:
                pattern = re.escape(phrase)
            else:
                pattern = r"\b" + re.escape(phrase) + r"\b"
            count += len(re.findall(pattern, text_lower))
        return count

    def _apply_genre_transitions(self, text, replacements):
        """
        Aplica reemplazos de transiciones específicos del género.

        Args:
            text: str, texto a modificar.
            replacements: list of (pattern, replacement) tuples.

        Returns:
            str, texto con reemplazos aplicados.
        """
        result = text
        for pattern, replacement in replacements:
            result = re.sub(
                pattern,
                replacement,
                result,
                count=random.randint(1, 3),
                flags=re.IGNORECASE,
            )
        return result

    # =========================================================================
    # STATIC HELPERS
    # =========================================================================

    @staticmethod
    def _std_dev(values, mean):
        """Calcula la desviación estándar de una lista de valores."""
        if len(values) < 2:
            return 0
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
