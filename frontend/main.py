import streamlit as st
import httpx
from model import Todo

# Base URL for the API
backend_url = "http://backend:8000"

# Streamlit UI
def main():
    st.title("Macronutrient Calculator App")

    menu = ["Home--",
            "Journal",
            "Add Food from List",
            "Add Custom Food",
            "Food List--",
            "Edit Food on List",
            "Delete Food from List--"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Macronutrient Calculator App!")

    elif choice == "Food List":
            st.subheader("Food List")
            response = httpx.get(f"{backend_url}/api/todo/all")
            foods = response.json()
            print(foods)
            if isinstance(foods, list):
                for food in foods:
                    st.write(f"{food['title']}:  {food['description']}")
            else:
                st.write("No foods available.")

    elif choice == "Delete Food from List":
            st.subheader("Delete Food from List")
            food = st.text_input("Food")
            if st.button("Delete"):
                response = httpx.delete(f"{backend_url}/api/todo/delete/{food}")
                if response.status_code == 200:
                    st.success("Food deleted successfully from the list!")
                else:
                    st.error("Failed to delete food. Please make sure the food is on the list and try again.")

    #if choice == "Journal":
    #if choice == "Add Food from List":
    #if choice == "Add Custom Food":
    #if choice == "Edit Food on List":







    elif choice == "Add Todo":
        st.subheader("Add Todo")
        title = st.text_input("Title")
        description = st.text_area("Description")
        if st.button("Add"):
            todo = Todo(title=title, description=description)
            response = httpx.post(f"{backend_url}/api/todo/add", json=todo.dict())
            if response.status_code == 200:
                st.success("Todo added successfully!")
            else:
                st.error("Failed to add todo. Please try again later.")

    elif choice == "Update Todo":
        st.subheader("Update Todo")
        title = st.text_input("Title")
        description = st.text_area("Description")
        print(f"This is title {title} and this is description {description}")
        if st.button("Update"):
            response = httpx.put(f"{backend_url}/api/todo/update/{title}", json={"title": title, "description": description})
            if response.status_code == 200:
                st.success("Todo updated successfully!")
            else:
                st.error("Failed to update todo. Please make sure the title exists and try again.")

    elif choice == "Delete Todo":
        st.subheader("Delete Todo")
        title = st.text_input("Title")
        if st.button("Delete"):
            response = httpx.delete(f"{backend_url}/api/todo/delete/{title}")
            if response.status_code == 200:
                st.success("Todo deleted successfully!")
            else:
                st.error("Failed to delete todo. Please make sure the title exists and try again.")

if __name__ == "__main__":
    main()
