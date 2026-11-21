export const missing_dates = [
    '2015-09-24',
    '2015-09-25',
    '2015-10-05',
    '2015-10-12',
    '2015-10-19',
    '2015-10-26',
    '2015-12-25',
]

export const model_info = {
    name: 'PizzaDemandWeekdayBaseline',
    version: '1',
    strategy: 'Promedio por día de semana',
}

export const model_scores = [
    { strategy: 'Promedio general', mae: 21.61 },
    { strategy: 'Promedio por día de semana', mae: 18.33 },
    { strategy: 'Random Forest', mae: 18.94 },
]

export const pipeline_demo = [
    {
        id: 'Ejemplo',
        start: 'Pendiente',
        end: 'Pendiente',
        duration: '—',
        status: 'Sin datos de Airflow',
        tone: 'pending',
        logs: 'Conecta Airflow para consultar ejecuciones reales.',
    },
]

export const sales_demo = [
    {
        id: 1,
        order_id: 1001,
        date: '2015-10-01',
        time: '12:00',
        product: 'Classic Deluxe',
        category: 'Classic',
        size: 'M',
        quantity: 2,
        price: 14,
        amount: 28,
    },
    {
        id: 2,
        order_id: 1002,
        date: '2015-10-02',
        time: '13:30',
        product: 'Chicken BBQ',
        category: 'Chicken',
        size: 'L',
        quantity: 1,
        price: 18,
        amount: 18,
    },
    {
        id: 3,
        order_id: 1003,
        date: '2015-10-03',
        time: '18:15',
        product: 'Veggie Garden',
        category: 'Veggie',
        size: 'S',
        quantity: 3,
        price: 11,
        amount: 33,
    },
    {
        id: 4,
        order_id: 1004,
        date: '2015-10-04',
        time: '14:20',
        product: 'Supreme',
        category: 'Supreme',
        size: 'M',
        quantity: 2,
        price: 16,
        amount: 32,
    },
    {
        id: 5,
        order_id: 1005,
        date: '2015-10-06',
        time: '19:10',
        product: 'Classic Deluxe',
        category: 'Classic',
        size: 'L',
        quantity: 1,
        price: 19,
        amount: 19,
    },
    {
        id: 6,
        order_id: 1006,
        date: '2015-10-07',
        time: '20:05',
        product: 'Chicken BBQ',
        category: 'Chicken',
        size: 'M',
        quantity: 2,
        price: 15,
        amount: 30,
    },
]

