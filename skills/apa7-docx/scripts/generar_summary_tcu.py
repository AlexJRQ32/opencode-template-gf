import sys
sys.path.insert(0, r"{{USER_DIR}}\.agents\skills\apa7-docx\scripts")
from apa7 import APA7Doc
from datetime import date

doc = APA7Doc()

# --- Portada ---
doc.add_title_page(
    title="Summary TCU CECI Micitt",
    authors="Programa de Trabajo Comunal Universitario",
    affiliation="Centro de Estudios en Ciencia, Ingeniería y Tecnología (CECI) – MICITT",
    course="TCU – Capacitación en Alfabetización Digital, Programación y Ciberseguridad",
    instructor="Coordinación CESI",
    date=date.today().strftime("%d de %B de %Y")
)

# --- Índice ---
doc.add_toc_page()

# --- Resumen ---
doc.add_abstract(
    "El presente documento constituye un resumen integral del programa de Trabajo Comunal Universitario "
    "(TCU) del CECI MICITT, orientado a la capacitación en alfabetización digital, programación web y "
    "ciberseguridad. Se describen el perfil y requisitos de los instructores, las modalidades y horarios "
    "de los cursos, el proceso de formalización documental, la oferta académica disponible, los canales "
    "de comunicación operativa y el procedimiento de evaluación y cierre. El programa busca profesionales "
    "con conocimientos técnicos sólidos y habilidades pedagógicas para facilitar cursos de 40 horas en "
    "modalidad virtual o presencial, adaptándose a las necesidades de comunidades vulnerables y diversos "
    "perfiles de estudiantes.",
    keywords=["TCU", "CECI", "MICITT", "alfabetización digital", "programación", "ciberseguridad", "instructores"]
)

# ============================================================
# SECCIÓN 1: PERFIL Y REQUISITOS DE INSTRUCTORES
# ============================================================
doc.add_heading_level1("Perfil y Requisitos de Instructores")

doc.add_heading_level2("Perfil del Instructor")
doc.add_paragraph(
    "El programa busca profesionales avanzados con conocimientos técnicos sólidos en su área de especialidad, "
    "combinados con habilidades comunicativas y pedagógicas para enseñar y conectar con diversos grupos "
    "de estudiantes. Se requiere que los instructores manejen buena dicción y empatía para explicar "
    "conceptos a estudiantes con diferentes niveles de conocimiento técnico."
)
doc.add_paragraph(
    "La capacidad de mantener la atención y motivar a grupos diversos es clave para el éxito del curso. "
    "Se enfatiza el uso de lenguaje sencillo y ejemplos prácticos para facilitar el aprendizaje "
    "significativo. Los instructores no son profesores formales, sino facilitadores que imparten cursos "
    "básicos o introductorios, pudiendo asignar tareas y atender consultas dentro del curso."
)

doc.add_heading_level2("Rol del Instructor y Modalidades de Enseñanza")
doc.add_paragraph(
    "Las clases pueden ser virtuales sincrónicas o presenciales, según la naturaleza del curso y la "
    "disponibilidad. La presencialidad es obligatoria en cursos como alfabetización digital para "
    "principiantes absolutos, ya que esta modalidad facilita la conexión con comunidades vulnerables "
    "y mejora la accesibilidad al programa."
)

doc.add_heading_level2("Sesión de Inducción y Evaluación")
doc.add_paragraph(
    "Se programa una sesión individual donde el candidato presenta una clase corta de aproximadamente "
    "10 minutos para evaluar habilidades técnicas y pedagógicas. Esta sesión es virtual, amigable y "
    "busca proporcionar retroalimentación para continuar con el proceso de formalización. La sesión "
    "tiene una duración de 40 a 45 minutos y se agenda según la disponibilidad indicada por el candidato."
)

# ============================================================
# SECCIÓN 2: MODALIDADES Y HORARIOS DE LOS CURSOS
# ============================================================
doc.add_heading_level1("Modalidades y Horarios de los Cursos")

doc.add_heading_level2("Estructura de Horas")
doc.add_paragraph(
    "Los cursos se organizan en grupos de 40 horas cada uno. Los instructores imparten tres cursos "
    "de 40 horas, sumando 120 horas de docencia presencial o virtual. Las restantes 30 horas se "
    "validan por seguimiento, preparación de materiales y atención a estudiantes, completando así "
    "las 150 horas requeridas por el TCU."
)

doc.add_heading_level2("Distribución Semanal")
doc.add_paragraph(
    "Entre semana, las clases se imparten en dos sesiones de dos horas, totalizando cuatro horas "
    "por semana durante diez semanas. Los fines de semana se ofrecen sesiones intensivas de cuatro "
    "horas en una sola jornada, para completar el curso en el mismo periodo. Se promueve que los "
    "horarios sean estables para respetar a los estudiantes y evitar cancelaciones o cambios."
)

