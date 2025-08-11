import streamlit as st
import pandas as pd

def calculate_bmr(weight, height, age, gender):
    if gender == 'ذكر':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def estimate_body_fat_percentage(weight, height, age, gender):
    bmi = weight / ((height / 100) ** 2)
    if gender == 'ذكر':
        return 1.20 * bmi + 0.23 * age - 16.2
    else:
        return 1.20 * bmi + 0.23 * age - 5.4

def get_activity_factor(level):
    factors = {
        'خامل': 1.2,
        'نشاط خفيف': 1.375,
        'نشاط متوسط': 1.55,
        'نشاط عالي': 1.725,
        'نشاط مكثف': 1.9
    }
    return factors.get(level, 1.2)

st.title("برنامج Hala Tamer")

weight = st.number_input("الوزن (كجم)", min_value=30.0, max_value=200.0, step=0.1)
height = st.number_input("الطول (سم)", min_value=100.0, max_value=250.0, step=0.1)
age = st.number_input("العمر (سنة)", min_value=10, max_value=100, step=1)
gender = st.selectbox("الجنس", ['ذكر', 'أنثى'])
activity_level = st.selectbox("مستوى النشاط اليومي", ['خامل', 'نشاط خفيف', 'نشاط متوسط', 'نشاط عالي', 'نشاط مكثف'])
goal = st.selectbox("الهدف", ['زيادة وزن', 'نقصان وزن', 'ثبات وزن'])

if st.button("حساب"):
    bmr = calculate_bmr(weight, height, age, gender)
    activity_factor = get_activity_factor(activity_level)
    tdee = bmr * activity_factor

    if goal == 'زيادة وزن':
        target_calories = tdee * 1.15
    elif goal == 'نقصان وزن':
        target_calories = tdee * 0.85
    else:
        target_calories = tdee

    body_fat = estimate_body_fat_percentage(weight, height, age, gender)
    st.write(f"معدل الأيض الأساسي (BMR): {bmr:.2f} سعر حراري")
    st.write(f"معدل الحرق اليومي (TDEE): {tdee:.2f} سعر حراري")
    st.write(f"السعرات المستهدفة حسب الهدف: {target_calories:.2f} سعر حراري")
    st.write(f"نسبة الدهون التقريبية في الجسم: {body_fat:.2f}%")
    
    try:
        meals_df = pd.read_excel('meal_plans_3_systems_100_each.xlsx')
        system_map = {'زيادة وزن': 'تضخيم', 'نقصان وزن': 'تنشيف', 'ثبات وزن': 'وزن ثابت'}
        selected_system = system_map.get(goal)
        filtered_meals = meals_df[meals_df['النظام'] == selected_system]
        st.write(f"عدد الوجبات المتاحة للنظام: {len(filtered_meals)}")
        st.write(filtered_meals.head())
    except Exception as e:
        st.error(f"خطأ في تحميل ملف الوجبات: {e}")
        
    try:
        training_df = pd.read_excel('workout_plans_100_systems.xlsx')
        st.write("نماذج أنظمة التدريب:")
        st.write(training_df.head(10))
    except Exception as e:
        st.error(f"خطأ في تحميل ملف أنظمة التدريب: {e}")