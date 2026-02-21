import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Fleet manager and Owner-Operators survey -- Results",
)

st.logo("Northwestern_purple_RGB.png", )
"""
# Fleet managers and owner-operators survey 

This dashboard summarizes results from a **national survey of U.S. medium- and heavy-duty vehicle (MHDV) operators** conducted by the Mobility and Transport Laboratory at Northwestern University. The goal of the study is to understand **how fleets make decisions** about replacing older trucks, what **tools and constraints** influence these decisions, and how companies, large and small, view **future options** available to them.
We reached both **fleet managers** and **owner-operators** to reflect the full range of business models, operating environments, and vehicle use cases across the industry.

## What the survey covers

The survey focuses on practical, day-to-day decision-making around fleet turnover. Topics include:

- How companies manage vehicle age, replacement cycles, and operational needs
- What tools or data they rely on when deciding to retire or replace a truck
- Willingness to consider different technology options, from newer diesel models to low- and zero-emission vehicles
- Views on regulations, incentives, and other external pressures influencing turnover decisions

## Survey recruitment 

Recruitment focused on achieving strong representation across fleet sizes, operating models, vehicle classes, and geographic regions. We partnered with industry associations, including NACFE, ITA, M-WTA, IAC, and OOIDA, to reach both carriers and independent owner-operators.

## Collaborators
- **Amanda Stathopolous**, Department of Civil and Environmental Engineering
- **Bret Johnson**, Transportation Center
- **Janody Pougala**, Department of Civil and Environmental Engineering,
- **Deirdre Edward**, Department of Engineering Science and Applied Mathematics

"""
st.space()



with st.container():
    st.markdown("""<div style="
                background: #f5f5f5;
                color: #444;
                font-size: 12px;
                line-height: 1.3;
                padding: 6px 10px;
                border-radius: 6px;
                border: 1px solid #e6e6e6;
                display: inline-block;
                text-align: left;">
                <strong>Disclaimers: </strong> This work was supported by RFQ 24-1 of the Health Effects Institute (HEI), an organization jointly funded by the United States Environmental Protection Agency (EPA) (Assistance Award No.CR-83590201) and certain motor vehicle and engine manufacturers. The research described here does not necessarily reflect the views of HEI, nor does it necessarily reflect the views and policies of HEI's sponsors (US Environmental Protection Agency or motor vehicle and engine manufacturers). <br> 
                All recruitment materials and the survey instrument were approved by Northwestern University's IRB (STU00222057).</div>""", unsafe_allow_html=True)

st.space()
col1, col2, col3 = st.columns(3)
with col1:
    st.image("mccormick_logo.png")
with col2: 
    st.image("nutc_logo.png")
with col3:
    st.image("hei_logo.png")


