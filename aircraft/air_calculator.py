import streamlit as st
import pandas as pd

#logo
st.sidebar.image("data/logo1.png", caption="Aircraft Cost")

countries = [
    "United States",
    "Canada",
    "United Kingdom  ",
    "Germany",
    "Nigeria",
    "France",
    "Japan",
    "Australia",
    "China",
    "India",
    "Brazil",
    "South Africa",
]

# Create two columns, with 3/4 and 1/4 of the width
col1, col2 = st.columns([3, 1])

# Position the dropdown in the second column (col2) at the top right corner
with col2:
    selected_country = st.selectbox(" ", countries)

# Display the selected country in the first column (col1)
with col1:
    st.write(" ", selected_country)

# Function to calculate total hours
def calculate_total_hours(owner_hours, charter_hours):
    total_hours = owner_hours + charter_hours
    return total_hours

# Function to calculate fuel cost
def calculate_fuel_cost(total_hours, fuel_cost_per_gallon, fuel_consumption_rate):
    fuel_cost = (total_hours * fuel_consumption_rate) * fuel_cost_per_gallon
    return fuel_cost

# Function to loan schedule
def calculate_loan_schedule(loan_amount, annual_interest_rate, loan_term_months, monthly_lease=0.00, period_number=0):
    monthly_interest_rate = annual_interest_rate / 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)
    interest_first_period = loan_amount * monthly_interest_rate
    principal_first_period = monthly_payment - interest_first_period
    return monthly_payment + monthly_lease, principal_first_period, interest_first_period, period_number

def calculate_owner_hourly(fuel_usage_per_hour, fuel_cost_per_gallon, airframe_maintenance, engine_apu_maintenance):
    
    fuel_cost_per_hour = fuel_usage_per_hour * fuel_cost_per_gallon

    # Calculate Total Maintenance Cost
    total_maintenance_cost = airframe_maintenance + engine_apu_maintenance
    return fuel_cost_per_hour, total_maintenance_cost

# Function to calculate monthly budget from annual budget
def calculate_monthly_budget(annual_budget):
    return annual_budget / 12

# Calculate the annual budget with charter
def calculate_annual_budgets(total_hourly_cost_with_charter, annual_owner_hours):
    annual_budget_with_charter = total_hourly_cost_with_charter * annual_owner_hours
    return annual_budget_with_charter

# Function to calculate the annual costs
def calculate_annual_costs(Fuel_Cost_Per_Gallon, Total_hrs, fuel_usage, airframe_maintenance, engine_apu_maintenance, Crew_Misc):
    Annual_Fuel_Gallons = Total_hrs * fuel_usage
    Annual_Fuel_cost = Annual_Fuel_Gallons * Fuel_Cost_Per_Gallon
    Annual_airframe_maintenance = Total_hrs * airframe_maintenance
    Annual_engine_apu_maintenance = Total_hrs * engine_apu_maintenance
    Annual_Crew_Misc = Total_hrs * Crew_Misc
    Total_Variable_cost = Annual_Fuel_cost + Annual_airframe_maintenance + Annual_engine_apu_maintenance + Annual_Crew_Misc
    return Annual_Fuel_Gallons, Annual_Fuel_cost, Annual_airframe_maintenance, Annual_engine_apu_maintenance, Annual_Crew_Misc, Total_Variable_cost

# Function to format numbers with commas
def format_number(number):
    return "{:,.2f}".format(number)

# Streamlit UI
st.title("_Aircraft Cost Calculator_")
st.divider()

