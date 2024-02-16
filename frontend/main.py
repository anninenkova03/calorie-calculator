import streamlit as st
import httpx
from model import Food

# Base URL for the API
backend_url = "http://backend:8000"

# Streamlit UI
def main():
    st.title("Calorie Calculator App")

    menu = ["Home",
            "Journal",
            "Macros",
            "Add Food",
            "Delete Food"
            ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Calorie Calculator App!")

    elif choice == "Journal":
        st.subheader("Journal")
        response = httpx.get(f"{backend_url}/api/food/all")
        foods = response.json()
        if foods:
            for food in foods:
                st.write(f"{food['name']},  {food['amount']}g")
            response = httpx.get(f"{backend_url}/api/food/calories")
            calories = response.json()
            st.write(f"Logged food amounts to a total of {calories} kcal.")
        else:
            st.write("No food added to the journal so far.")

    elif choice == "Macros":
        st.subheader("Macronutrients per 100g")
        response = httpx.get(f"{backend_url}/api/food/all")
        foods = response.json()
        if foods:
            for food in foods:
                st.write(f"{food['name']}:  {food['carbs']}g carbs, {food['fat']}g fat, {food['protein']}g protein")
        else:
            st.write("No macros logged so far.")

    elif choice == "Add Food":
        st.subheader("Add Food")
        name = st.text_input("Food")
        carbs = st.number_input("Carbs per 100g", step=1, value=0, format="%d")
        fat = st.number_input("Fat per 100g", step=1, value=0, format="%d")
        protein = st.number_input("Protein per 100g", step=1, value=0, format="%d")
        amount = st.number_input("Amount in g", step=1, value=0, format="%d")
        if st.button("Add"):
            food = Food(name=name, carbs=carbs, fat=fat, protein=protein, amount=amount)
            response = httpx.post(f"{backend_url}/api/food/add", json=food.dict())
            if response.status_code == 200:
                st.success("Food added successfully!")
            else:
                st.error("Failed to add food. Please make sure there isn't any food with that name already and the macronutrients sum up to 100g.")

    elif choice == "Delete Food":
        st.subheader("Delete Food")
        name = st.text_input("Food")
        if st.button("Delete"):
            response = httpx.delete(f"{backend_url}/api/food/delete/{name}")
            if response.status_code == 200:
                st.success("Food deleted successfully!")
            else:
                st.error("Failed to delete food. Please make sure food with that name has been added and try again.")

if __name__ == "__main__":
    main()
