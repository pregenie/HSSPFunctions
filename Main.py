#######################################################################################################################
# This module is used to calculate all fuel abatement required values that are more easily calculated using a module
# than a query. These values are specifically any values that require financial or more complex array calculations that
# are better handled because of ease of use and performance in the module.  Any values requiring multiple calculations
# based on the number of years in service, number of years for financing or time based functions are also calculated
# here.  References to the spreadsheet are provided as direction and may change based on versions (they will not be
# maintained)
#######################################################################################################################
__author__ = 'pregenie'
import numpy as np

# this area is for single value input variables which will come from the web interface and be passed through a
# json string


# SOLAR DATA
solar_DCAC_ratio = 1.3                          # Hybrid System Design!B4
solar_harvest_130_DCAC_ratio = 1614.00          # Hybrid System Design!B5
solar_harvest_degradation_1st_yr = .015         # Hybrid System Design!B6
solar_harvest_degradation_afterwards = .005     # Hybrid System Design!B7
solar_hours_in_a_day = 8.0                      # Hybrid System Design!B8
solar_capitalized_cost = 2.70000000             # Hybrid System Design!B9
Solar_OPEX_cost = .012                          # Hybrid System Design!B10
solar_system_upsizing = 0.0                     # Hybrid System Design!B11

# LOAD DATA
peak_load_power	= 12.0                          # Hybrid System Design!F4
load_energy_use = 84.6                          # Hybrid System Design!F5
daily_load_requirement = 213.4                  # Hybrid System Design!F6
largest_load_block_to_switch_on = .20           # Hybrid System Design!F7
starting_torque_at_load_switching = 2.5         # Hybrid System Design!F8
yearly_load_growth = 0.0                        # Hybrid System Design!F9

# BATTERY DATA
battery_selection =	8                           # Hybrid System Design!B14
battery_type = 'LG-Chem'                        # Hybrid System Design!B15
battery_PE_ratio =	0.500                       # Hybrid System Design!B16
battery_energy_storage_cost = 1000.000          # Hybrid System Design!B17
battery_invertercharger_cost =	200.000         # Hybrid System Design!B18
battery_OM_cost = .02                           # Hybrid System Design!B19
battery_replacement_cost_reduction = .05        # Hybrid System Design!B20
battery_cost_reduction_period =	10              # Hybrid System Design!B21
battery_lifetime = 3600                         # Hybrid System Design!B22
depth_of_discharge = .995                       # Hybrid System Design!B23
capacity_degradation_factor =	.022            # Hybrid System Design!B24
battery_round_trip_ACAC_efficiency = .85        # Hybrid System Design!B25
battery_converter_ACDC_efficiency = .97         # Hybrid System Design!B26
battery_inverter_DCAC_efficiency = .97          # Hybrid System Design!B27
battery_DCDC_efficiency = .90                   # Hybrid System Design!B28
battery_energy_upsizing	= 0.0                   # Hybrid System Design!B29

# ECONOMIC DATA
wacc = 0.075                                    # Hybrid System Design!B38
inflation_rate = .03                            # Hybrid System Design!B39
ppa_term = 18                                   # Hybrid System Design!B40
PPA_price_escalation_rate = .03                 # Hybrid System Design!B41
depreciation_for_tax_purposes_solar = 7         # Hybrid System Design!B42
depreciation_for_tax_purposes_storage =	5       # Hybrid System Design!B43
depreciation_for_tax_purposes_gen = 2           # Hybrid System Design!B44
SPV_income_tax_rate = .35                       # Hybrid System Design!B45

# SYSTEM SIZING
battery_full_cycles_per_day	= 1                 # Hybrid System Design!B49
included_solar_to_meet_battery_losses = 0.0     # Hybrid System Design!B54
battery_system_size_power = 0.00                # Hybrid System Design!B56
battery_system_size_energy = 0.00               # Hybrid System Design!B57
fossil_generator_size =	14.40                   # Hybrid System Design!B58
fossil_generator_fuel_usage = 9.68              # Hybrid System Design!B59

# FOSSIL GENERATOR
generation_selection = 1                            # Hybrid System Design!F14
generation_type = 'Combustion Engine - High Speed'  # Hybrid System Design!F15
fossil_capital_cost = 750                                  # Hybrid System Design!F16
fossil_fixed_OM = 45                                       # Hybrid System Design!F17
fossil_variable_OM = 18.75                                 # Hybrid System Design!F18
fixed_and_additional_OPEX_cost = .06
average_efficiency = .352
fuel_selection = 4
fuel_type = 'Diesel'
fuel_measurement_unit = 'US Gal'
fuel_heat_value	= 0.135
fuel_cost = 4.625
fuel_cost_escalation = .03
min_generator_size_for_reliability = 1.20       # Hybrid System Design!F27
number_of_generators = 10                       # Hybrid System Design!F28
minimum_gen_loading	= .20                       # Hybrid System Design!F29
unit_availability = .80
plant_availability = .975
generator_max_capacity_factor = 1.0
generator_lifetime = 18000
generator_refurbishments= 2
refurbishment_cost = 375

