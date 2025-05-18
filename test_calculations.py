import sys
import unittest
import math
from app import calculate_trig_function


class TestTrigCalculations(unittest.TestCase):
    def test_sin_30_degrees(self):
        result = calculate_trig_function('sin', 30, 'degrees', 2)
        self.assertAlmostEqual(result, 0.5, delta=0.001)

    def test_negative_zero(self):
        result = calculate_trig_function('sin', -0.0, 'degrees', 2)
        self.assertEqual(result, -0.0)

    def test_cos_radians(self):
        result = calculate_trig_function('cos', 0.523333, 'radians', 4)
        self.assertAlmostEqual(result, 0.8661, delta=0.001)


    def test_tan_270_degrees(self):
        result = calculate_trig_function('tan', 270, 'degrees', 2)
        self.assertEqual(result, "inf")

    def test_tan_90_degrees(self):
        result = calculate_trig_function('tan', 90, 'degrees', 2)
        self.assertEqual(result, "inf")

    def test_tan_0_degrees(self):
        result = calculate_trig_function('tan', 0, 'degrees', 2)
        self.assertEqual(result, 0.0)

    def test_cot_90_degrees(self):
        result = calculate_trig_function('cot', 90, 'degrees', 2)
        self.assertAlmostEqual(result, 0.0, delta=0.001)

    def test_cot_0_degrees(self):
        result = calculate_trig_function('cot', 0, 'degrees', 2)
        self.assertEqual(result, "inf")


    def test_tan_close_to_90(self):
        """Проверка значений, близких к 90°"""
        result = calculate_trig_function('tan', 89.9999, 'degrees', 4)
        expected = math.tan(math.radians(89.9999))
        self.assertAlmostEqual(result, expected, delta=0.0001)

        # Проверка, что результат действительно очень большой
        self.assertGreater(abs(result), 100000)

    def test_extreme_precision(self):
        """Проверка экстремальной точности (10 знаков)"""
        result = calculate_trig_function('sin', 30, 'degrees', 10)
        self.assertAlmostEqual(result, 0.5, delta=1e-10)

    def test_periodicity(self):
        """Проверка периодичности тригонометрических функций"""
        result1 = calculate_trig_function('sin', 30, 'degrees', 10)
        result2 = calculate_trig_function('sin', 390, 'degrees', 10)
        self.assertAlmostEqual(result1, result2, delta=1e-10)

    def test_negative_angle(self):
        """Проверка отрицательных углов"""
        result = calculate_trig_function('sin', -45, 'degrees', 5)
        self.assertAlmostEqual(result, -math.sqrt(2)/2, delta=0.00001)

    def test_giant_angle_degrees(self):
        """Угол больше 1e10 градусов (проверка переполнения)"""
        result = calculate_trig_function('sin', 1e10, 'degrees', 2)
        self.assertAlmostEqual(result, math.sin(math.radians(1e10 % 360)), delta=0.01)

    def test_angle_precision_limits(self):
        """Очень маленький угол (близкий к машинному эпсилон)"""
        angle = sys.float_info.epsilon  # Минимальное положительное число
        result = calculate_trig_function('sin', angle, 'degrees', 10)
        self.assertAlmostEqual(result, math.sin(math.radians(angle)), delta=1e-10)


class TestInvalidInputs(unittest.TestCase):
    def test_invalid_function_name(self):
        with self.assertRaises(ValueError):
            calculate_trig_function('sec', 45, 'degrees', 2)  # sec не поддерживается

    def test_invalid_unit_type(self):
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', 45, 'gradians', 2)  # только degrees/radians

    def test_non_numeric_angle(self):
        """Проверка нечислового значения угла"""
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', 'forty-five', 'degrees', 2)

    def test_negative_precision(self):
        """Проверка отрицательной точности"""
        with self.assertRaises(ValueError):
            calculate_trig_function('cos', 60, 'degrees', -1)

    def test_extreme_precision(self):
        """Проверка слишком большой точности (>15 знаков)"""
        with self.assertRaises(ValueError):
            calculate_trig_function('tan', 30, 'degrees', 20)

    def test_none_values(self):
        """Проверка передачи None в параметрах"""
        with self.assertRaises(ValueError):
            calculate_trig_function(None, 45, 'degrees', 2)
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', None, 'degrees', 2)

    def test_empty_string_input(self):
        """Проверка пустых строк"""
        with self.assertRaises(ValueError):
            calculate_trig_function('', 45, 'degrees', 2)
        with self.assertRaises(ValueError):
            calculate_trig_function('cos', '', 'degrees', 2)

    def test_whitespace_input(self):
        """Проверка строк с пробелами"""
        with self.assertRaises(ValueError):
            calculate_trig_function('  ', 45, 'degrees', 2)
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', '  ', 'degrees', 2)

    def test_special_symbols(self):
        """Проверка специальных символов"""
        with self.assertRaises(ValueError):
            calculate_trig_function('@#$', 45, 'degrees', 2)
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', '45°', 'degrees', 2)

    def test_boolean_input(self):
        """Проверка булевых значений"""
        with self.assertRaises(ValueError):
            calculate_trig_function(True, 45, 'degrees', 2)
        with self.assertRaises(ValueError):
            calculate_trig_function('sin', False, 'degrees', 2)

if __name__ == '__main__':
    unittest.main()