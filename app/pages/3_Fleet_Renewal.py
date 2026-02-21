import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processing import likert_data, scatter_comparison_data, timeline_data, ranking_data

st.set_page_config(
    page_title="Outlook on fleet renewal")

data = pd.read_csv("app/data_full_app.csv")

COLORS_LIKERT_3 = ["#ef8a62","#c7c7c7", "#67a9cf"]
COLORS_LIKERT_4 = ["#ef8a62","#c7c7c7", "#92c5de", "#0571b0"]

st.header("Outlook on fleet renewal", anchor = "renewal")

st.markdown("""In this section of the survey, we focused specifically on the replacement of aging and obsolete vehicles with more energy-efficient or more technologically advanced models (fleet renewal). We invited respondents' insights on the outlook for these newer technologies in their organizations and in the broader industry, including adoption likelihood and ranking of available decision support systems. We consider 10 specific technologies: 
- New Internal Combustion Engines (ICE), 
- Hybrid vehicles, 
- Battery Electric Vehicles (BEV), 
- Hydrogen Fuel Cell  (HFC) vehicles, 
- Smart management tools (non-A.I.),
- A.I tools, 
- Optimization and logistics innovations.
            
*Table of contents:*
1. [Plans and timeline for replacing pre-2010 vehicles](#replace-pre2010)
2. [Plans and timeline for expanding fleet (owner-operators)](#expandoo)
3. [Likelihood of pursuing fleet renewal strategies](#renewal-likelihood)
4. [Most helpful type of support to accelerate fleet renewal](#rank-support)
5. [Key barriers to fleet renewal](#barriers-renewal)
""")

st.subheader("Plans and timeline for replacing pre-2010 vehicles", anchor="replace-pre2010")

st.markdown("Respondents were asked whether they were planning to replace vehicles manufactured before model year 2010 in the coming years. Answers differ drastically by groups. The majority of fleet managers follow industry standards of short (3-5 years) replacement cycles. The vast majority of owner-operatrors with pre-2010 trucks have no plans to replace them.")


xdata, ydata, top_labels = timeline_data(data, "replace")
fig = go.Figure()

for i in range(0, len(xdata[0])):
    for j, (xd, yd) in enumerate(zip(xdata, ydata)):
        fig.add_trace(go.Bar(
            x=[xd[i]], y=[yd],
            orientation='h',
            name = top_labels[i],
            marker=dict(
                color=COLORS_LIKERT_4[i],
                line=dict(color='ghostwhite', width=1),   
            ),
            legendgroup = f'{top_labels[i]}',
            showlegend = (j == 0)
        ))

fig.update_layout(
    title=dict(text="Plans and timeline for replacing pre-2010 vehicles"),
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
    margin=dict(l=120, r=10, t=140, b=80),
    #showlegend=False,
    width = 950,
    height = 400,
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="top",
    y=1.2,
    xanchor="center",
    x = 0.5
    ),
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

st.subheader("Plans and timeline for expanding fleet (owner-operators)", anchor = "expandoo")

st.markdown("As a complement, owner-operators were asked about their plans and timeline to expand their fleet by purchasing new vehicles. The answers are not as negative, with about 1/3 of the respondents being open to a potential expansion.")

xdata, ydata, top_labels = timeline_data(data, "expand")

fig = go.Figure()

for i in range(0, len(xdata[0])):
    for j, (xd, yd) in enumerate(zip(xdata, ydata)):
        fig.add_trace(go.Bar(
            x=[xd[i]], y=[yd],
            orientation='h',
            name = top_labels[i],
            marker=dict(
                color=COLORS_LIKERT_4[i],
                line=dict(color='ghostwhite', width=1),  
            ),
            showlegend = (j==0),
            legendgroup=f'{top_labels[i]}'
        ))

fig.update_layout(
    title=dict(text="Plans and timeline for expanding fleet (Owner-operators)"),
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
    margin=dict(l=50, r=10, t=100, b=80),
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="top",
    y=1.5,
    xanchor="center",
    x = 0.5
    ),
    width = 750,
    height = 250
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

st.subheader("Likelihood of pursuing fleet renewal strategies", anchor="renewal-likelihood")

st.markdown("Respondents were asked how likely they were to pursue different fleet renewal alternatives. Owner-operators are overall more technologically averse than fleet managers, with very low likelihoods of adoption for all strategies, with the exception of **route optimization**. Conversely, the fleet manager group seems more open to adopting renewal strategies, notably **technologies aimed at improving operational efficiency** such as smart fleet management tools, A.I. tools, and route optimization. On the other hand, vehicle renewal is met with more skepticism, especially towards renewable energies (hybrid vehicles, BEV and HFC).")


