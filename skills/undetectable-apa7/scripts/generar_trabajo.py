#!/usr/bin/env python3
"""
Generador de trabajos académicos en formato APA 7ª edición
con humanización anti-detección para IA.

Wraps APA7Doc (skill apa7-docx) + Humanizer (skill undetectable-apa7)
para producir documentos .docx académicamente correctos e indetectables
por clasificadores de IA.

Uso típico (vía el agente IA que carga este skill):

    from generar_trabajo import DocumentSpec, Section, Source, generate_document

    spec = DocumentSpec(
        title="Impacto de la Inteligencia Artificial en la Educación Superior",
        authors="Carlos Mendoza",
        affiliation="Universidad de Costa Rica",
        course="Investigación Educativa",
        instructor="Dr. Roberto Jiménez",
        date="2026",
        abstract="Este estudio analiza...",
        keywords=["inteligencia artificial", "educación superior"],
        sections=[
            Section(title="Introducción", level=1, content="..."),
            Section(title="Antecedentes", level=2, content="..."),
        ],
        sources=[
            Source(authors="García, J.", year="2020", title="...",
                   source_type="journal", journal="Revista de Educación",
                   volume="15", pages="123-145", doi="10.1234/abc"),
        ],
    )
    ruta, reporte = generate_document(spec)
"""

import sys
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

# Añadir scripts/ actual al path para importar humanize
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# Añadir apa7-docx scripts al path
_APA7_PATH = os.path.expanduser("~/.agents/skills/apa7-docx/scripts")
if _APA7_PATH not in sys.path:
    sys.path.insert(0, _APA7_PATH)

try:
    from apa7 import APA7Doc
except ImportError:
    raise ImportError(
        "No se pudo importar APA7Doc. "
        "Verifique que el skill apa7-docx esté instalado en:\n"
        f"  {_APA7_PATH}\n"
        "Ejecute: pip install python-docx (si no está instalado)"
    )

from humanize import Humanizer

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Ruta de salida según AGENTS.md: Documentos/ para .docx
OUTPUT_DIR = os.path.expanduser(
    "~/OneDrive/Documentos/Archivos OpenCode/Documentos"
)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Section:
    """
    Una sección del documento académico.

    Attributes:
        title: Título de la sección.
        level: Nivel APA 7 (1-5). 1 = centrado negrita,
               2 = izquierda negrita, etc.
        content: Texto de la sección (será humanizado automáticamente).
        references: Lista de referencias citadas en esta sección
                    (formato APA 7 en string).
    """
    title: str = ""
    level: int = 2
    content: str = ""
    references: List[str] = field(default_factory=list)


@dataclass
class Source:
    """
    Una fuente académica para incluir en la página de Referencias.

    Attributes:
        authors: Autores en formato APA ("Apellido, I., & Apellido, I.").
        year: Año de publicación.
        title: Título del trabajo.
        source_type: "journal", "book", "website", "chapter".
        journal: Nombre de la revista (para source_type="journal").
        volume: Volumen de la revista.
        issue: Número de la revista (opcional).
        pages: Páginas ("123-145").
        publisher: Editorial (para book/chapter).
        edition: Edición (para libro, opcional).
        editors: Editores (para capítulo).
        book_title: Título del libro (para capítulo).
        doi: DOI (opcional).
        url: URL (para website).
        site_name: Nombre del sitio web.
        date_accessed: Fecha de acceso al sitio web.
    """
    authors: str = ""
    year: str = ""
    title: str = ""
    source_type: str = "website"
    journal: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    publisher: str = ""
    edition: str = ""
    editors: str = ""
    book_title: str = ""
    doi: str = ""
    url: str = ""
    site_name: str = ""
    date_accessed: str = ""


@dataclass
class DocumentSpec:
    """
    Especificación completa de un documento a generar.

    Attributes:
        title: Título del trabajo (portada).
        authors: Autor(es) para la portada.
        affiliation: Afiliación institucional.
        course: Curso (opcional, portada student paper).
        instructor: Instructor (opcional, portada student paper).
        date: Fecha de entrega (opcional).
        abstract: Texto del resumen (será humanizado).
        keywords: Palabras clave (3-5 recomendadas).
        sections: Lista de secciones del documento.
        sources: Lista de fuentes para Referencias.
        style: Género textual ("academic", "argumentative",
               "narrative", "informative").
        intensity: Intensidad de humanización (0.0-1.0).
        include_toc: Incluir tabla de contenidos.
    """
    title: str = ""
    authors: str = ""
    affiliation: str = ""
    course: str = ""
    instructor: str = ""
    date: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    sections: List[Section] = field(default_factory=list)
    sources: List[Source] = field(default_factory=list)
    style: str = "academic"
    intensity: float = 0.7
    include_toc: bool = True


# ---------------------------------------------------------------------------
# Helper: agregar una referencia formateada al documento
# ---------------------------------------------------------------------------


