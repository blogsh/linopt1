# PARAMETER DEFINITION

param biodiesel_per_veggie_oil;
param biodiesel_per_methanol;
param methanol_price;
param petrol_price;

param max_petrol;
param max_area;
param max_water;

param min_diesel;

set Plants;

param seed_yield{p in Plants};
param water_demand{p in Plants};
param oil_yield{p in Plants};

set DieselType;

param bio_percentage{d in DieselType};
param sale_price{d in DieselType};
param tax{d in DieselType};

# VARIABLE DEFINITION

var area{p in Plants} >= 0;
var veggieOil >= 0;
var methanol >= 0;
var biodiesel >= 0;
var petrol >= 0;
var diesel{d in DieselType} >= 0;
var sales{d in DieselType} >= 0;
var costs{d in DieselType} >= 0;

var profits{d in DieselType} >= 0;

# OPTIMIZATION PROBLEM

#maximize PROFIT: sum{d in DieselType} (1 - tax[d]) * (sales[d] - costs[d]);

maximize PROFIT: sum{d in DieselType} (1 - tax[d]) * profits[d];
subject to PROFITS{d in DieselType}: profits[d] = sales[d] - costs[d];

subject to AREA: sum{p in Plants} area[p] <= max_area;
subject to WATER: sum{p in Plants} water_demand[p] * area[p] <= max_water;
subject to PETROL: petrol <= max_petrol;
subject to OVERALL: sum{d in DieselType} diesel[d] >= min_diesel;

subject to VEGGIEOIL: veggieOil = sum{p in Plants} seed_yield[p] * oil_yield[p] * area[p];

subject to BIODIESEL: biodiesel = biodiesel_per_veggie_oil * veggieOil;# + biodiesel_per_methanol * methanol;
subject to METHANOL:  methanol = biodiesel / biodiesel_per_methanol;

subject to BIODIESEL_DIESEL: sum{d in DieselType} bio_percentage[d] * diesel[d] = biodiesel;
subject to PETROL_DIESEL: sum{d in DieselType} (1 - bio_percentage[d]) * diesel[d] = petrol;

subject to SALES{d in DieselType}: sales[d] = sale_price[d] * diesel[d];
subject to COSTS{d in DieselType}: costs[d] 
	= diesel[d] * bio_percentage[d] / biodiesel_per_methanol * methanol_price
	+ diesel[d] * (1 - bio_percentage[d]) * petrol_price;

objective PROFIT;
