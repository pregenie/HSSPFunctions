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
included_solar_to_meet_battery_losses = 0.0
battery_system_size_power = 0.00
battery_system_size_energy = 0.00
fossil_generator_size =	14.40
fossil_generator_fuel_usage = 9.68

# FOSSIL GENERATOR
generation_selection = 1
generation_type = 'Combustion Engine - High Speed'
capital_cost = 750
fixed_OM = 45
variable_OM = 18.75
fixed_and_additional_OPEX_cost = .06
average_efficiency = .352
fuel_selection = 4
fuel_type = 'Diesel'
fuel_measurement_unit = 'US Gal'
fuel_heat_value	= 0.135
fuel_cost = 4.625
fuel_cost_escalation = .03
min_generator_size_for_reliability = 1.2
number_of_generators = 10
minimum_gen_loading = .20
unit_availability = .80
plant_availability = .975
generator_max_capacity_factor = 1.0
generator_lifetime = 18000
generator_refurbishments= 2
refurbishment_cost = 375

min_generator_size_for_reliability = 1.20       # Hybrid System Design!F27
number_of_generators = 10                       # Hybrid System Design!F28
minimum_gen_loading	= .20                       # Hybrid System Design!F29

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
def load_ppa_arrays(term, factor, load_growth, daily_load):
    a = 0
    serving = 0
    load = 0
    print 'inc', 'factor',' serving', 'load'
    while a < term+1:
        print a, factor, serving, load
        factor = factor/(1+wacc)
        serving = daily_load*365*(1+load_growth)**(a-1)/1000
        load += factor*serving
        a+=1
    return load


LCOE_escalation_factor = 1.1435734517
load = load_ppa_arrays(ppa_term, discount_factor, yearly_load_growth, daily_load_requirement)

print 'Sum of Solar:', costs['solar'].sum()
print 'Sum of Solar Summed:', '0.0844', costs['solar'].sum()/load/LCOE_escalation_factor

print 'Sum of Battery:', costs['battery'].sum()
print 'Sum of Battery Summed:', '0.0692', costs['battery'].sum()/load/LCOE_escalation_factor

print 'Sum of Fossil:', costs['fossil'].sum()
print 'Sum of Fossil Summed:', '0.2196', costs['fossil'].sum()/load/LCOE_escalation_factor
print '\n'

print 'total:', \
    np.sum([costs['solar'].sum()/load/LCOE_escalation_factor,
             costs['battery'].sum()/load/LCOE_escalation_factor,
             costs['fossil'].sum()/load/LCOE_escalation_factor]), '0.3731'