LCOE_escalation_factor = 1.1435734517

discount_factor = (1+wacc)**0.5                 # Hybrid System Design!
print 'discount factor:', discount_factor

# solar costs calculated

# fossil
fossil_fuel_energy_blend = .70                  # Hybrid System Design!F38

########################################################################################################################
# this area will be for all calculations not requiring a loop and separated by their perspective use
########################################################################################################################

# CALCULATED FIELD: min_gen_energy
# Hybrid System Design!B50 =F29*F27*F4*B8/F28
min_gen_energy = minimum_gen_loading*min_generator_size_for_reliability*peak_load_power*solar_hours_in_a_day/number_of_generators
print 'min gen energy:', min_gen_energy

# CALCULATED FIELD: excess_solar_energy_stored
# Hybrid System Design!B51 =IF((F6*(1-F38))>(F5-B50), F6*(1-F38)-(F5-B50), 0)
if(daily_load_requirement*(1-fossil_fuel_energy_blend) > (load_energy_use-min_gen_energy)):
    excess_solar_energy_stored = daily_load_requirement*(1-fossil_fuel_energy_blend) - (load_energy_use-min_gen_energy)
else:
    excess_solar_energy_stored = 0
print 'excess_solar_energy_stored:', excess_solar_energy_stored

# CALCULATED FIELD: min_solar_system_size
# Hybrid System Design!B52 =IF(B51>0, B51/B25+F5-B50, F6*(1-F38)) / (B5/365)
if(excess_solar_energy_stored > 0):
    min_solar_system_size =((excess_solar_energy_stored/battery_round_trip_ACAC_efficiency)+(load_energy_use-min_gen_energy)) / (solar_harvest_130_DCAC_ratio/365.00)
else:
    min_solar_system_size = daily_load_requirement*(1-fossil_fuel_energy_blend) / (solar_harvest_130_DCAC_ratio/365.00)

print 'min solar system size:', min_solar_system_size

# CALCULATED FIELD: solar_system_size
# Hybrid System Design!B53 =B52*(1+B11)+0.000001
solar_system_size = min_solar_system_size*(1+solar_system_upsizing)+0.000001
print 'solar size:', solar_system_size

# CALCULATED FIELD: solar_system_capital_costs
# Hybrid System Design!B83 =$B$53*$B$9
solar_system_capital_costs = solar_system_size*solar_capitalized_cost

# capital_costs: [solar, battery, fossil], o_and_m: [solar, battery, fossil, fuel: [solar, battery, fossil]
costs = np.array([(63.30712547, 52.94, 11.50),
                         (12.34, 9.09, 17.36),
                         (0, 0, 168.06)],
                         dtype=[('solar','float'),('battery','float'),('fossil','float') ])

# The eventual extent of this function will be to calculate all values requiring calculation within
# the PPA year loop and return an array of values

