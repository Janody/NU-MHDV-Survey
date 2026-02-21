import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processing import likert_data, scatter_comparison_data

st.set_page_config(
    page_title="Fleet turnover practices")

data = pd.read_csv("data_full_app.csv")

COLORS_LIKERT_3 = ["#ef8a62","#c7c7c7", "#67a9cf"]
COLORS_LIKERT_4 = ["#ef8a62","#c7c7c7", "#92c5de", "#0571b0"]


st.header("Fleet turnover practices")

st.markdown("""This section of the survey aims to understand the respondents' practices regarding fleet turnover, defined as “the rate at which aging or obsolete vehicles in a defined fleet are retired or substituted with newer models over a given period, regardless of the characteristics of the replacement vehicles.
            
*Table of contents:*
1. [Top priorities when evaluating fleet turnover options](#turnover-priorities)
2. [Primary cost and financial considerations influencing turnover decisions](#cost-considerations)
3. [Tools and methods to support fleet turnover decisions](#tools-turnover)
4. [Vehicles prioritized for replacement](#veh-replacement)
5. [Typical purchase markets](#purchase-markets)
""")


st.subheader("Top priorities when evaluating fleet turnover options", anchor = "turnover-priorities")

st.markdown("""Respondents were asked to select up to 3 top priorities when evaluating fleet turnover options, out of 8 alternatives.
The number one concern for both fleet managers and owner-operators is the **reliability of the new vehicle**, followed by the potential for **cost savings** and **operational efficiency**. The two groups differ in the 4th priority: **compliance with regulations** for fleet managers and **driver's comfort and satisfaction** for owner-operators. For both groups, the potential reduction in emissions is a priority for only a minority of respondents.""")


ms_pri = st.multiselect("Select group", ['Fleet managers','Owner-Operators'], default=["Fleet managers", "Owner-Operators"], key="ms_pri")

df = scatter_comparison_data(data, 'turnover')
fig = go.Figure()

if 'Fleet managers' in ms_pri:
    fig.add_trace(go.Scatter(
        x=list(df['Fleet managers']),
        y=list(df['Priorities']),
        name='Fleet managers',
        marker=dict(
            color='rgb(102, 102, 102)',
            line_color='rgba(156, 165, 196, 1.0)',
        )
    ))
if 'Owner-Operators' in ms_pri: 
    fig.add_trace(go.Scatter(
        x=list(df['Owner-Operators']),
        y=list(df['Priorities']),
        name='Owner-operators',
        marker=dict(
            color='rgba(204, 204, 204, 0.95)',
            line_color='rgba(217, 217, 217, 1.0)'
        )
    ))

fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))

fig.update_layout(
    title=dict(text="Top priorities when evaluating fleet turnover options"),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=10,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)',
        title = 'Percentage of respondents'
    ),
    margin=dict(l=140, r=40, b=50, t=80),
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="center",
    x = 0.2
    ),
    width=800,
    height=600,
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='closest',
    template = 'ggplot2'
)

st.plotly_chart(fig)

st.subheader("Primary cost and financial considerations influencing turnover decisions", anchor= "cost-considerations")

st.markdown("""Respondents were asked to select up to three cost and financial considerations influencing their company's turnover decision.**Maintenance and repair costs** are the most frequent financial consideration across both groups, followed by **fuel and energy costs** and **upfront costs for vehicle acquisition**. Owner-operators generally consider less often financing and leasing terms and optimization of lifecycle costs than fleet managers.""")

ms_fin = st.multiselect("Select group", ['Fleet managers','Owner-Operators'], default=["Fleet managers", "Owner-Operators"], key="ms_fin")

#xfm2 = st.checkbox(label = "Fleet managers", value = True, key = 'financialfm')
#xoo2 = st.checkbox(label = "Owner-operators", key = 'financialoo')

df = scatter_comparison_data(data, 'financial')
fig = go.Figure()

if "Fleet managers" in ms_fin:
    fig.add_trace(go.Scatter(
        x=list(df['Fleet managers']),
        y=list(df['Financial']),
        name='Fleet managers',
        marker=dict(
            color='rgb(102, 102, 102)',
            line_color='rgba(156, 165, 196, 1.0)',
        )
    ))
if "Owner-Operators" in ms_fin: 
    fig.add_trace(go.Scatter(
        x=list(df['Owner-Operators']),
        y=list(df['Financial']),
        name='Owner-operators',
        marker=dict(
        color='rgba(204, 204, 204, 0.95)',
        line_color='rgba(217, 217, 217, 1.0)'
        )   
    ))

fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))
fig.update_layout(
    title=dict(text="Primary cost and financial considerations influencing turnover decisions"),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=10,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)',
        title = 'Percentage of respondents'
    ),
    margin=dict(l=100, r=40, b=50, t=80),
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="center",
    x = 0.2
    ),
    width=800,
    height=650,
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='closest',
    #template = 'ggplot2'
)

st.plotly_chart(fig)

st.subheader("Tools and methods to support fleet turnover decisions", anchor = "tools-turnover")

st.markdown("""Respondents were asked how frequently their company used the following tools or method to support their fleet turnover decisions.
**Maintenance and perfomance tracking** is consistently used by all groups. The majority of fleet managers uses all available tools at least sometimes, but more often **vehicle usage data**, **regulatory compliance assessment** and **cost analysis tools**. On the other hand, owner-operators rely less often on decision-making tools, in particular data- or AI-driven solutions.""")

slbtool = st.selectbox("Select group", ['Fleet managers', 'Owner-Operators', 'Other'], key = "slbtool")
xdata, ydata,top_labels = likert_data(data, "decision_tools",source = slbtool)

