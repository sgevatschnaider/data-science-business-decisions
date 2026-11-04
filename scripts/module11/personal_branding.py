"""Keep the public neural-network module identified as a personal repository."""
import re


def personal_branding(text: str) -> str:
    replacements = {
        '<p class="muted">Jueves 5 de noviembre · 9:30 a 12:00 · UCA</p>': '',
        'Guía de estudio UCA:': 'Guía de estudio de Sergio Gevatschnaider:',
        'Material UCA:': 'Material de Sergio Gevatschnaider:',
        'UCA · Ciencias de Datos II · Módulo 12 del programa': 'Repositorio personal · Sergio Gevatschnaider · Módulo 12',
        'UCA · Ciencias de Datos II': 'Repositorio personal · Sergio Gevatschnaider',
        'Sergio Gevatschnaider · UCA · Ciencias de Datos II · 2026': 'Sergio Gevatschnaider · Repositorio personal · 2026',
        'Sergio Gevatschnaider · UCA · 2026': 'Sergio Gevatschnaider · Repositorio personal · 2026',
        'Datos y Decisiones · UCA': 'Datos y Decisiones · Sergio Gevatschnaider',
        'Ruta principal: 28 diapositivas para el jueves 5/11, 9:30–12:00.': 'Ruta principal: 28 diapositivas esenciales para estudiar a tu ritmo.',
        'Clase del jueves 5/11/2026 · 150 minutos': 'Recorrido de estudio sugerido · 150 minutos',
        '<th>Horario</th>': '<th>Tiempo transcurrido</th>',
        '9:30–9:45': '0–15 min', '9:45–10:03': '15–33 min',
        '10:03–10:15': '33–45 min', '10:15–10:45': '45–75 min',
        '10:45–11:05': '75–95 min', '11:05–11:20': '95–110 min',
        '11:20–11:45': '110–135 min', '11:45–12:00': '135–150 min',
        'Sergio Gevatschnaider · Repositorio personal · Sergio Gevatschnaider · 2026': 'Sergio Gevatschnaider · Repositorio personal · 2026',
        ' · UCA': '', 'UCA · ': '',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r'\bUCA\b', 'Repositorio personal', text)