# load, Hybrid System Design!B98:AA98 =SUMPRODUCT(B98:AA98,B69:AA69)
# solar_system_capital_costs, Hybrid System Design!B83:AA83 =IF(C68<=$B$42,-$B83/$B$42*$B$45,0)
# initial storage capital costs =($B$56*$B$18+$B$57*$B$17)/1000
# battery_capital_costs, Hybrid System Design!B91:AA91 =(IF(AND(D$88>0,D$88<=$B$43),-$B91/$B$43*$B$45,0)
# +IF(D$87<>C$87,($B$56*$B$18+$B$57*$B$17)/1000*(1-$B$20)^MIN(COUNTIF($C$87:$AA$87,C$87),$B$21),0)  )
#  *  IF(D68<>"",1,0)
#   break down of battery calculation logic
#       if there is a year (ignore this as we have a specific loop) and we are less than the depreciation years for
#       storage -$B91/$B$43*$B$45
#           the prior year's value divided by the depreciation years * the income tax rate for depreciation +
#           if there has been a battery replaced
#               (total battery costs) battery system size power * battery inverter charger cost + battery system size
#               energy * battery energy storage costs / 1000 (megawatt)  * (1 - battery replacement
#               cost reduction) to the power of (the number of years the battery has been in service or the battery
#               cost reduction period whichever is less)
#
# discount_factor, Hybrid System Design!B69:AA69 =IF(E68<>"",D69/(1+$B$38),0)
# total_energy_serving_load, Hybrid System Design!B69:AA69 =IF(D68<>"",$F$6*365*(1+$F$9)^(D68-1)/1000,0)
# capital_cost, =IF(C68<=$B$42,-$B83/$B$42*$B$45,0)
# solar LCOE, =C129/$C$144/B148
class LCOE:
    'Calculation class for the LCOE of solar, battery, fossil by capital, o&m, and fuel'

    'initialize variables for class'


    def __init__(self, term, factor, load_growth, daily_load, LCOE_escalation_factor, solar_system_size,
                 solar_capitalized_cost, battery_cost_reduction_period):
        self.term = term
        self.factor = factor
        self.load_growth = load_growth
        self.daily_load = daily_load
        self.serving = 0
        self.load = 0

        # solar variables
        self.solar_capital_cost = 0
        self.init_solar_capital_cost = 0
        self.solar_capital_costs = 0
        self.solar_capitalized_cost = solar_capitalized_cost
        self.solar_system_size = solar_system_size
        self.lcoe_escalation_factor = LCOE_escalation_factor

        # battery variables
        self.battery_cost_reduction_period = battery_cost_reduction_period
        self.battery_replacement_number = 0
        self.storage_capital_cost = 0
        self.init_storage_capital_cost = 0
        self.storage_capital_costs = 0


    def calculate_ppa_values(self):
        a = 0
        print 'inc', 'factor',' serving', 'load', 'solar_capital_cost', 'battery_replacement_number', 'storage_capital_cost', 'fossil_capital_cost'
        while a < self.term+1:
            if (a==0):
                factor = 1*(1+wacc)**0.5

                # solar calculations
                self.init_solar_capital_cost = self.solar_system_size*self.solar_capitalized_cost
                self.solar_capital_costs = self.factor*self.init_solar_capital_cost


                # battery calculations
                self.battery_replacement_number == 0
                self.init_storage_capital_cost = battery_system_size_power * battery_invertercharger_cost + battery_system_size_energy * battery_energy_storage_cost/1000
                self.storage_capital_costs = self.init_storage_capital_cost

                # fossil calculations
                self.init_fossil_capital_cost = fossil_generator_size*fossil_capital_cost/1000
                self.fossil_capital_cost = self.init_fossil_capital_cost

                print a, factor, self.serving, self.load, self.solar_capital_costs, self.battery_replacement_number, self.storage_capital_costs, self.fossil_capital_cost

            else:

                # solar calculations
                if (a <= depreciation_for_tax_purposes_solar):
                    self.solar_capital_cost = (-self.init_solar_capital_cost/depreciation_for_tax_purposes_solar)*SPV_income_tax_rate
                else:
                    self.solar_capital_cost = 0

                self.factor = self.factor/(1+wacc)
                self.solar_capital_costs = self.solar_capital_costs + (self.factor*self.solar_capital_cost)

                #battery calculations (need to be checked for completeness
                if (a % self.battery_cost_reduction_period == 0):
                    self.battery_replacement_number += 1

                if (a < depreciation_for_tax_purposes_storage):
                    self.storage_capital_cost = (-self.init_storage_capital_cost/depreciation_for_tax_purposes_storage)*SPV_income_tax_rate
                else:
                    self.storage_capital_cost = 0

                # general calculations
                self.serving = self.daily_load*365*(1+self.load_growth)**(a-1)/1000
                self.load += self.factor*self.serving

                # calculate the solar LCOE capital cost
                print a, self.factor, self.serving, self.load, self.solar_capital_costs, self.battery_replacement_number, self.storage_capital_costs
            a+=1
        solar_lcoe_capital = self.solar_capital_costs/self.load/self.lcoe_escalation_factor
        print 'Solar LCOE Capital:', solar_lcoe_capital


lcoe = LCOE(ppa_term, discount_factor, yearly_load_growth, daily_load_requirement, LCOE_escalation_factor,
            solar_system_size, solar_capitalized_cost, battery_cost_reduction_period)
lcoe.calculate_ppa_values()

print 'Calculated load:', lcoe.load
print 'Solar Capital Costs:', lcoe.solar_capital_costs

print 'Sum of Solar:', costs['solar'].sum()
print 'Sum of Solar Summed:', '0.0844', costs['solar'].sum()/lcoe.load/LCOE_escalation_factor

print 'Sum of Battery:', costs['battery'].sum()
print 'Sum of Battery Summed:', '0.0692', costs['battery'].sum()/lcoe.load/LCOE_escalation_factor

print 'Sum of Fossil:', costs['fossil'].sum()
print 'Sum of Fossil Summed:', '0.2196', costs['fossil'].sum()/lcoe.load/LCOE_escalation_factor
print '\n'

print 'total:', \
    np.sum([costs['solar'].sum()/lcoe.load/LCOE_escalation_factor,
             costs['battery'].sum()/lcoe.load/LCOE_escalation_factor,
             costs['fossil'].sum()/lcoe.load/LCOE_escalation_factor]), '0.3731'
