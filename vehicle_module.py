
# Parent Class
class Vehicle:

    # Magic Method: __init__
    def __init__(self, customer_name, phone, plate_number,
                 model, vehicle_type="Car"):

        self.customer_name = customer_name
        self.phone = phone
        self.plate_number = plate_number
        self.model = model
        self.vehicle_type = vehicle_type

    # Magic Method: __str__
    def __str__(self):
        return f"{self.model} ({self.plate_number})"

    # Operator Overloading
    def __add__(self, other):
        return f"{self.model} & {other.model}"

    # Vehicle information
    def get_info(self):
        return {
            "Customer Name": self.customer_name,
            "Phone Number": self.phone,
            "Plate Number": self.plate_number,
            "Vehicle Model": self.model,
            "Vehicle Type": self.vehicle_type
        }

    # Function Overloading using default parameter
    def service_summary(self, service="General Service"):
        return f"{self.model} requires {service}"


# Child Class
class PremiumVehicle(Vehicle):

    # Magic Method: __init__
    def __init__(self, customer_name, phone, plate_number,
                 model, vehicle_type="Car", membership="Gold"):

        super().__init__(
            customer_name,
            phone,
            plate_number,
            model,
            vehicle_type
        )

        self.membership = membership

    # Premium benefit
    def premium_benefit(self):

        if self.membership == "Platinum":
            discount_rate = 0.15
        else:
            discount_rate = 0.10

        benefit = (
            f"{self.membership} Member - "
            f"{int(discount_rate * 100)}% Discount"
        )

        return discount_rate, benefit