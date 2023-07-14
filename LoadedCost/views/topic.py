from decimal import Decimal

# Treat single employee and multiple employee use cases as the same thing
# A project may have one or more employees

class Project:
    def __init__(self):
        self.employee_list = []

########################################################################################################

    # employee_dict like {employee: e, hours: h, rate: r, extra_time: t}
    def add_employee(self, employee_dict):
        self.employee_list.append(employee_dict)

########################################################################################################

    def get_resulting_margin(self, project_rate, cost):
        if cost is None or project_rate is None or project_rate == 0:
            return 0
        return round(1 - (Decimal(cost) / Decimal(project_rate)), 2)

########################################################################################################

    def is_profitable(self, target_margin, resulting_margin):
        if len(self.employee_list) == 0:
            raise("No employees added to project")
        elif len(self.employee_list) == 1 or len(self.employee_list) > 1:
            try: 
                # Logic for single employee use case
                if target_margin is not None and resulting_margin is not None:
                    if Decimal(resulting_margin) < 0:
                        return('Margin is Negative!')
                    elif Decimal(target_margin) > Decimal(resulting_margin) + Decimal(2):
                        return ('Seek Approval! Margin is low at this rate.')
                    elif Decimal(target_margin) <= Decimal(resulting_margin) + Decimal(2) and Decimal(target_margin) >= Decimal(resulting_margin) - Decimal(2):
                        return('Caution! Margin close to target (+/- 2%).')
                    else:
                        return('Good! Margin better than target.')
            except: 
                return 'Invalid Margin Values'


###############################################################################################################################

    def get_weekly_revenue(self, employee_list):
        rate = []
        hours = []
        for employee in employee_list:
            if employee['rate'] is not None and employee['hours'] is not None:
                rate.append(employee['rate'])
                hours.append(employee['hours'])
        rate_sum = sum(rate)
        hours_sum = sum(hours)
        revenue = rate_sum * hours_sum
        return revenue


###############################################################################################################################

    def get_weekly_cost(self, employee_list, hourly_rate):
        employee_weekly_cost = None

        if len(employee_list) > 1:
            for employee in employee_list: 
                if employee['extra_time'] == 'busy' or employee['extra_time'] == 'contractor':
                    if employee['hours'] is not None and hourly_rate is not None:
                        employee_weekly_cost = hourly_rate * employee['hours']
                elif employee['extra_time'] == 'idle':
                    if hourly_rate is not None:
                        employee_weekly_cost = 40 * hourly_rate
                elif employee['extra_time'] == 'partial':
                    if employee['hours'] is not None and hourly_rate is not None:
                        idle_time = 40 - employee['hours']
                        partial_time = (idle_time / 2) + employee['hours']
                        employee_weekly_cost = partial_time * hourly_rate
                elif employee['extra_time'] is None or employee['extra_time'] == 'N/A': 
                    return

        if employee_weekly_cost is None: 
            return 0 
        else:
            return employee_weekly_cost

###############################################################################################################################