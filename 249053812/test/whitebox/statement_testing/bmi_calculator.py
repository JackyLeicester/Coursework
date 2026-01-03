class BMICalculator:
    @staticmethod
    def bmi_calculator(weight, height):
        bmi = weight / (height * height)
        if bmi >= 30:
            return "obesity"
        elif 25 <= bmi < 30:
            return "overweight"
        elif 18.5 <= bmi < 25:
            return "healthy"
        elif 0 <= bmi < 18.5:
            return "underweight"
        return "error"
