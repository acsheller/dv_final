'''
EN.605.662 Data Visualization Final project
Tony Sheller

A Streamlit based application for Visualizing resources in Kubernetes

'''

import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.error import URLError
from kubernetes import client, config

def get_k8s_pods():
    '''
    
    '''
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    pd_ct = []
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        
        print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")


st.set_page_config(layout = "wide")

c1,c2 = st.columns(2)

page = st.sidebar.selectbox('Select View',['Start','option1']) 

st.markdown(
"""
<script>
// Function to scroll to the top of the page
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Scroll to top on page load
window.onload = function() {
    scrollToTop();
};
</script>
""",
unsafe_allow_html=True
)





if page == 'Start':
    c1.subheader('EN.605.662 Data Visualization Final Project')
    c1.subheader('Author: Anthony Sheller')
    c1.markdown(
        """
        **Overview**
        PLANETINA combines GPU acceleration with Network acceleration for containers operating in Kubernetes (K8s).
        The application being viewed is a streamlit application running in K8s.


        **Instructions**

        From the dropdown on the left select the visusalization you would like to view.
    """)
    # https://rickandmorty.fandom.com/wiki/Planetina
    c1.image('images/Planetina.webp',caption='Planetina from Rick and Morty [1]')
    #c2.image("images/tree1.jpg",caption= 'Tree, Clouds, Fields image. Free for use')
    c2.markdown(
        """
        **References:**
        1.	"Fandom Contributors." "Planetina." Rick and Morty Wiki, Fandom, https://rickandmorty.fandom.com/wiki/Planetina.
        
        **GitHub Repo**
        [Data Visualization Final Project](https://github.com/acsheller/dv_final)

    """
    )    
    

if page == 'U.S. Temperature Outliers':
    
    @st.cache_data(show_spinner=True)
    def get_WO_data():
        
        df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv',engine='pyarrow',dtype_backend='pyarrow')
        return df


    def get_max_temp_data_for_plot(df):
        
        #df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv')
        results = df.groupby('year')['max_temp'].mean()
        return results.to_frame().reset_index()


    def get_min_temp_data_for_plot(df):
        
        #df = pd.read_csv('data/weather-anomalies-1964-2013-ymd-40k.csv')
        results = df.groupby('year')['min_temp'].mean()
        return results.to_frame().reset_index()

    def plot_max_temp(df):
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),df.max_temp.to_numpy(),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        sc_plot = go.Scatter(x=df.year, y=df.max_temp ,mode='markers',
                                 name='Max Outlier Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Max US Temperature Outlier 1964 - 2013',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')

        return fig


    def plot_min_temp(df):
        #print(df)
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),df.min_temp.to_numpy(),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        # Add a line trace
        sc_plot = go.Scatter(x=df.year, y=df.min_temp ,mode='markers',
                                 name='Min Outlier Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Min US Temperature Outlier 1964 - 2013',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')
        return fig

    try:
        st.markdown(
        """
        <script>
        // Function to scroll to the top of the page
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Scroll to top on page load
        window.onload = function() {
            scrollToTop();
        };
        </script>
        """,
        unsafe_allow_html=True
        )


        states_list =  list(get_WO_data().state.unique())
        #print(type(states_list))
        #print(states_list.sort())
        states_list.sort()
        ab = ['All']
        ab.extend(states_list)
        state = st.sidebar.selectbox("Choose a Specific State",ab )
        data = get_WO_data()
        if state != 'All':
            data = data[data.state == state]



        c1.header("US Temperature Outlier 1964 - 2013")
        c1.markdown(
        """
        **Overview**
        This dataset is from [data.world](https://data.world/carlvlewis/u-s-weather-outliers-1964/workspace/intro) and presents
        temperature outliers from 1964 to 2013.
        
        Each entry represents a report from a weather station with high or low temperatures that were historical outliers 
        within that month, averaged over time. Note: This table's columns contain data that was collected from [NOAA](https://www.ncei.noaa.gov/).

        """

        )
        c1.map(data)
        c1.dataframe(data)
        c2.subheader('Temperature Trends 1964 - 2013')
        c2.markdown(
        """
        **Observations**

        The maximum and minimum temperatures were averaged over the year. What is disturbing is that both maximum and minimum are inceraseing.
        One might expect this with the climate situation the way it is (not very good: global warming for example).
        
        """
        )

        fig = plot_max_temp(get_max_temp_data_for_plot(data))
        c2.plotly_chart(fig)
        fig2 = plot_min_temp(get_min_temp_data_for_plot(data))
        c2.plotly_chart(fig2)


    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )

