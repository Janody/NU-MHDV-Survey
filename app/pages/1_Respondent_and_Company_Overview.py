import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Respondent profile, company and fleet overview")

data = pd.read_csv("data_full_app.csv")

st.header("Respondent profile, company and fleet overview")
st.markdown("""*Table of contents:*
1. [Respondent's current role](#current-role)
2. [Fleet size (fleet managers only)](#fleet-size)
3. [Regions of operation](#region-op)
4. [Fleet vocation](#fleet-vocation)
5. [Fleet composition](#fleet-composition)
""")
st.subheader("Respondent's current role", anchor = "current-role")
st.markdown(f'''We have a sample of **{len(data)} respondents**, including **{len(data[data.source == 'Fleet managers'])} fleet managers**, **{len(data[data.source == 'Owner-Operators'])} owner-operators**, and **{len(data[data.source == 'Other'])}** respondents in other roles. Other roles include: non-manager employees of trucking companies, fleet managers of non-trucking organizations, respondents in industries adjacent to trucking without operating fleets, retired or unemployed respondents.
''')
roles = ['Owner operator', 'Fleet manager', 'Employed (non-manager)', 'Other']
d = data.copy()
d['current_role'] = d['current_role'].map({3: 'Owner operator', 1: 'Fleet manager',2: 'Employed (non-manager)', 4:'Other'})
d = (100*d['current_role'].value_counts()/len(d)).reset_index()
fig = px.bar(d, x='current_role', y='count', color = 'current_role', labels = {'count' : 'Percentage of respondents', 'current_role': 'Current role'}, template = 'ggplot2') 

st.plotly_chart(fig)

st.subheader("Fleet size (fleet managers only)", anchor="fleet-size")

d = data.copy()
d['fleet_size'] = d['fleet_size'].map({1:'Very small<br>(1-6 veh)', 2:'Small<br>(7-19 veh)', 
              3:'Medium<br>(20-100 veh)', 4:'Large<br>(101-2,000 veh)', 5:'Very Large<br>(2,001-5,000 veh)', 6:'Mega fleet<br>(5,001+)'})
d = d['fleet_size'].value_counts(normalize = True, dropna = True, sort = False)
d['Very Large<br>(2,001-5,000 veh)'] = 0
d = d[['Very small<br>(1-6 veh)', 'Small<br>(7-19 veh)',
        'Medium<br>(20-100 veh)', 'Large<br>(101-2,000 veh)', 'Very Large<br>(2,001-5,000 veh)', 'Mega fleet<br>(5,001+)']]

d = d*100
d = d.reset_index()

st.markdown(f"""
The majority of repsondents in our survey manage **medium** fleets of 20-100 vehicles ({d[d.fleet_size == 'Medium<br>(20-100 veh)']['proportion'].values[0]:.1f}%).
""")
fig = px.bar(d, x='fleet_size', y='proportion', labels = {'proportion' : 'Percentage of fleet managers', 'fleet_size': 'Fleet size'}, 
             template = 'ggplot2', width=900, height=400)

st.plotly_chart(fig)

st.subheader("Regions of operation", anchor = "region-op")

st.markdown("The **Midwest** is the most represented region in our sample (41% of respondents, including 68% of owner-operators), followed by the **South** (33% of respondents, 42% of owner-operators) and national operators (30% of respondents, including 37% of fleet managers).")

bsource = st.pills("Filter by source", ['All','Fleet managers', 'Owner-Operators', 'Other'],  selection_mode="single", default="All", key="b_region")

if bsource == 'All':
    d_regions = data[['region_1', 'region_2', 'region_3', 'region_4', 'region_5', 'region_6']].sum().reset_index().rename(columns = {'index': 'region', 0 : 'count'})
    tot_size = len(data)
else: 
    d_regions = data[data.source == bsource][['region_1', 'region_2', 'region_3', 'region_4', 'region_5', 'region_6']].sum().reset_index().rename(columns = {'index': 'region', 0 : 'count'})
    tot_size = len(data[data.source == bsource])
                   
#d_regions['path'] = ['region_2', "", "region_1", "region_1", "region_1", "region_1"]
region_labels = {'region_1': 'Nationally, across the US',
                 'region_2':'Internationally', 
                 'region_3':'Midwest', 
                 'region_4': 'South', 
                 'region_5': 'Northeast', 
                 'region_6': 'West'}

d_regions = d_regions.replace(region_labels)
d_regions['proportion'] = 100*d_regions['count']/tot_size
colors = px.colors.sequential.Sunset_r



f = px.bar(d_regions, x='region', y='proportion', labels = {'proportion' : 'Percentage of respondents', 'region': 'Region of operations'}, 
             template = 'ggplot2', width=900, height=400, color_discrete_sequence = colors)
f.update_layout(title = dict(text = f'Region of operations: {bsource}', x = 0))

st.plotly_chart(f)

st.subheader("Fleet vocation", anchor = "fleet-vocation")

