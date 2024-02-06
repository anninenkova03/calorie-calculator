import streamlit as st
import httpx
from model import Food
import numpy as np

# Base URL for the API
backend_url = "http://backend:8000"

# Streamlit UI
def main():
    st.title("Macronutrient Calculator App")

    menu = ["Home",
            "Journal",
            "Macros",
            "Add Food"
            ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Macronutrient Calculator App!")

    elif choice == "Journal":
        st.subheader("Journal")
        #st.write("No food added to journal so far.")
        response = httpx.get(f"{backend_url}/api/food/all")
        foods = response.json()
        print(foods)
        if isinstance(foods, list):
            for food in foods:
                st.write(f"{food['name']},  {food['amount']}g")
        else:
            st.write("No food added to journal so far.")

    elif choice == "Macros":
            st.subheader("Macros")
            response = httpx.get(f"{backend_url}/api/food/all")
            foods = response.json()
            print(foods)
            if isinstance(foods, list):
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
                st.error("Failed to add food. Please make sure there isn't a food with that name already and try again.")




    elif choice == "Delete Food":
            st.subheader("Delete Food")
            name = st.text_input("Food")
            if st.button("Delete"):
                response = httpx.delete(f"{backend_url}/api/food/delete/{name}")
                if response.status_code == 200:
                    st.success("Food deleted successfully!")
                else:
                    st.error("Failed to delete food. Please check the name of the food and try again.")

    elif choice == "Add Food from List":
        st.subheader("Add Food from List")
        name = st.text_input("Food")
        amount = st.text_input("Amount in g")
        if st.button("Add"):
            #food = Food(name=name, macros=np.array([1, 2, 3]), amount=amount)
            response = httpx.put(f"{backend_url}/api/food/update/{name}", json={"name": name})
            #response = httpx.post(f"{backend_url}/api/food/add", json=food.dict())
            if response.status_code == 200:
                st.success("Food added successfully!")
            else:
                st.error("Failed to add food. Please try again later.")

    elif choice == "Edit Food Macros":
        st.subheader("Edit Food on List")
        name = st.text_input("Food")
        carbs = st.text_input("Carbs per 100g")
        protein = st.text_input("Protein per 100g")
        fat = st.text_input("Fat per 100g")
        #print(f"This is name {name} and this is macros {macros}")
        if st.button("Edit"):
            response = httpx.put(f"{backend_url}/api/food/update/{name}", json={"name": name, "macros": macros})
            if response.status_code == 200:
                st.success("Food macros edited successfully!")
            else:
                st.error("Failed to edit macros. Please make sure the food is on the list and try again.")


if __name__ == "__main__":
    main()