elif page == 'U.S. Weather Radars':

    def assign_color(row):
        if row['radartype'] == 'NEXRAD':
            return "#cc000000"

        else:
            return "#000000ff"
        

    #@st.cache_data(show_spinner=True)
    def get_WR_data(what=None,state = 'All'):
        df = pd.read_csv('data/weather_radar_stations_state.csv')
        print("State is {}".format(state))
        df.rename(columns={'y': 'lat','x':'lon'}, inplace=True)
        df['color']=df.apply(lambda row: assign_color(row),axis=1)
        print("What is {}".format(what))
        if what == None:
            if state == 'All':
                print("returning df for ALL")
                return df
            else:
                print("NOT ALL State is {}".format(state))
                df = df.loc[df['state'] == state]
                print("PAST CREATING DF\n {}".format(df))
                return df
        elif what == 'NEXRAD':
            df = df[df.radartype=='NEXRAD']
            if state == 'All':
                print("Returning nexrad All")
                return df
            else:
                print("Returning nexrad by state")
                return df[df.state == state]
        elif what == "TDWR":
            df = df[df.radartype=='TDWR']
            if state == 'All':
                return df
            else:
                return df[df.state == state]

    try:
        st.markdown(
        """
        <script>
        // Function to scroll to the top of the page
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Scroll to top on page load
        window.onload = function() {
            scrollToTop();
        };
        </script>
        """,
        unsafe_allow_html=True
        )

        c1.header("US Weather Radar Stations")
        c1.markdown(
        """
        **Overview**
        This dataset is from [data.world](https://data.world/dhs/weather-radar-stations) and presents
        Next Generation Radar (NEXRAD) and Terminal Doppler Weather Radar (TDWR) stations within the US. 
        
        The NEXRAD radars are operatoed by National Oceanic and Atmospheric Administration (NOAA).
        The TWDR radar stations are operated by teh Federal Aviation Administration (FAA).

        Each radar can measure out to 460km.
        """

        )

        #c1.map(get_WR_data(), color='color')
        r_type = st.sidebar.radio("Select Radar Type",('All','NEXRAD','TDWR'))
        import numpy as np
        states_list =  list(get_WR_data(what=None).state.unique())
        #print(type(states_list))
        #print(states_list.sort())
        states_list.sort()
        ab = ['All']
        ab.extend(states_list)
        state = st.sidebar.selectbox("Choose a Specific State",ab )
        data = ""
        if r_type == 'All':
            st.subheader("Both TDWR and NEXRAD")
            if state == 'All':
                data = get_WR_data(what=None,state=state)
                print("Data size is {}".format(len(data)))
                st.map(data)
            else:
                print("State is {}".format(state))
                data = get_WR_data(what=None,state=state)
                st.map(data)
        elif r_type == 'TDWR':
            data = get_WR_data(what='TDWR',state=state)
            st.subheader("TDWR -- Terminal Doppler Weather Radar")
            if len(data) == 0:
                c2.markdown(
                    """
                    **No Data Available**
                    """)
            st.map(data)
        elif r_type == 'NEXRAD':
            st.subheader("NEXRAD -- Next Generation Radar Sites")
            data = get_WR_data(what='NEXRAD',state=state)
            if len(data) == 0:
                c2.markdown(
                    """
                    **No Data Available**
                    """)
            st.map(data)
        st.dataframe(data)
        
    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )

