import plotly.express as px

# Define visualizations
def generate_visualizations(df):
    df_atrasos = df[((df.status=='A') | (df.status=='C')) & (df.data_vencimento < '20240617')]
    # New visualization 1
    # df1 = series.groupby("year").size().reset_index(name='count')
    df1 = df_atrasos["razao_cliente"].value_counts().head(15).reset_index(name='count')
    fig_line_count = px.line(df1, x='year', y='count', title='Work Count Over Time')

    # Update line color to yellow
    fig_line_count.update_traces(line=dict(color='yellow'))

    # Update layout with dark template and yellow font color
    fig_line_count.update_layout(template='plotly_dark', font=dict(color='yellow'))

    # New visualization 2

    # df2 = series.groupby("year")["votes"].mean().reset_index(name='votes')
    df2 = df_atrasos["razao_cliente"].value_counts().head(15).reset_index(name='count')
    fig_line_votes = px.line(df2, x='year', y='votes', title='Work Votes Over Time')

# Update line color to yellow
    fig_line_votes.update_traces(line=dict(color='yellow'))

# Update layout with dark template and yellow font color
    fig_line_votes.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_line_count, fig_line_votes