st.markdown("**Long-haul** and **regional** operations are the most common vocations among respondents in our sample. Fleet managers operate more frequently regional operations (52%), while a majority owner-operators are involved with long-haul trucking (56%).")


bsfv = st.pills("Filter by source", ['All','Fleet managers', 'Owner-Operators', 'Other'],  selection_mode="single", default="All", key="bsfv")

if bsfv == 'All':   
    d_fv = data[['fleet_vocation_1', 'fleet_vocation_2', 'fleet_vocation_3', 'fleet_vocation_4', 'fleet_vocation_5', 'fleet_vocation_6']].sum().reset_index().rename(columns = {'index': 'fleet_vocation', 0: 'count'})
    tot_size = len(data)
else:
    d_fv = data[data.source == bsfv][['fleet_vocation_1', 'fleet_vocation_2', 'fleet_vocation_3', 'fleet_vocation_4', 'fleet_vocation_5', 'fleet_vocation_6']].sum().reset_index().rename(columns = {'index': 'fleet_vocation', 0: 'count'})
    tot_size = len(data[data.source == bsfv])


d_fv['fleet_vocation'] = d_fv['fleet_vocation'].replace({'fleet_vocation_1': 'Drayage',
                                                        'fleet_vocation_2': 'Long-haul',
                                                        'fleet_vocation_3': 'Regional',
                                                        'fleet_vocation_4': 'Urban Logistics',
                                                        'fleet_vocation_5': 'Mixed Use',
                                                        'fleet_vocation_6': 'Other'})

d_fv['proportion'] = 100*d_fv['count']/tot_size

f = px.bar(d_fv, x='fleet_vocation', y='proportion', labels = {'proportion' : 'Percentage of respondents', 'fleet_vocation': 'Fleet vocation'}, 
             template = 'ggplot2', width=900, height=400, color_discrete_sequence = colors[1:])
f.update_layout(title = dict(text = f'Fleet vocation: {bsfv}', x = 0))

#     colors =  px.colors.sequential.Sunset

st.plotly_chart(f)


st.subheader("Fleet composition", anchor = "fleet-composition")

st.markdown("""Regarding fleet characteristics, we asked about the proportion of vehicles in the fleet dedicated to urban logistics, the proportion of vehicles with pre-2010 engines, and the proportion of Class 6 and higher vehicles. On average, the majority of vehicles in fleets of 100 vehicles and more are of **Class 6 and higher** (53%). This percentage drops to *18%* for smaller fleets (less than 100 vehicles in the fleet). On average, almost half of the vehicles in larger fleets are used for **urban logistics** (23% for smaller fleets).

For owner-operators, the majority owns a Class 6 or higher vehicle (57%), and about a third own a vehicle with a pre-2010 engine.
""")

bsfc = st.pills("Filter by source", ['Fleet managers', 'Owner-Operators'],  selection_mode="single", default="Fleet managers", key="bsfc")

if bsfc == 'Fleet managers':
    bfsize = st.pills("Filter by fleet size", ['Less than 100 vehicles', 'More than 100 vehicles'],  selection_mode="single", default="Less than 100 vehicles", key="bfsize")
    if bfsize == 'Less than 100 vehicles':
        typ = "< 100 vehicles"
    else: 
        typ = "> 100 vehicles"
    d = data[data.fleet_type == typ][['percentage_pre_2010', 'percentage_class_6', 'percentage_urban_logistics']].dropna(how = 'any')
    d = d[['percentage_pre_2010', 'percentage_class_6', 'percentage_urban_logistics']].mean(axis = 0).reset_index().rename(columns = {'index':'veh_char', 0: 'average'})
    labels = {'percentage_pre_2010': 'Pre-2010 engine', 
          'percentage_class_6': 'Class 6+', 
          'percentage_urban_logistics': 'Used for urban logistics'}
    d = d.replace(labels)

    f = px.bar(d, x='veh_char', y='average', labels = {'veh_char' : 'Vehicle characteristics', 
                                                       'average': 'Average proportion of fleet'}, 
                    template = 'ggplot2',
                    width=900, height=400, 
                    color_discrete_sequence = colors[2:],
                    range_y = [0,80]
                    )
    f.update_layout(title = dict(text = f'Fleet composition: {bsfc} ({bfsize})', x = 0))

else: 
    d = data[[f'oo_veh_char_{i}' for i in range(1,4)]].sum()
    d = 100*d/len(data[data.source == bsfc])

    labels = {'oo_veh_char_1': 'Pre-2010 engine', 
          'oo_veh_char_2': 'Class 6+', 
          'oo_veh_char_3': 'Used for urban logistics'}
    
    d = d.reset_index().rename(columns = {'index': 'veh_char', 0: 'percentage'}).replace(labels)
    f = px.bar(d, x='veh_char', y='percentage', labels = {'veh_char' : 'Vehicle characteristics', 'percentage': 'Percentage of respondents'}, 
             template = 'ggplot2', width=900, height=400, color_discrete_sequence = colors[2:])
    
    f.update_layout(title = dict(text = f'Fleet composition: {bsfc}', x = 0))

st.plotly_chart(f)
    






