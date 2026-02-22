
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Northwestern MHDV Survey")


st.header("Open comments")

st.markdown("""The survey included several opportunities for respondents to express their opinions through open comments. Specifically, they were asked what   were, in their opinion the least and most promising innovations for fleet renewal in the next 3 years. Another question asked them to share aspects of fleet renewal that they felt were not well understood -- either within their organization or more broadly across the industry.

*Table of contents*
1.  [Least and most promising innovations](#bestworst)
2.  [Misunderstood aspects of fleet renewal](#misunderstood)
""")

st.subheader("Least and most promising innovations", anchor = "bestworst")

st.markdown("This figure shows the proportional share of mentions by group for each innovation keyword, appearing in either \"best\" or \"worst\" innovation comments. Each cell represents the percentage of all mentions within a group that referred to a given innovation, allowing for comparison across    Fleet Managers, Owner-Operators, and Others regardless of group size.")

st.markdown("For the most promising innovations, **A.I.** is the most mentioned by fleet managers, while owner-operators mentioned more often **improvements in mileage and fuel efficiency**. While a significant part of fleet managers considers **electric vehicles** one of the most promising  innovations, it is mentioned as the least promising by the majority of respondents across all groups, followed by **hydrogen fuel cell vehicles**    for fleet managers and **self-driving vehicles** for owner-operators. Owner-operators also highlighted the role of regulations in the adoption of  innovative strategies, both positively and negatively.")

st.markdown("*Click on any cell to zoom in.*")


innov_df = pd.read_csv("app/innovation_best_worst.csv")
innov_df = innov_df.melt(id_vars = ['Category', 'Innovation'], value_vars = ['FM', 'OO', 'Other'], var_name = 'source', value_name = 'proportion')
innov_df['source'] = innov_df['source'].map({'FM': 'Fleet managers', 'OO': 'Owner-Operators', 'Other': 'Other'})

colors_tm = ["#f7f7f7","#92c5de", "#f4a582"]
f = px.treemap(innov_df, path =['source','Category', 'Innovation'], values = 'proportion',width=1000, height=500, template = 'ggplot2', color = 'Category', color_discrete_sequence = colors_tm, hover_data = ["source", "Category", "Innovation", "proportion"], hover_name = "Innovation")
f.update_traces(root_color='rgb(243,243,243)',
                hovertemplate=["Name=%{label}<br>Category=%{parent}<extra></extra>" if label in f.data[0].parents else "Category=%{parent}<br>Innovation=%{label}<br>Proportion=%{value}<extra></extra>" for label in f.data[0].ids])
f.update_layout(title = dict(text = 'Proportion of keywords mentions per group'), uniformtext=dict(minsize=14),)

st.plotly_chart(f)

st.subheader("Misunderstood aspects of fleet renewal", anchor = "misunderstood")

st.markdown("This table displays all comments made by respondents, categorized into broad themes. Some responses touched on multiple topics and are categorized under multiple categories: technology, brand or image, costs, regulation, organization or firm management, operations, maintenance, and environmental issues.)")

st.markdown("Several similarities emerge across fleet managers, owner-operators, and others in how they responded. **Costs** and the true **total cost of ownership** were emphasized by all three groups, with respondents in each noting that organizations tend to focus on upfront expenses while overlooking long-term factors such as maintenance, downtime, depreciation, and residual value. Similarly, **regulatory issues** were raised in every group, particularly around emissions standards, compliance burdens, and inconsistent rules across jurisdictions. Finally, **emerging technologies** (such as EVs, AI, and automation) appeared as a cross-cutting theme, though the tone ranged from optimism to skepticism depending on the respondent.")

data = pd.read_csv('app/text_df.csv', encoding = 'utf-8-sig')
data = data[~data.category1.isna()]

button_source = st.pills("Filter by group", ['Fleet managers', 'Owner-Operators', 'Other'],  selection_mode="multi", default=None, key="button_source2")

button_topic = st.pills("Filter by topic", ['Technology', 'Brand/Image', 'Cost', 'Regulation',
       'Organization', 'Operations', 'Maintenance', 'Environment'],  selection_mode="multi", key="button_topic2", default=None)

categories = data[~data["category1"].isna()]['category1'].unique()


if button_source:
    if button_topic:
        mask = (data.source.isin(button_source))& (data.category1.isin(button_topic) | data.category2.isin(button_topic))
    else:
        mask = data.source.isin(button_source)
    data_filt = data[mask]
else:
    if button_topic:
        mask = (data.category1.isin(button_topic) | data.category2.isin(button_topic))
        data_filt = data[mask]
    else: 
        data_filt = data


COLUMN_CONFIG = {
    "source":st.column_config.MultiselectColumn(label = 'Group', options=set(data["source"].unique()), color="auto", width = 'medium'),
    "comment":st.column_config.TextColumn(label = 'Comment', width = 'large'),
    "category1": st.column_config.MultiselectColumn(label = 'Category 1', options=categories, color="auto", width = 'medium'),
    "category2": st.column_config.MultiselectColumn(label = 'Category 2', options=categories, color="auto", width = 'medium')
}

f'*Displaying {len(data_filt)} comments. Click on any "comment" cell to read full comment.*'

st.dataframe(data_filt, hide_index = True, column_config = COLUMN_CONFIG)

with st.container():
    st.markdown("""<div style="float: right;
                background: #f5f5f5;
                color: #444;
                font-size: 12px;
                line-height: 1.3;
                padding: 6px 10px;
                border-radius: 6px;
                border: 1px solid #e6e6e6;
                display: inline-block;
                text-align: left;">
                The comment analysis was conducted by Deirdre Edward.</div>""", unsafe_allow_html=True)