doc.add_heading_level2("Flexibilidad Horaria")
doc.add_paragraph(
    "Se coordinan horarios según la disponibilidad del instructor y la comunidad, pudiendo ser en "
    "la mañana, tarde o fines de semana. Se busca que los CESIs asignados se adapten al horario "
    "del instructor y a las necesidades de la comunidad para facilitar la asistencia. Los cambios "
    "de horario deben gestionarse antes del inicio del curso para evitar inconvenientes."
)

doc.add_heading_level2("Plataformas y Materiales")
doc.add_paragraph(
    "Las clases virtuales utilizan plataformas gratuitas como Google Meet. La comunicación de la "
    "lista de participantes se realiza vía WhatsApp para soporte logístico. Algunos cursos cuentan "
    "con manuales o materiales ya desarrollados; otros requieren que el instructor prepare el "
    "programa y los recursos didácticos. Se prohíbe la distribución no autorizada de materiales "
    "para proteger los derechos de propiedad intelectual."
)

# ============================================================
# SECCIÓN 3: PROCESO DE FORMALIZACIÓN
# ============================================================
doc.add_heading_level1("Proceso de Formalización y Documentación")

doc.add_heading_level2("Documentos Requeridos")
doc.add_paragraph(
    "Se debe completar un proceso con recursos humanos que incluye el envío de cinco documentos "
    "en un solo envío para evitar devoluciones o retrasos:"
)
doc.add_paragraph(
    "1. Carta membretada de la universidad, firmada por una autoridad con cargo claro, que incluya "
    "nombre, número de cédula y carrera del solicitante. "
    "2. Copia de la cédula de identidad. "
    "3. Póliza estudiantil, que puede ser cubierta por la universidad o adquirida por el estudiante "
    "por un periodo usual de un año. "
    "4. Compromiso de confidencialidad, documento legal que debe firmarse de puño y letra o digitalmente. "
    "5. Carta de solicitud al departamento de alfabetización digital, indicando claramente que no "
    "habrá retribución económica durante la pasantía."
)

doc.add_heading_level2("Registro y Aval")
doc.add_paragraph(
    "Recursos humanos emite un oficio de aval con fecha de inicio y fin que valida formalmente el "
    "TCU. Una vez avalado, el instructor se registra como usuario en la plataforma CESI para la "
    "emisión de certificados. El CESI se encarga de matricular a los participantes y gestionar la "
    "logística del curso; los instructores solo se encargan de impartir las clases y evaluar a los "
    "estudiantes."
)

doc.add_heading_level2("Importancia del Cumplimiento")
doc.add_paragraph(
    "Se enfatiza seguir el proceso formal correctamente a la primera para evitar devoluciones y "
    "retrasos en la formalización. Se realiza una sesión de inducción para explicar claramente "
    "los pasos y evitar errores comunes en el papeleo."
)

# ============================================================
# SECCIÓN 4: OFERTA Y DIVERSIDAD DE CURSOS
# ============================================================
doc.add_heading_level1("Oferta y Diversidad de Cursos")

doc.add_heading_level2("Alfabetización Digital")
doc.add_paragraph(
    "Existe una demanda alta en cursos de alfabetización digital, los cuales requieren presencialidad "
    "obligatoria. Estos cursos enseñan desde cero a personas sin experiencia, facilitando la conexión "
    "con comunidades vulnerables y mejorando la accesibilidad. Se busca cubrir zonas con mayor "
    "necesidad y escasa alfabetización digital."
)

doc.add_heading_level2("Programación Web")
doc.add_paragraph(
    "Se pueden impartir cursos básicos de HTML, CSS y JavaScript, confirmados como viables para el "
    "programa. Estos cursos proporcionan a los estudiantes las bases fundamentales para el desarrollo "
    "web, con materiales protegidos y enfoque práctico."
)

doc.add_heading_level2("Ciberseguridad")
doc.add_paragraph(
    "Para ciberseguridad, existen cursos certificados por Cisco y también cursos diseñados internamente "
    "de 40 horas. Nuevos cursos pueden incorporarse tras evaluación y certificación, permitiendo la "
    "innovación constante en la oferta académica."
)

doc.add_heading_level2("Convenios con Plataformas")
doc.add_paragraph(
    "El programa dispone de acceso a plataformas como Oracle y Cisco para cursos técnicos avanzados. "
    "Los instructores interesados pueden solicitar acceso para impartir cursos en esas modalidades, "
    "lo que amplía la oferta y mejora la calidad técnica de la capacitación."
)

doc.add_heading_level2("Propiedad Intelectual")
doc.add_paragraph(
    "Los manuales y materiales son para uso exclusivo de instructores y no deben compartirse con "
    "estudiantes. Se controla que los cursos no infrinjan derechos de propiedad intelectual de "
    "terceros, buscando evitar problemas legales y proteger la integridad del programa."
)

