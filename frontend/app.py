# frontend/app.py
import streamlit as st
import requests
import os

# Use 'backend' as the host if running inside Docker Compose, otherwise use 'localhost' if running locally.
API_URL = os.environ.get("API_URL", "http://backend:8000")

st.title("CRM System")

pages = ["Customers", "Orders"]
page = st.sidebar.selectbox("Select Page", pages)

if page == "Customers":
    st.header("Add New Customer")
    name = st.text_input("Customer Name")
    email = st.text_input("Customer Email")
    if st.button("Create Customer"):
        if name and email:
            response = requests.post(f"{API_URL}/customers/", json={"name": name, "email": email})
            if response.status_code == 200:
                st.success("Customer created successfully!")
                st.rerun()
            else:
                st.error("Error creating customer.")
        else:
            st.warning("Please provide both name and email.")

    st.header("Customer List")
    try:
        customers = requests.get(f"{API_URL}/customers/").json()
    except Exception as e:
        st.error("Cannot connect to backend. Please ensure the backend is running and accessible.")
        st.stop()

    for cust in customers:
        st.subheader(f"{cust['name']} ({cust['email']})")
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"Delete Customer {cust['id']}", key=f"delcust{cust['id']}"):
                resp = requests.delete(f"{API_URL}/customers/{cust['id']}")
                if resp.status_code == 200:
                    st.success("Customer deleted.")
                    st.rerun()
        with c2:
            with st.form(f"update_customer_{cust['id']}"):
                new_name = st.text_input("New Name", value=cust['name'], key=f"ucustname{cust['id']}")
                new_email = st.text_input("New Email", value=cust['email'], key=f"ucustemail{cust['id']}")
                if st.form_submit_button("Update Customer"):
                    resp = requests.put(f"{API_URL}/customers/{cust['id']}", json={"name": new_name, "email": new_email})
                    if resp.status_code == 200:
                        st.success("Customer updated.")
                        st.rerun()
                    else:
                        st.error("Error updating customer.")

elif page == "Orders":
    st.header("Orders")
    customers = requests.get(f"{API_URL}/customers/").json()
    customer_options = {f"{c['name']} ({c['email']})": c['id'] for c in customers}
    selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
    customer_id = customer_options[selected_customer] if selected_customer else None

    st.subheader("Add Order")
    item = st.text_input("Order Item")
    if st.button("Add Order"):
        if item and customer_id:
            resp = requests.post(f"{API_URL}/customers/{customer_id}/orders/", json={"item": item})
            if resp.status_code == 200:
                st.success("Order added.")
                st.rerun()
            else:
                st.error("Error adding order.")
        else:
            st.warning("Order item and customer required.")

    st.subheader("Order List")
    if customer_id:
        orders = requests.get(f"{API_URL}/customers/{customer_id}/orders/").json()
        for idx, order in enumerate(orders):
            st.write(f"- {order['item']}")
            ocol1, ocol2 = st.columns(2)
            with ocol1:
                # Make the key unique by including both order id and customer id (or index)
                if st.button(f"Delete Order {order['id']}", key=f"delorder{order['id']}_{customer_id}_{idx}"):
                    resp = requests.delete(f"{API_URL}/orders/{order['id']}")
                    if resp.status_code == 200:
                        st.success("Order deleted.")
                        st.rerun()
            with ocol2:
                with st.form(f"update_order_{order['id']}_{customer_id}_{idx}"):
                    new_item = st.text_input("New Item", value=order['item'], key=f"uorderitem{order['id']}_{customer_id}_{idx}")
                    if st.form_submit_button("Update Order"):
                        resp = requests.put(f"{API_URL}/orders/{order['id']}", json={"item": new_item})
                        if resp.status_code == 200:
                            st.success("Order updated.")
                            st.rerun()
                        else:
                            st.error("Error updating order.")