elif page == 'Global Temperature Averages since 1750':

    @st.cache_data(show_spinner=True)
    def get_gltm_data(what=None,country='All'):

        df = pd.read_csv('data/globallandtemperaturesbymajorcity-ymd.csv')
        if country=='All':
            print("Returning Country == All")
            return df.groupby('country', group_keys=False).apply(lambda x: x.sample(400))
        else:
            print("Returning country = {}".format(country))
            return df[df.country==country]


    def plot_temp(df):
        import plotly.graph_objects as go
        import numpy as np
        coefficients = np.polyfit(df.year.to_numpy(),df.avg_yrly_temp.to_numpy(),1)
        trendline = np.polyval(coefficients,df.year.to_numpy())
        sc_plot = go.Scatter(x=df.year, y=df.avg_yrly_temp ,mode='markers',
                                 name='Global Average Temperatures')
        trend_plot = go.Scatter(x=df.year, y=trendline ,mode='lines',
                                 name='Trendline')
        fig = go.Figure(data=[sc_plot,trend_plot])
        fig.update_layout(title='Global Temperature Averages Trend',
                        xaxis_title='Year',
                        yaxis_title='Temp in Degress C')

        return fig

    def plot_heatmap(df, its_type='year',country='All'):
        import plotly.express as px

        fig = px.imshow(df, x=df.columns, y=df.index)
        if its_type == 'year':
            fig.update_layout(title='Heatmap --Global Temperature Averages Trend',width=700,height=500)
        elif its_type == 'month':
            fig.update_layout(title='Heatmap --Global Temperature Averages Trend {}'.format(country),width=700,height=500,xaxis_type='category')
        return fig        

    try:
        st.markdown(
        """
        <script>
        // Function to scroll to the top of the page
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Scroll to top on page load
        window.onload = function() {
            scrollToTop();
        };
        </script>
        """,
        unsafe_allow_html=True
        )



        c1.header("Global Tempertures by Country since 1750")
        c1.markdown("""
        This data [Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
        Compiling global temperature readings  since 1750.

        Collection techniques have improved since 1750 and there is greater and more robust collection.
        Note that not all countries have data dating back to 1750.

        """
        )
        country_list =  list(get_gltm_data(what=None).country.unique())
        country_list.sort()
        ab = ['All']
        ab.extend(country_list)

        country = st.sidebar.selectbox("Choose a Specific Country",ab )

        data = get_gltm_data(what=None,country=country)
        data2 = data.groupby(['year'])['averagetemperature'].mean().reset_index(name='avg_yrly_temp')
        print(data2.head())
        c1.map(data)
        c1.dataframe(data)
        fig = plot_temp(data2)
        c2.plotly_chart(fig)
        if country=='All':
            data3 = data.groupby(['country','year'])['averagetemperature'].mean().reset_index(name='avg_yrly_temp')
            data3 = data3.pivot(index='country', columns='year')['avg_yrly_temp'].fillna(0)
            fig2 = plot_heatmap(data3)
            c2.plotly_chart(fig2)
        else:

            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            data3 = data.groupby(['month','year'])['averagetemperature'].mean().reset_index(name='avg_yrly_temp')
            print(data3.info())
            #data['month_str'] =data.apply(lambda x: months[x-1])
            #data3 = data.groupby(['month_str','year'])['averagetemperature'].mean().reset_index(name='avg_yrly_temp')
            data3 = data3.pivot(index='month', columns='year')['avg_yrly_temp'].fillna(0)
            print(data3.info())
            print(data3.head())
            fig2 = plot_heatmap(data3,its_type='month',country=country)
            c2.plotly_chart(fig2)

    except URLError as e:
        st.error(
            """
            **Something went wrong**

            Connection error: %s
        """
            % e.reason
        )