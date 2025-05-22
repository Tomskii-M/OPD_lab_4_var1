from flask import Flask, render_template, request
import math

app = Flask(__name__)


def calculate_trig_function(function, angle, unit, precision):
    """
        Вычисляет тригонометрическую функцию с обработкой особых случаев
    """

    valid_functions = ['sin', 'cos', 'tan', 'cot']
    if not isinstance(function, str) or function not in valid_functions:
        raise ValueError(f"Недопустимая функция")

    valid_units = ['degrees', 'radians']
    if not isinstance(unit, str) or unit not in valid_units:
        raise ValueError(f"Недопустимая единица измерения: {unit}. Используйте degrees или radians")

    if isinstance(angle, bool):
        raise ValueError("Булевы значения (True/False) недопустимы в качестве угла")
    try:
        angle = float(angle)
    except (ValueError, TypeError):
        raise ValueError(f"Угол должен быть числом, получено: {angle}")

    if not isinstance(precision, int) or precision < 0 or precision > 10:
        raise ValueError(f"Точность должна быть целым числом от 0 до 10, получено: {precision}")

    try:
        # Конвертируем в радианы если нужно
        if unit == 'degrees':
            angle_rad = math.radians(angle)
        elif unit == 'radians':
            angle_rad = angle

        # Вычисляем выбранную функцию
        if function == 'sin':
            value = math.sin(angle_rad)
        elif function == 'cos':
            value = math.cos(angle_rad)
        elif function == 'tan':
            if math.degrees(angle_rad) % 360 in [90.0, 270.0]:
                value = "inf"
            else:
                value = math.tan(angle_rad)
        elif function == 'cot':
            if math.degrees(angle_rad) % 360 in [0.0, 180.0]:
                value = "inf"
            else:
                value = 1 / math.tan(angle_rad)

        # Округляем если возможно
        try:
            return round(value, precision)
        except (TypeError, ValueError):
            return value

    except (ValueError, TypeError) as e:
        raise ValueError(f"Ошибка вычисления: {str(e)}")


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        function='sin',
        angle='',
        unit='degrees',
        precision=2,
        result=None
    )


@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        # Получаем данные из формы
        try:
            function = request.form.get('function')
            angle = float(request.form.get('angle'))
            unit = request.form.get('unit')
            precision = int(request.form.get('precision'))

            result = calculate_trig_function(function, angle, unit, precision)

            return render_template(
                'index.html',
                function=function,
                angle=angle,
                unit=unit,
                precision=precision,
                result=result
            )
        except Exception as e:
            return render_template(
                'index.html',
                function='sin',
                angle='',
                unit='degrees',
                precision=2,
                result=f"Ошибка: {str(e)}"
            )


@app.errorhandler(404)
def page_not_found(e):
    return f"ERROR: {e}", 404


if __name__ == '__main__':
    app.run(debug=True)
