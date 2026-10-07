import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from vehicle_module import Vehicle, PremiumVehicle


# PAGE SETTINGS
st.set_page_config(
    page_title="AutoCare Service Centre",
    page_icon="🚗",
    layout="centered"
)


st.markdown("""
<style>

    /* Main page width */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        margin: auto;
    }

    /* Center main headings */
    h1 {
        text-align: center;
        font-size: 42px !important;
    }

    h2 {
        text-align: center;
    }

    h3 {
        text-align: center;
    }

    /* Center normal text */
    .center-text {
        text-align: center;
    }

    /* Make buttons full width */
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }

    /* Make dataframe fit nicely */
    .stDataFrame {
        width: 100%;
    }

</style>
""", unsafe_allow_html=True)



# SERVICE PRICES
SERVICES = {
    "Oil Change": 80.00,
    "Brake Service": 150.00,
    "Engine Check": 120.00,
    "Air Conditioning": 100.00,
    "Tyre Service": 200.00,
    "Full Service": 300.00
}


# FUNCTION 1
# REGISTER CUSTOMER AND VEHICLE
def register_customer_vehicle(
    name,
    phone,
    plate,
    model,
    vehicle_type,
    is_premium,
    membership
):

    if not name.strip():
        raise ValueError("Please enter customer name.")

    if not phone.strip():
        raise ValueError("Please enter phone number.")
    
    if not phone.isdigit():
        raise ValueError("Phone number must contain digits only.")

    if len(phone) < 10 or len(phone) > 11:
        raise ValueError("Phone number must be 10 or 11 digits.")
    
    if not plate.strip():
        raise ValueError("Please enter plate number.")

    if len(plate.strip()) < 3:
        raise ValueError("Invalid plate number.")

    if not model.strip():
        raise ValueError("Please enter vehicle model.")

    if is_premium:

        return PremiumVehicle(
            name,
            phone,
            plate,
            model,
            vehicle_type,
            membership
        )

    return Vehicle(
        name,
        phone,
        plate,
        model,
        vehicle_type
    )


# FUNCTION 2
# CALCULATE SERVICE CHARGE
def calculate_service_charge(
    selected_services,
    discount_rate=0.0
):

    subtotal = sum(
        SERVICES[service]
        for service in selected_services
    )

    discount = subtotal * discount_rate

    total = subtotal - discount

    return subtotal, discount, total


# FUNCTION 3
# DISPLAY INFORMATION
def display_information(
    vehicle,
    selected_services,
    discount,
    total
):

    st.header("📋 Service Information")

    # CUSTOMER & VEHICLE INFORMATION
    info = vehicle.get_info()

    if isinstance(vehicle, PremiumVehicle):

        _, benefit = vehicle.premium_benefit()

        info["Membership"] = vehicle.membership
        info["Premium Benefit"] = benefit

    info_df = pd.DataFrame(
        list(info.items()),
        columns=["Information", "Details"]
    )

    st.dataframe(
        info_df,
        use_container_width=True,
        hide_index=True
    )

    # MAGIC METHOD
    st.write(
        f"**Vehicle Summary (`__str__`):** "
        f"`{str(vehicle)}`"
    )

    # SELECTED SERVICES
    st.subheader("🔧 Selected Services")

    service_data = []

    for service in selected_services:

        service_data.append({
            "Service": service,
            "Charge (RM)": f"{SERVICES[service]:.2f}"
        })

    if discount > 0:

        service_data.append({
            "Service": "Premium Discount",
            "Charge (RM)": f"-{discount:.2f}"
        })

    service_data.append({
        "Service": "TOTAL",
        "Charge (RM)": f"{total:.2f}"
    })

    service_df = pd.DataFrame(service_data)

    st.dataframe(
        service_df,
        use_container_width=True,
        hide_index=True
    )


# HEADER
st.title("🚗 AutoCare Service Centre")

