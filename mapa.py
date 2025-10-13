import streamlit as pd
fig = px.choropleth(dataset, locations=dataset ['iso3'], color=dataset['nome'], hover_name=dataset['nome'])
fig.update_layout(title="Mapa coroplético dos países!", geo_scope='world')
fig.show()