# ============================================================
# SECCIÓN 5: COMUNICACIÓN Y COORDINACIÓN OPERATIVA
# ============================================================
doc.add_heading_level1("Comunicación y Coordinación Operativa")

doc.add_heading_level2("Canales de Comunicación")
doc.add_paragraph(
    "Los interesados deben enviar un correo electrónico a CESI@MICIT con el asunto "
    "\"Programación sesión dos\" seguido de su nombre completo. Este correo debe incluir la "
    "disponibilidad horaria y los temas de cursos que pueden impartir. La correcta redacción "
    "del asunto evita devoluciones y asegura la asignación rápida a los analistas."
)

doc.add_heading_level2("Proceso de Inscripción")
doc.add_paragraph(
    "No existe una fecha límite estricta para enviar el correo de interés tras la inducción. "
    "Se puede iniciar el proceso en meses posteriores, pero se recomienda hacerlo antes de "
    "octubre para iniciar el mismo año. Se realiza una última inducción en octubre para el "
    "reclutamiento del siguiente ciclo."
)

doc.add_heading_level2("Coordinación con CESIs")
doc.add_paragraph(
    "Se busca que los cursos se impartan en diferentes CESIs para facilitar la cobertura regional. "
    "La comunicación vía WhatsApp entre instructor, administrador y gestor del CESI es clave para "
    "el soporte logístico continuo. Se evita cambiar horarios una vez iniciado el curso para "
    "respetar a los estudiantes matriculados."
)

# ============================================================
# SECCIÓN 6: EVALUACIÓN Y CIERRE
# ============================================================
doc.add_heading_level1("Evaluación y Cierre")

doc.add_heading_level2("Evaluación de Estudiantes")
doc.add_paragraph(
    "Al finalizar el curso, el instructor debe entregar las notas y los materiales utilizados "
    "para revisión y cierre administrativo. Se firma la bitácora y la carta de cierre para "
    "documentar la finalización del proceso."
)

doc.add_heading_level2("Certificación")
doc.add_paragraph(
    "El encargado del CESI valida el cierre y procede con la certificación de los participantes. "
    "Se realiza una sesión individual para la presentación de resultados y retroalimentación, "
    "asegurando que el proceso cumpla con los estándares del programa."
)

doc.add_heading_level2("Cierre Administrativo")
doc.add_paragraph(
    "La entrega oportuna de notas y la firma de la documentación de cierre son requisitos "
    "indispensables para la validación final del TCU. El cumplimiento correcto de cada paso "
    "garantiza la certificación exitosa de los estudiantes y la formalización del trabajo "
    "realizado por el instructor."
)

# ============================================================
# SECCIÓN 7: ACCIONES REQUERIDAS
# ============================================================
doc.add_heading_level1("Acciones Requeridas")

doc.add_heading_level2("Para Estudiantes Participantes")
doc.add_paragraph(
    "1. Enviar un correo con asunto \"Programación sesión dos\" a CESI@MICIT, incluyendo nombre "
    "completo, conocimientos técnicos, posibles cursos a impartir y horario disponible para agendar "
    "la sesión individual. "
    "2. Preparar y asistir a la segunda sesión para presentar una clase corta de aproximadamente "
    "10 minutos para evaluación de competencias técnicas y pedagógicas. "
    "3. Reunir y enviar los cinco documentos necesarios para la formalización del TCU en un solo "
    "envío para evitar devoluciones o retrasos. "
    "4. Informar claramente la disponibilidad horaria para la impartición de cursos. "
    "5. En caso de requerir un curso nuevo no listado, enviar propuesta detallada para evaluación "
    "y posible certificación."
)

doc.add_heading_level2("Para Recursos Humanos y Organización Interna")
doc.add_paragraph(
    "Coordinar con el departamento de recursos humanos el trámite de aval del TCU tras el envío "
    "correcto de la documentación completa."
)

doc.add_heading_level2("Para Instructores TCU")
doc.add_paragraph(
    "No compartir materiales didácticos o manuales con los participantes para evitar conflictos "
    "de propiedad intelectual y proteger la integridad del programa."
)

# ============================================================
# REFERENCIAS
# ============================================================
doc.add_references_section([
    "CECI MICITT. (2026). Programa de Trabajo Comunal Universitario: Capacitación en tecnologías digitales. San José, Costa Rica.",
    "Ministerio de Ciencia, Innovación, Tecnología y Telecomunicaciones. (2024). Lineamientos para programas de alfabetización digital. MICITT.",
    "Cisco Networking Academy. (2025). Ciberseguridad: Curso introductorio. Cisco Systems.",
    "Oracle University. (2025). Programación web: Fundamentos de HTML, CSS y JavaScript. Oracle Corporation."
])

# --- Guardar ---
output_dir = r"{{USER_DIR}}\OneDrive\Documentos\Archivos OpenCode\Documentos"
output_path = f"{output_dir}\\Summary TCU CECI Micitt.docx"
doc.save(output_path)
print(f"Documento guardado en: {output_path}")