def _add_source_reference(doc: APA7Doc, source: Source) -> None:
    """
    Agrega una referencia formateada en APA 7 al documento,
    usando el método apropiado según el tipo de fuente.

    Args:
        doc: Instancia de APA7Doc.
        source: Datos de la fuente.
    """
    if source.source_type == "journal":
        doc.add_journal_reference(
            source.authors,
            source.year,
            source.title,
            source.journal,
            source.volume,
            source.pages,
            doi=source.doi or None,
            issue=source.issue or None,
        )
    elif source.source_type == "book":
        doc.add_book_reference(
            source.authors,
            source.year,
            source.title,
            source.publisher,
            edition=source.edition or None,
            doi=source.doi or None,
        )
    elif source.source_type == "chapter":
        doc.add_chapter_reference(
            source.authors,
            source.year,
            source.title,
            source.editors,
            source.book_title,
            source.pages,
            source.publisher,
            doi=source.doi or None,
        )
    elif source.source_type == "website":
        doc.add_website_reference(
            source.authors,
            source.year,
            source.title,
            source.site_name,
            source.url,
            date_accessed=source.date_accessed or None,
        )
    else:
        # Fallback: referencia genérica
        ref = f"{source.authors} ({source.year}). {source.title}."
        if source.url:
            ref += f" {source.url}"
        doc.add_reference(ref)


# ---------------------------------------------------------------------------
# Main document generation
# ---------------------------------------------------------------------------


def generate_document(
    spec: DocumentSpec, output_filename: Optional[str] = None
) -> tuple:
    """
    Genera un documento .docx completo en formato APA 7ª edición
    con contenido humanizado para evitar detección por IA.

    Domain terms are automatically extracted from the title and keywords
    and passed to the humanizer for improved context-aware humanization.

    El flujo es:
    1. Extraer términos de dominio del título y palabras clave
    2. Humanizar el resumen (con intensidad reducida)
    3. Construir portada, tabla de contenidos y resumen
    4. Para cada sección: agregar título, humanizar contenido, añadir párrafos
    5. Agregar página de referencias
    6. Ejecutar análisis de detectabilidad sobre el texto completo
    7. Guardar el .docx en la carpeta de salida estándar

    Args:
        spec: DocumentSpec con todos los datos del documento.
        output_filename: Nombre del archivo de salida (opcional;
                         por defecto se deriva del título).

    Returns:
        Tuple de (ruta_al_archivo, reporte_de_detectabilidad).
    """
    humanizer = Humanizer()

    # Extract domain terms from title and keywords
    domain_terms = []
    if spec.title:
        domain_terms.extend(spec.title.split())
    if spec.keywords:
        domain_terms.extend(spec.keywords)
    domain_terms = list(set(domain_terms))[:10]  # dedup, max 10

    # --- Humanizar resumen (menos intensidad: los resúmenes son directos) ---
    abstract_text = None
    if spec.abstract:
        abstract_text = humanizer.humanize(
            spec.abstract,
            style=spec.style,
            intensity=spec.intensity * 0.4,
            domain_terms=domain_terms,
        )

    # --- Construir documento ---
    doc = APA7Doc()

    # Portada
    doc.add_title_page(
        spec.title,
        spec.authors,
        spec.affiliation,
        course=spec.course or None,
        instructor=spec.instructor or None,
        date=spec.date or None,
    )

    # Tabla de contenidos
    if spec.include_toc:
        doc.add_toc_page()

    # Resumen
    if abstract_text:
        doc.add_abstract(abstract_text, spec.keywords or None)

    # --- Secciones ---
    humanized_paragraphs = []

    # Mapeo de nivel de título a método APA7Doc
    _HEADING_METHODS = {
        1: doc.add_heading_level1,
        2: doc.add_heading_level2,
        3: doc.add_heading_level3,
        4: doc.add_heading_level4,
        5: doc.add_heading_level5,
    }

    for section in spec.sections:
        if not section.title:
            continue

        # Agregar título según nivel
        method = _HEADING_METHODS.get(section.level, doc.add_heading_level2)
        method(section.title)

        if not section.content:
            continue

        # Humanizar contenido de la sección
        humanized = humanizer.humanize(
            section.content,
            style=spec.style,
            intensity=spec.intensity,
            domain_terms=domain_terms,
        )

        # Dividir en párrafos (separados por doble salto de línea)
        paragraphs = re.split(r"\n\s*\n", humanized)
        for para in paragraphs:
            para = para.strip()
            if para:
                doc.add_paragraph(para)
                humanized_paragraphs.append(para)

    # --- Referencias ---
    if spec.sources:
        doc.add_heading_level1("Referencias")
        for source in spec.sources:
            _add_source_reference(doc, source)
    else:
        # También recolectar referencias desde las secciones
        all_refs = []
        for section in spec.sections:
            all_refs.extend(section.references)
        if all_refs:
            doc.add_heading_level1("Referencias")
            # Deducir y ordenar
            unique_refs = list(dict.fromkeys(all_refs))
            unique_refs.sort()
            doc.add_references_section(unique_refs)

    # --- Análisis de detectabilidad ---
    full_text = " ".join(humanized_paragraphs) if humanized_paragraphs else (abstract_text or "")
    if full_text:
        detect_report = humanizer.check_detectability(full_text)
    else:
        detect_report = {"error": "no content", "detectability_score": 0}

    # --- Guardar ---
    if not output_filename:
        safe_title = re.sub(r"[^\w\s-]", "", spec.title.lower())
        safe_title = re.sub(r"[-\s]+", "_", safe_title).strip("_")[:50]
        output_filename = f"{safe_title}.docx"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    doc.save(output_path)

    return output_path, detect_report


