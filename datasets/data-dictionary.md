
# Diccionario de datos

## clientes.csv

| Variable | Tipo | Descripción |
|---|---|---|
| cliente_id | entero | Identificador sintético único |
| segmento | categoría | Perfil comercial inicial |
| antiguedad_meses | entero | Meses desde el alta |
| compras_90d | entero | Compras en los últimos noventa días |
| ticket_promedio | decimal | Importe medio por compra |
| reclamos_180d | entero | Reclamos en los últimos ciento ochenta días |
| abandono_30d | binaria | Evento sintético en los treinta días siguientes |

## ventas-mensuales.csv

| Variable | Tipo | Descripción |
|---|---|---|
| fecha | fecha | Primer día del mes |
| ventas | decimal | Nivel sintético mensual |
| promocion | binaria | Mes con promoción planificada |
| feriado | binaria | Indicador de período festivo |

## operaciones.csv

| Variable | Tipo | Descripción |
|---|---|---|
| orden_id | entero | Identificador sintético |
| producto | categoría | Familia A, B o C |
| horas_maquina | decimal | Consumo estimado de capacidad |
| materia_prima | decimal | Consumo estimado de insumo |
| margen | decimal | Contribución sintética |