# Define the set_bg_hack_url function
def set_bg_hack_url():
    # Set the background image and sidebar styling

    st.markdown(
        """
        <style>
        .stApp {
            background: url("https://wallpaperset.com/w/full/1/9/7/183261.jpg");
            background-size: cover;
            background-repeat: no-repeat;
        }

        [data-testid=stSidebar] {
            background-color: #87666d;
            font-family: sans-serif;
            background-color: transparent;
        }
        
        div.css-1r6slb0.metric_card_class{
            padding: 5% 5% 5% 10%,
            
        }
        
        .card_style {
            border: 2px solid #000;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            text-align: center;
        }
        @media (max-width: 768px){
            .container{
                flex-direction:column
            }
        }
        .metric{
            font-family: italic;
            font-weight: bold
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
# Call the function to set the background
set_bg_hack_url()


style = """
<style>
    .with-border {
        border: 5px solid #87666d; /* You can adjust the border width and color */
        border-radius: 7px; /* You can adjust the border radius for rounded corners */
        padding: 5px; /* You can adjust the padding for spacing inside the element */
        background-color: #87666d;
        opacity: ;
        box-shadow: inset 0 -3em 3em rgba(0, 0, 0, 0.1),
            0 0 0 2px rgb(255, 255, 255),
            0.3em 0.3em 1em rgba(0, 0, 0, 0.3);  
        font-family: sans-serif;
        padding: 5% 5% 5% 10%;
        opacity: 0.6;
    
            
        
    }
    .with-border:hover{
        transform: scale(1.5);
        opacity: none;
        
    }
    
    .with-data{
        background-color: #87666d;
    }
</style>
"""
 # Display the CSS style
st.markdown(style, unsafe_allow_html=True)


# Sidebar for selecting a calculation
selected_calculation = st.sidebar.selectbox("Select a Calculation", ["Watch Video","Payment Schedule", "General Parameters", "Owner Hourly cost", "Annual Budget", "Per Month", "Annual Variable Cost"])

if selected_calculation == "Watch Video":
    
    st.sidebar.header("Watch Video", divider='rainbow')
    # Replace 'video_bytes' with the actual video file or URL you want to display
    #st.video("https://mixkit.co/free-stock-video/airplane/")
    #video_file = open('star.mp4', 'rb')
    #video_bytes = video_file.read()
    #st.video(video_bytes)

    
# Input fields for loan schedule
elif selected_calculation == "Payment Schedule":
    st.sidebar.header("Calculator Metrics Input ⌨", divider='rainbow')
    

    loan_amount = st.sidebar.number_input("Loan Amount (in dollars)", value=200000)
    annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", value=4.0)
    loan_term_months = st.sidebar.number_input("Loan Term (in months)", value=120)
    monthly_lease = st.sidebar.number_input("Monthly Lease Amount (if any)", value=0.0)
    period_number = st.sidebar.number_input("Annual Owner Flight Hours", value=150)
    period_number = st.sidebar.number_input("Annual Charter Flight Hours", value=0)
    period_number = st.sidebar.number_input("Fuel Cost per Gallon (in dollars)", value=4.25)
    period_number = st.sidebar.number_input("Fuel Consumption Rate (gallons per hour)", value=10)

    # Calculate loan schedule
    if st.sidebar.button("Calculate payment Schedule"):
        monthly_payment, principal_first_period, interest_first_period, period_number = calculate_loan_schedule(
            loan_amount, annual_interest_rate / 100, loan_term_months, monthly_lease, period_number
        )

        # Display results in columns with metric cards
        
        col1, col2, col3 = st.columns(3)
        
        # Define CSS class for metric cards
        metric_card_class = 'css-1r6slb0'


        # Add metric cards with inline styling to make text bold
        #col1.metric("**Monthly Payment**", format_number(monthly_payment), "USD")
        
        col1.markdown(f'<div class="with-border">' +
                      '<h5>Monthly Payment </h5>' +
                      f'<h2>{format_number(monthly_payment)}</h2>'+ "USD" +
                      
                      '</div>', unsafe_allow_html=True)
        #col2.metric("**Principal for the first period**",format_number(principal_first_period), "USD")
        
        col2.markdown(f'<div class="with-border">' +
                      '<h5>Principal Amount</h5>' +
                      f'<h2>{format_number(principal_first_period)}</h2>'+ "USD" +
                      
                      '</div>', unsafe_allow_html=True)
        #col3.metric("**Interest for the first period**", format_number(interest_first_period), "USD")
        
        col3.markdown(f'<div class="with-border">' +
                      '<h5>Interest Amount</h5>' +
                      f'<h2>{format_number(interest_first_period)}</h2>'+ "USD" +
                      
                      '</div>', unsafe_allow_html=True)
        
    

# Input fields for General parameters calculation
if selected_calculation == "General Parameters":
    st.sidebar.header("General Parameters ✈️", divider='rainbow')

    
    

    annual_owner_hours = st.sidebar.number_input("Annual Owner Flight Hours", value=150)
    annual_charter_hours = st.sidebar.number_input("Annual Charter Flight Hours", value=0)
    fuel_cost_per_gallon = st.sidebar.number_input("Fuel Cost per Gallon (in dollars)", value=4.25)
    fuel_consumption_rate = st.sidebar.number_input("Fuel Consumption Rate (gallons per hour)", value=10)

    # Calculate the total flight hours for aircraft ownership
    total_flight_hours = calculate_total_hours(annual_owner_hours, annual_charter_hours)

    # Calculate the fuel cost based on the total flight hours and fuel parameters
    total_fuel_cost = calculate_fuel_cost(total_flight_hours, fuel_cost_per_gallon, fuel_consumption_rate)

    # Display the results in columns with metric cards
    col1, col2 = st.columns(2)
    
    # Define CSS class for metric cards
    metric_card_class = 'css-1r6slb0'

    # Add metric cards with inline styling to make text bold
    #col1.metric("Total Flight Hours for Ownership", total_flight_hours)
    
    col1.markdown(f'<div class="with-border">' +
                      '<h5>Total Flight Hours</h5>' +
                      f'<h2>{format_number(total_flight_hours)}</h2>'+ "Hrs" +
                      
                      '</div>', unsafe_allow_html=True)
    #col2.metric("Total Fuel Cost", format_number(total_fuel_cost), "USD")
    
    col2.markdown(f'<div class="with-border">' +
                      '<h5>Total Fuel Cost</h5>' +
                      f'<h2>{format_number(total_fuel_cost)}</h2>'+ "USD" +
                      
                      '</div>', unsafe_allow_html=True)
 # Input fields for General parameters calculation   

# Sidebar inputs
elif selected_calculation == "Owner Hourly cost":
    
    fuel_usage_per_hour = st.sidebar.number_input("Fuel Usage per Hour (gallons)", value=18.90)
    fuel_cost_per_gallon = st.sidebar.number_input("Fuel Cost per Gallon ($)", value=4.25)
    airframe_maintenance = st.sidebar.number_input("Airframe Maintenance Cost ($)", value=33.15)
    engine_apu_maintenance = st.sidebar.number_input("Engine/APU Maintenance Cost ($)", value=33.13)
    crew_costs = st.sidebar.number_input("Crew Costs ($)", value=5.00)
    total_fixed_cost_without_charter = st.sidebar.number_input("Total Fixed Cost without Charter ($)", value=557.04)
    total_fixed_cost_with_charter = st.sidebar.number_input("Total Fixed Cost with Charter ($)", value=557.04)

    # Calculate metrics
    fuel_cost_per_hour = fuel_usage_per_hour * fuel_cost_per_gallon
    total_maintenance_cost = airframe_maintenance + engine_apu_maintenance
    total_variable_cost_per_hour = fuel_cost_per_hour + total_maintenance_cost + crew_costs
    total_hourly_cost_without_charter = total_variable_cost_per_hour + total_fixed_cost_without_charter
    total_hourly_cost_with_charter = total_variable_cost_per_hour + total_fixed_cost_with_charter

    # Create a dictionary with the metrics
    data = {
        "Metric Name": [
            "Fuel Cost per Hour",
            "Total Maintenance Cost",
            "Total Variable Cost per Hour",
            "Total Hourly Cost without Charter",
            "Total Hourly Cost with Charter",
            "Total Fixed Cost with Charter",
            "Total Fixed Cost without Charter",
        ],
        "Formatted Value": [
            f"${fuel_cost_per_hour:.2f} USD",
            f"${total_maintenance_cost:.2f} USD",
            f"${total_variable_cost_per_hour:.2f} USD",
            f"${total_hourly_cost_without_charter:.2f} USD",
            f"${total_hourly_cost_with_charter:.2f} USD",
            f"${total_fixed_cost_with_charter:.2f} USD",
            f"${total_fixed_cost_without_charter:.2f} USD",
        ],
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Display the DataFrame
    st.dataframe(df, hide_index=True)
     
elif selected_calculation == "Annual Budget":
    st.sidebar.header("Annual Budget✈️")
    
    # Input for total_hourly_cost_with_charter in the sidebar
    total_hourly_cost_with_charter = st.sidebar.number_input(
        "Total Hourly Cost with Charter ($):", min_value=708.0
    )

    # Input for annual_owner_hours in the sidebar
    annual_owner_hours = st.sidebar.number_input(
        "Annual Owner Hours:", min_value=150
    )

    # Calculate the annual budgets using the function
    annual_budget_with_charter = calculate_annual_budgets(
        total_hourly_cost_with_charter, annual_owner_hours)

    # Display the results in columns with metric cards
    col1, col2 = st.columns(2)
    
    # Add the "with-border" class to apply the styling
    col1.markdown(
        f'<div class="with-border">' +
        f'<h5>Annual Owned Hours</h5>' +
        f'<h2>{format_number(annual_owner_hours)}</h2>' + "Hrs" +
        '</div>',
        unsafe_allow_html=True
    )
    
    col2.markdown(
        f'<div class="with-border">' +
        f'<h5>Annual Budget</h5>' +
        f'<h2>{format_number(annual_budget_with_charter)}</h2>' + "USD" +
        '</div>',
        unsafe_allow_html=True
    )
        
# Check which calculation is selected
elif selected_calculation == "Per Month":
    st.sidebar.header("Per Month ✈️", divider='rainbow')
    
    # Input field for annual budget
    annual_budget = st.sidebar.number_input("Enter Annual Budget", value=106297.49)
    monthly_hours = st.sidebar.number_input("Enter Monthly Hours", value=13)
    
    
    if st.sidebar.button("Calculate Per Month"):
        
        monthly_budget = calculate_monthly_budget(annual_budget)
    
        # Display the results in columns with metric cards
        col1, col2 = st.columns(2)
    
        # Define CSS class for metric cards
        metric_card_class = 'css-1r6slb0'

        # Add metric cards with inline styling to make text bold
        #col1.metric("Monthly_Hours", format_number(monthly_hours), "Hrs")
    
        col1.markdown(f'<div class="with-border">' +
                      '<h5>Monthly_Hours</h5>' +
                      f'<h2>{format_number(monthly_hours)}</h2>'+ "Hrs" +
                      
                      '</div>', unsafe_allow_html=True)
    
        #col2.metric("Monthly Budget", format_number(monthly_budget), "USD")
    
        col2.markdown(f'<div class="with-border">' +
                      '<h5>Monthly Budget</h5>' +
                      f'<h2>{format_number(monthly_budget)}</h2>'+ "USD" +
                      
                      '</div>', unsafe_allow_html=True)
    
# Check which calculation is selected
elif selected_calculation == "Annual Variable Cost":
    st.sidebar.header("Annual Variable Cost✈️", divider='rainbow')
    
    Fuel_Cost_Per_Gallon = st.sidebar.number_input("Fuel Cost Per Gallon", value=4.25)
    Total_hrs = st.sidebar.number_input("Total Hours", value=150)
    fuel_usage = st.sidebar.number_input("Fuel Usage (Gallons per Hour)", value=18.90)
    fuel_cost_per_hour = Fuel_Cost_Per_Gallon * fuel_usage
    airframe_maintenance = st.sidebar.number_input("Airframe Maintenance Cost Per Hour", value=33.15)
    engine_apu_maintenance = st.sidebar.number_input("Engine & APU Maintenance Cost Per Hour", value=33.13)
    Crew_Misc = st.sidebar.number_input("Crew Miscellaneous Cost Per Hour", value=5)
    
    if st.sidebar.button("Calculate Annual Variable Cost"):
        
        Annual_Fuel_Gallons, Annual_Fuel_cost, Annual_airframe_maintenance, Annual_engine_apu_maintenance, Annual_Crew_Misc, Total_Variable_cost = calculate_annual_costs(
        Fuel_Cost_Per_Gallon, Total_hrs, fuel_usage, airframe_maintenance, engine_apu_maintenance, Crew_Misc
    )
        
        # Create a dictionary with the metrics
        data = {
            "Metric Name": [
                "Annual Fuel Gallons",
                "Annual Fuel Cost",
                "Annual Airframe Maintenance Cost Cost",
                "Annual Engine & APU Maintenance Cost",
                "Annual Crew Miscellaneous Cost",
                "Total Variable Cost",
                
            ],
            "Formatted Value": [
                f"${Annual_Fuel_Gallons:.2f} USD",
                f"${Annual_Fuel_cost:.2f} USD",
                f"${Annual_airframe_maintenance:.2f} USD",
                f"${Annual_engine_apu_maintenance:.2f} USD",
                f"${Annual_Crew_Misc:.2f} USD",
                f"${Total_Variable_cost:.2f} USD",
                
            ],
        }

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(data)

        # Display the DataFrame
        st.dataframe(df, hide_index=True)
    
    
    

  
    
    
    


