import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Настройки страницы
st.set_page_config(page_title="Аналитика оттока клиентов", layout="wide")

st.title("📉 Прогноз оттока клиентов")
st.markdown("Интерактивный дашборд по вероятности ухода клиентов")

# === Загрузка файла ===
uploaded_file = st.file_uploader("📂 Загрузите CSV с данными клиентов", type=["csv"])

# === Вкладки ===
tab1, tab2 = st.tabs(["📊 Аналитика оттока", "💡 Рекомендации по удержанию"])

# -----------------------------
# 📊 ВКЛАДКА 1 — АНАЛИТИКА ОТТОКА
# -----------------------------
with tab1:
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "Вероятность_оттока" not in df.columns:
            st.error("⚠️ В файле должна быть колонка 'Вероятность_оттока'")
        else:
            segment = st.selectbox(
                "Выберите сегмент риска", ["Все", "Надёжный", "Группа риска", "Высокий риск"]
            )

            if segment != "Все":
                df = df[df["Сегмент"] == segment]

            avg_prob = df["Вероятность_оттока"].mean()
            high_risk = (df["Вероятность_оттока"] > 0.6).mean() * 100

            col1, col2 = st.columns(2)
            col1.metric("Средняя вероятность ухода", f"{avg_prob:.2f}")
            col2.metric("Доля клиентов с высоким риском", f"{high_risk:.1f}%")

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df["Вероятность_оттока"], bins=10, color="coral", edgecolor="black")
            ax.set_title("Распределение вероятности оттока клиентов")
            ax.set_xlabel("Вероятность ухода")
            ax.set_ylabel("Количество клиентов")
            st.pyplot(fig)

            st.subheader("🔝 Топ клиентов с высоким риском ухода")
            st.dataframe(
                df.sort_values("Вероятность_оттока", ascending=False).head(15),
                use_container_width=True,
            )
    else:
        st.info("👆 Загрузите CSV-файл с результатами прогноза (включая 'Вероятность_оттока' и 'Сегмент').")

# -----------------------------
# 💡 ВКЛАДКА 2 — РЕКОМЕНДАЦИИ
# -----------------------------
with tab2:
    st.subheader("💡 Индивидуальные рекомендации по удержанию клиентов")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "Вероятность_оттока" not in df.columns:
            st.warning("⚠️ В файле нет данных о вероятности оттока.")
        else:
            def рекомендации(row):
                if row["Вероятность_оттока"] > 0.8:
                    return "📞 Персональное предложение + звонок менеджера"
                elif row["Вероятность_оттока"] > 0.6:
                    return "💌 Отправить промокод или письмо с бонусом"
                elif row["Вероятность_оттока"] > 0.4:
                    return "🎁 Предложить скидку 10% на следующий заказ"
                else:
                    return "✅ Клиент лоялен, поддерживать коммуникацию"

            df["Рекомендация"] = df.apply(рекомендации, axis=1)

            st.dataframe(
                df[["Средний_чек", "Количество_покупок", "Вероятность_оттока", "Рекомендация"]]
                .sort_values("Вероятность_оттока", ascending=False)
                .head(15),
                use_container_width=True,
            )
    else:
        st.info("⬆️ Загрузите CSV с вероятностями оттока, чтобы увидеть рекомендации.")