fig = go.Figure()

for i in range(0, len(xdata[0])):
    for j, (xd, yd) in enumerate(zip(xdata, ydata)):
        fig.add_trace(go.Bar(
            x=[xd[i]], y=[yd],
            orientation='h',
            name = top_labels[i],
            marker=dict(
                color=COLORS_LIKERT_3[i],
                line=dict(color='ghostwhite', width=1),
                
            ),
            showlegend = (j==0),
            legendgroup = f'{top_labels[i]}'
        ))

fig.update_layout(
    title=dict(text=f"Use of tools to support fleet turnover decisions<br><i>{slbtool}</i>"),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=10,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)',
        title = 'Percentage of respondents',
        domain=[0.15, 1]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    barmode='stack',
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=70, r=10, t=140, b=80),
    width = 950,
    height = 600,
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="top",
    y=1.1,
    xanchor="center",
    x = 0.5
    )
)

annotations = []

for yd, xd in zip(ydata, xdata):
    # labeling the y-axis
    annotations.append(dict(xref='paper', yref='y',
                            x=0.14, y=yd,
                            xanchor='right',
                            text=str(yd),
                            font=dict(family='Arial', size=14,
                                      color='dimgray'),
                            showarrow=False, align='right'))

fig.update_layout(annotations=annotations)

st.plotly_chart(fig)

st.subheader("Vehicles prioritized for replacement", anchor = "veh-replacement")

st.markdown("Fleet managers were asked which vehicles are typically prioritized for replacement. Answers highlight that priority is typically given to vehicles with the **highest maintenance costs**, **oldest by age** and with the **highest mileage**.")

d = data.copy()
replacement_q = [f'replacement_priority_{i}' for i in range(1,8)]
d = d[replacement_q]

for c in replacement_q:
    tot_respondents = len(d[~d[c].isna()])
    d[c] = 100*d[c].sum()/tot_respondents

d = d.iloc[0].rename({'replacement_priority_1':'Oldest by age', 
              'replacement_priority_2':'Highest maintenance costs',
              'replacement_priority_3':'Highest mileage',
              'replacement_priority_4':'Outdated technology',
              'replacement_priority_5':'Assigned to specific <br>vocations or duty cycles',
              'replacement_priority_6':'Poor fuel efficiency',
              'replacement_priority_7':'Highest emissions'})

d = d.reset_index().rename(columns = {'index': 'Priorities', 0: 'Percentage'}).sort_values(by = 'Percentage', ascending = False)

f = px.bar_polar(
    d,
    r="Percentage",
    theta="Priorities",
    color="Percentage", 
    color_continuous_scale = px.colors.sequential.Sunset,
    hover_name = 'Priorities',
    hover_data = {'Priorities': False, 'Percentage': ':.1f'},
    labels= {'Percentage': 'Percentage<br> of respondents'}
    )

f.update_layout(
    title = dict(text = 'Vehicles prioritized for replacement',
                  y = 0.99, x = 0),
    polar_hole=0.25,
    height=500,
    width=800,
    margin=dict(b=50, t=60, l=50, r=0),
    template = 'ggplot2',
    polar = dict(radialaxis = dict(showticklabels = False, showline = False, ticks = ""))
    #showlegend = False, 
)

f.update_coloraxes(colorbar_orientation='h', colorbar_y=-0.5) 

st.plotly_chart(f)

st.subheader("Typical purchase markets", anchor = "purchase-markets")

st.markdown("Respondents were asked which markets their company typically purchases from to replace vehicles. A significant number of respondents buys **new** or a **mix of new and used**. This distribution is not equal across groups: the majority of fleet managers use a mix of new and used markets, while owner-operators rely more on the used market. ")

slbmarket = st.selectbox("Select group", ['All', 'Fleet managers', 'Owner-Operators', 'Other'], key = "slbmarket")

df = data.copy()
sources = df.source.unique()

df= df[df.purchase_markets != 7]

df.purchase_markets = df.purchase_markets.map({1: 'New', 2: 'Used', 3: 'Mix of new and used', 4: 'Leasing', 5: 'Other'})

d = df[['source','purchase_markets']].groupby(['source', 'purchase_markets']).size()
d = d.reset_index().rename(columns = {0: 'count'})
tot_groups = d.groupby('source')['count'].sum().to_dict()
d['percentage'] = d.apply(lambda x:100*x['count']/tot_groups[x['source']], axis = 1)

if slbmarket == 'All':
    ds = df[['source','purchase_markets']].groupby('purchase_markets').size()
    ds = ds.reset_index().rename(columns = {0: 'count'})
    ds['percentage'] = 100*ds['count']/len(df)
else: 
    ds= d[d.source == slbmarket]

f = px.bar_polar(
    ds,
    r="percentage",
    theta="purchase_markets",
    color="percentage", 
    color_continuous_scale = px.colors.sequential.Sunset,
    hover_name = 'purchase_markets',
    hover_data = {'purchase_markets': False, 'percentage': ':.1f'},
    labels= {'percentage': 'Percentage of respondents', 'purchase_markets': 'Purchase markets'},
    range_r = [0,80],
    range_color = [0,60]
    ).update_layout(
    title = dict(text = f'Typical purchase markets: {slbmarket}',
                  y = 0.99, x = 0),
    polar_hole=0.25,
    height=500,
    width=800,
    margin=dict(b=50, t=60, l=50, r=0),
    template = 'ggplot2',
    polar = dict(radialaxis = dict(showticklabels = False, showline = False, ticks = ""))
    #showlegend = False,
    )
f.update_coloraxes(colorbar_orientation='h', colorbar_y=-0.5) 

st.plotly_chart(f)