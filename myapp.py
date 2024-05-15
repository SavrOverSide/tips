import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64
import io

st.write("""
# Исследование по чаевым (датасет tips.csv)
         
""")

df = pd.read_csv('/home/savr/tips.csv')
st.write('База данных чаевых')
st.dataframe(df)

# Прочитаем датасет в переменную tips
tips = pd.read_csv('/home/savr/tips.csv')

# Создание столбца time_order
# Заполнение его случайной датой в промежутке от 2023-01-01 до 2023-01-31
random_dates = pd.date_range(start='2023-01-01', end='2023-01-31', periods=len(tips))

tips['time_order'] = random_dates

# Создание интерфейса Streamlit
st.write('Анализ динамики чаевых')

### Построение графика динамики чаевых во времени

df = tips

df['time_order'] = pd.to_datetime(df['time_order'])

fig = plt.figure(figsize=(10, 6))  
plt.plot(df['time_order'], df['tip'], marker='o', linestyle='-', color='blue') 

plt.xlabel('Дата')
plt.ylabel('Чаевые')
plt.title('Динамика чаевых во времени')

st.pyplot(fig)

### Рисование гистограммы total_bill

fig2 = plt.figure(figsize=(10, 6))  
plt.hist(df['total_bill'], bins=20, edgecolor='black')  


plt.xlabel('Total Bill')
plt.ylabel('Frequency')
plt.title('Distribution of Total Bills')

st.write('Гистограмма total_bill')
st.pyplot(fig2)

### Рисование scatterplot, показывающий связь между total_bill and tip
fig, ax = plt.subplots()

# Создание диаграммы рассеяния с использованием seaborn
sns.scatterplot(data=df, x='total_bill', y='tip', hue='sex', style='sex', size='size', sizes=(30, 200), ax=ax)

# Настройка подписей осей и заголовка
ax.set_xlabel('Total Bill')
ax.set_ylabel('Tip')
ax.set_title('Relationship between Total Bill and Tip')

# Сохранение фигуры в переменную
fig3 = fig

st.write('Scatterplot, показывающий связь между total_bill and tip')

# Отображение фигуры в Streamlit
st.pyplot(fig3)

### Рисование 1 графика, связывающего total_bill, tip, и size
fig4 = sns.pairplot(df, vars=['total_bill', 'tip', 'size'], hue='sex')


plt.suptitle('Relationships between Total Bill, Tip, and Size', fontsize=14)
plt.tight_layout()

st.write('График, связывающий total_bill, tip и size')
st.pyplot(fig4)

# Показ связи между днем недели и размером счета
fig, ax = plt.subplots()
sns.boxplot(x='day', y='total_bill', data=df)


plt.xlabel('Day of Week')
plt.ylabel('Total Bill')
plt.title('Boxplot of Total Bill by Day of Week')

fig5 = fig

st.write('Связь между днём недели и размером счёта')
st.pyplot(fig5)

### Рисование scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='tip', y='day', hue='sex', style='sex', size='size', sizes=(30, 200))


plt.xlabel('Tip')
plt.ylabel('Day of Week')
plt.title('Relationship between Tip and Day of Week')

fig6 = fig

st.write('Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу')
st.pyplot(fig6)

### Рисование box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)

grouped_data = df.groupby(['day', 'time'])['total_bill'].sum().reset_index()

fig, ax = plt.subplots()
sns.boxplot(x='day', y='total_bill', hue='time', data=grouped_data)


plt.xlabel('Day of Week')
plt.ylabel('Sum of Total Bill')
plt.title('Boxplot of Sum of Total Bill by Day and Time')

fig7 = fig

st.write('box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)')
st.pyplot(fig7)

## Рисование 2 гистограмм чаевых на обед и ланч. Расположение их рядом по горизонтали.
# Фильтрация данных для обеда и ланча
lunch_data = df[df['time'] == 'Lunch']['tip']
dinner_data = df[df['time'] == 'Dinner']['tip']

# Создание фигуры с двумя подграфиками
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Создание гистограммы чаевых на обед
sns.histplot(lunch_data, ax=axs[0], kde=False, bins=20, color='blue', label='Lunch')

# Создание гистограммы чаевых на ужин
sns.histplot(dinner_data, ax=axs[1], kde=False, bins=20, color='red', label='Dinner')


axs[0].set_title('Tip Distribution at Lunch')
axs[0].set_xlabel('Tip Amount')
axs[0].set_ylabel('Frequency')
axs[1].set_title('Tip Distribution at Dinner')
axs[1].set_xlabel('Tip Amount')
axs[1].set_ylabel('Frequency')


axs[0].legend()
axs[1].legend()

fig8 = fig

st.write('2 гистограммы чаевых на обед и ланч')
st.pyplot(fig8)

### Рисование 2 scatterplots (для мужчин и женщин), показав связь размера счета и чаевых, дополнительно разбив по курящим/некурящим. 
### Расположение их по горизонтали.
# Создание фигуры с двумя подграфиками
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Создание scatterplot для мужчин
sns.scatterplot(data=df[(df['sex'] == 'Male') & (df['smoker'] == 'No')], x='total_bill', y='tip', ax=axs[0], label='Non-smoking Men')
sns.scatterplot(data=df[(df['sex'] == 'Male') & (df['smoker'] == 'Yes')], x='total_bill', y='tip', ax=axs[0], label='Smoking Men', color='red')

# Создание scatterplot для женщин
sns.scatterplot(data=df[(df['sex'] == 'Female') & (df['smoker'] == 'No')], x='total_bill', y='tip', ax=axs[1], label='Non-smoking Women')
sns.scatterplot(data=df[(df['sex'] == 'Female') & (df['smoker'] == 'Yes')], x='total_bill', y='tip', ax=axs[1], label='Smoking Women', color='red')


axs[0].set_title('Scatterplot for Men')
axs[0].set_xlabel('Total Bill')
axs[0].set_ylabel('Tip')
axs[1].set_title('Scatterplot for Women')
axs[1].set_xlabel('Total Bill')
axs[1].set_ylabel('Tip')


axs[0].legend()
axs[1].legend()

fig9 = fig

st.write('Scatterplots (для мужчин и женщин), показавывающие связь размера счета и чаевых, дополнительно разбив по курящим/некурящим')
st.pyplot(fig9)

### Построение тепловой карты зависимостей численных переменных

# Вычисление корреляции между численными переменными
correlation_matrix = df[['total_bill', 'tip']].corr()

# Создание тепловой карты
fig, axs = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

fig10 = fig

plt.title('Correlation Heatmap of Numerical Variables')

st.write('Тепловая карта зависимостей численных переменных')
st.pyplot(fig10)

# Добавление виджетов в боковую панель
with st.sidebar:
    # Текстовое поле ввода
    user_name = st.text_input('Введите ваше имя: ')
    st.write(f"Привет, {user_name}!")

    # Кнопка
    if st.button('Нажмите меня'):
        st.write('Вы нажали кнопку!')

    # Радио-кнопки
    shipping_method = st.radio(
        "Выберите способ доставки",
        ("Стандарт (5-15 дней)", "Экспресс (2-5 дней)")
    )
    st.write(f"Выбран способ доставки: {shipping_method}")

    # Выпадающий список
    contact_method = st.selectbox(
        "Как вам бы хотелось связаться?",
        ("Email", "Домашний телефон", "Мобильный телефон")
    )
    st.write(f"Выбран способ связи: {contact_method}")