def generate_and_print_report(
    spec: DocumentSpec, output_filename: Optional[str] = None
) -> tuple:
    """
    Genera un documento e imprime un reporte formateado en consola.

    Args:
        spec: DocumentSpec con todos los datos.
        output_filename: Nombre del archivo (opcional).

    Returns:
        Tuple de (ruta_al_archivo, reporte_de_detectabilidad).
    """
    output_path, detect_report = generate_document(spec, output_filename)

    print("=" * 60)
    print("   DOCUMENTO GENERADO")
    print("=" * 60)
    print(f"  Ruta: {output_path}")
    print()
    print("  Reporte de detectabilidad:")
    print("-" * 40)
    for key, value in detect_report.items():
        if isinstance(value, float):
            print(f"    {key}: {value:.4f}")
        else:
            print(f"    {key}: {value}")
    print("-" * 40)

    score = detect_report.get("detectability_score", 0)
    if score >= 60:
        print("  ⚠️  ALERTA: Puntuación de detectabilidad alta.")
        print("     Considere aumentar spec.intensity (ej. 0.9)")
        print("     o revisar el contenido manualmente.")
    elif score >= 35:
        print("  📊  Moderado. Podría mejorarse con más humanización.")
        print("     Pruebe intensity=0.85 o estilo 'informative'.")
    else:
        print("  ✅  Baja detectabilidad. El texto parece humano.")
    print("=" * 60)

    return output_path, detect_report


# ---------------------------------------------------------------------------
# CLI (uso directo para pruebas)
# ---------------------------------------------------------------------------


def main():
    """
    Punto de entrada para pruebas directas desde línea de comandos.

    Uso:
        python generar_trabajo.py

    Genera un documento de ejemplo con contenido humanizado.
    """
    spec = DocumentSpec(
        title="Ejemplo de Documento Académico Humanizado",
        authors="María López",
        affiliation="Universidad de Costa Rica",
        course="Metodología de la Investigación",
        instructor="Dr. Roberto Jiménez",
        date="2026",
        abstract=(
            "Este estudio analiza el impacto de las herramientas de "
            "inteligencia artificial en la educación superior. Se examinan "
            "los cambios en las metodologías de enseñanza y los desafíos "
            "éticos que surgen de su implementación. Los resultados sugieren "
            "que la integración de estas tecnologías ofrece oportunidades "
            "significativas para mejorar la experiencia educativa."
        ),
        keywords=["inteligencia artificial", "educación superior",
                  "metodologías de enseñanza"],
        sections=[
            Section(
                title="Introducción",
                level=1,
                content=(
                    "La inteligencia artificial ha transformado diversos "
                    "aspectos de la sociedad contemporánea, y el ámbito "
                    "educativo no es una excepción. En los últimos años, "
                    "numerosas instituciones han comenzado a implementar "
                    "herramientas basadas en IA para mejorar sus procesos "
                    "de enseñanza y aprendizaje. Este fenómeno ha generado "
                    "un debate sustancial sobre las implicaciones pedagógicas "
                    "y éticas de dicha integración."
                ),
            ),
            Section(
                title="Antecedentes",
                level=2,
                content=(
                    "Diversos estudios han examinado la relación entre "
                    "tecnología y educación. Según García (2020), la adopción "
                    "de herramientas digitales en el aula ha aumentado "
                    "considerablemente en la última década. Por otra parte, "
                    "Martínez (2021) señala que los estudiantes muestran "
                    "una mayor disposición hacia metodologías que incorporan "
                    "elementos tecnológicos."
                ),
                references=[
                    "García, J. (2020). Tecnología educativa: Un análisis "
                    "contemporáneo. Revista de Educación, 15(2), 123-145.",
                    "Martínez, L. (2021). Aprendizaje digital en el siglo "
                    "XXI. Editorial Universitaria.",
                ],
            ),
        ],
        style="academic",
        intensity=0.7,
    )

    ruta, reporte = generate_and_print_report(spec)
    print(f"\nArchivo guardado en: {ruta}")
    print(f"Puntaje de detectabilidad: {reporte.get('detectability_score', 'N/A')}")


if __name__ == "__main__":
    main()