st.markdown(
    """
    <div class="center-text">
        <b>Smart Car Service Centre Management and Analysis System</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Welcome to AutoCare Service Centre. "
    "Enter customer and vehicle information, "
    "select the required services, and calculate "
    "the total service charge."
)


st.header("👤 Customer Information")

name = st.text_input(
    "Customer Name",
    placeholder="e.g. Ahmad"
)

phone = st.text_input(
    "Phone Number",
    placeholder="e.g. 0123456789"
)


st.header("🚗 Vehicle Information")

plate = st.text_input(
    "Plate Number",
    placeholder="e.g. P1234A"
)

model = st.text_input(
    "Vehicle Model",
    placeholder="e.g. Perodua Myvi"
)

vehicle_type = st.selectbox(
    "Vehicle Type",
    [
        "Car",
        "SUV",
        "MPV"
    ]
)


st.header("⭐ Membership")

is_premium = st.checkbox(
    "Customer is a Premium Member"
)

membership = "Standard"

if is_premium:

    membership = st.selectbox(
        "Membership Level",
        [
            "Gold",
            "Platinum"
        ]
    )


st.header("🔧 Service Selection")

selected_services = st.multiselect(
    "Choose one or more services:",
    list(SERVICES.keys())
)


if selected_services:

    st.subheader("💰 Service Price Preview")

    for service in selected_services:

        st.write(
            f"• **{service}** — "
            f"RM {SERVICES[service]:.2f}"
        )

    preview_total = sum(
        SERVICES[service]
        for service in selected_services
    )

    st.info(
        f"Estimated Service Charge: "
        f"RM {preview_total:.2f}"
    )


# PROCESS BUTTON
st.divider()

process_button = st.button(
    "🚗 Process Service",
    use_container_width=True
)


# PROCESS SYSTEM
if process_button:

    try:

        # FUNCTION 1
        vehicle = register_customer_vehicle(
            name,
            phone,
            plate,
            model,
            vehicle_type,
            is_premium,
            membership
        )

        if not selected_services:

            raise ValueError(
                "Please select at least one service."
            )

        discount_rate = 0.0

        if isinstance(
            vehicle,
            PremiumVehicle
        ):

            discount_rate, _ = (
                vehicle.premium_benefit()
            )

        # FUNCTION 2
        subtotal, discount, total = (
            calculate_service_charge(
                selected_services,
                discount_rate
            )
        )

        # FUNCTION 3
        display_information(
            vehicle,
            selected_services,
            discount,
            total
        )

        st.divider()

        st.header("🧾 Service Invoice")

        st.write(
            f"**Subtotal:** RM {subtotal:.2f}"
        )

        st.write(
            f"**Discount:** RM {discount:.2f}"
        )

        st.success(
            f"### Final Total: RM {total:.2f}"
        )

        # PREMIUM INFORMATION
        if is_premium:

            _, benefit = vehicle.premium_benefit()

            st.info(
                f"⭐ Premium Benefit: {benefit}"
            )

        # OOP DEMONSTRATION
        st.divider()

        st.header("💻 OOP Demonstration")

        # Magic Method
        st.subheader("Magic Method `__str__()`")

        st.code(
            str(vehicle)
        )

        # Function Overloading
        st.subheader("Function Overloading")

        st.write(
            vehicle.service_summary()
        )

        st.write(
            vehicle.service_summary(
                selected_services[0]
            )
        )

        # OPERATOR OVERLOADING
        st.subheader(
            "🔗 Operator Overloading `__add__()`"
        )

        second_vehicle = Vehicle(
            "Demo Customer",
            "0100000000",
            "ABC1234",
            "Honda Civic",
            "Car"
        )

        combined = vehicle + second_vehicle

        st.write(
            f"**Output:** `{combined}`"
        )

    # EXCEPTION HANDLING
    except ValueError as error:

        st.error(
            f"⚠️ {error}"
        )

    except Exception as error:

        st.error(
            f"❌ Unexpected error: {error}"
        )


# DATA ANALYSIS
st.divider()

st.header("📊 Vehicle Service Data Analysis")

st.write(
    "Data analysis using NumPy, Pandas and Matplotlib"
)


# DATAFRAME
raw_data = {

    "Service_ID": [
        101, 102, 103, 104,
        105, 106, 107, 108
    ],

    "Vehicle_Model": [
        "Myvi",
        "Civic",
        "Saga",
        "HR-V",
        "Myvi",
        "Alza",
        "Civic",
        "City"
    ],

    "Service_Type": [
        "Oil Change",
        "Full Service",
        "Brake Service",
        "Engine Check",
        "Tyre Service",
        "Full Service",
        "Oil Change",
        "Brake Service"
    ],

    "Service_Charge_RM": [
        80,
        300,
        150,
        120,
        200,
        300,
        80,
        150
    ]
}


df = pd.DataFrame(raw_data)


st.subheader("1️⃣ Service Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# NUMPY ARRAY
charges = np.array(
    df["Service_Charge_RM"]
)


st.subheader("2️⃣ NumPy Analysis")

st.write(
    f"**Total Revenue:** "
    f"RM {np.sum(charges):.2f}"
)

st.write(
    f"**Average Charge:** "
    f"RM {np.mean(charges):.2f}"
)

st.write(
    f"**Maximum Charge:** "
    f"RM {np.max(charges):.2f}"
)


# ARRAY ATTRIBUTES
with st.expander(
    "🔍 View NumPy Array Attributes"
):

    st.write(
        f"**Array:** {charges}"
    )

    st.write(
        f"**Shape:** {charges.shape}"
    )

    st.write(
        f"**Data Type:** {charges.dtype}"
    )

    st.write(
        f"**Dimensions:** {charges.ndim}"
    )

    st.write(
        f"**First 3 values (Slicing [0:3]):** "
        f"{charges[0:3]}"
    )

    st.write(
        f"**Last value (Indexing [-1]):** "
        f"{charges[-1]}"
    )


# FILTER AND SORT
st.subheader("3️⃣ Filter & Sort")

minimum_price = st.slider(
    "Show services above RM:",
    50,
    300,
    100
)

filtered_df = (
    df[
        df["Service_Charge_RM"] > minimum_price
    ]
    .sort_values(
        "Service_Charge_RM",
        ascending=False
    )
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# MATPLOTLIB
st.subheader("4️⃣ Service Revenue Graph")

grouped = (
    df.groupby("Service_Type")
    ["Service_Charge_RM"]
    .sum()
)

fig, ax = plt.subplots(
    figsize=(9, 4)
)

ax.bar(
    grouped.index,
    grouped.values
)

ax.set_title(
    "Total Revenue by Service Type"
)

ax.set_xlabel(
    "Service Type"
)

ax.set_ylabel(
    "Revenue (RM)"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

st.pyplot(fig)