slbinnov = st.selectbox("Select group", ['Fleet managers', 'Owner-Operators', 'Other'], key = "slbinnov")
xdata, ydata,top_labels = likert_data(data, "innovation",source = slbinnov)

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
            showlegend = (j == 0), 
            legendgroup = f'{top_labels[i]}'
        ))

fig.update_layout(
    title=dict(text=f'Likelihood of pursuing fleet renewal strategies - {slbinnov}', x = 0),
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
    margin=dict(l=120, r=10, t=140, b=80),
    legend=dict(
        font_size=10,
        orientation="h",
    yanchor="top",
    y=1.2,
    xanchor="center",
    x = 0.5
    ),
    width = 950,
    height = 500
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

st.subheader("Most helpful type of support to accelerate fleet renewal", anchor="rank-support")

st.markdown("""Respondents were asked to rank typical supports to accelerate fleet renewal from 1 to 5. The possible supports are: financial incentives (e.g., grants, tax credits, rebates or leasing programs), technical assistance (e.g., vehicle evaluation, planning tools), infrastructure support (e.g., fueling/charging stations), certifications (e.g. SmartWay), or other. 

Respondents who selected "other" were asked to specify. Comments include: 

> None of the above. 

> Roll back of emission regulations

> Technology that increases reliability
 
> Make the manufacturers and government responsible for the junk they make now

> Proving the DRIVER is still in control, NOT the Ai or autonomous ideas

> Less [regulations]

> I don't plan to ever adopt new technologies for my fleet replacement! If it's not diesel I won't have it.

> Larger useable bunk, lighter weight on steer axle
""")

slbrank = st.selectbox("Select group", ['All', 'Fleet managers', 'Owner-Operators', 'Other'], key = "slbrank")

df = ranking_data(data, slbrank)

plot = [go.Scatter(x = ['Financial', 'Technical', 'Infrastructure', 'Other', 'Certifications'], y = list(df.percentage), mode = 'markers', marker = dict( size = 15))]
layout = go.Layout(
    shapes=[dict(
        type='line',
        xref='x',
        yref='y',
        x0=i,
        y0=0,
        x1=i,
        y1 = list(df.percentage)[i],
        line=dict(
            color='black',
            width=2
        ),
        layer = 'below',
    ) for i in range(len(df.question))],
    template = 'ggplot2',
    title = dict(text=f'Most helpful types of support for: {slbrank}',x = 0),
    annotations = [dict(xref='x', yref='y',
                            x=i, y= list(df.percentage)[i] + 15,
                            xanchor='center',
                            text=f'Ranked #1 for <b>{list(df.percentage)[i]:.1f}%</b> <br> of respondents',
                            font=dict(family='Arial', size=12,
                                      color='rgb(102, 102, 102)'),
                            showarrow=False, align='center') for i in range(len(df.question))],
    width = 800, 
    height = 300, 
    margin = dict(t = 50, l = 20, r = 20, b = 0),
    xaxis = dict(showgrid = False, 
                 showline=True,
        linecolor='rgb(102, 102, 102)', 
        ),
    yaxis = dict(visible = False,rangemode = 'tozero'),
paper_bgcolor='white',
    plot_bgcolor='white',
    
)

f = go.Figure(plot, layout)
st.plotly_chart(f)



st.subheader("Key barriers to fleet renewal", anchor = "barriers-renewal")
st.markdown("Respondents were asked to identify up to 3 key barriers against fleet renewal. Both fleet managers and owner-operators consider **capital costs for new vehicles** to be a barrier, followed by concerns around **vehicle performance and reliability**. In third position, owner-operators are more concerned about the **uncertainty around future regulations**, while fleet managers are concerned about the **limited availability of suitable models.**")

ms_bar = st.multiselect("Select group", ['Fleet managers','Owner-Operators'], default=["Fleet managers", "Owner-Operators"], key="ms_bar")

#xfm3 = st.checkbox(label = "Fleet managers", value = True, key = 'barriersfm')
#xoo3 = st.checkbox(label = "Owner-operators", key = 'barriersoo')

df = scatter_comparison_data(data, 'barriers')

fig = go.Figure()

if "Fleet managers" in ms_bar:
    fig.add_trace(go.Scatter(
        x=list(df['Fleet managers']),
        y=list(df['Barriers']),
        name='Fleet managers',
        marker=dict(
            color='rgb(102, 102, 102)',
            line_color='rgba(156, 165, 196, 1.0)',
        )
    ))
if "Owner-Operators" in ms_bar: 
    fig.add_trace(go.Scatter(
        x=list(df['Owner-Operators']),
        y=list(df['Barriers']),
        name='Owner-operators',
        marker=dict(
            color='rgba(204, 204, 204, 0.95)',
            line_color='rgba(217, 217, 217, 1.0)'
        )
    ))

fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))

fig.update_layout(
    title=dict(text="Key barriers to fleet renewal"),
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

