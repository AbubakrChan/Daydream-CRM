import streamlit as st
from streamlit_airtable import AirtableConnection
import streamlit_google_oauth as oauth
from pyairtable import Api, Base, Table, metadata
st.set_page_config(page_title='Daydream CRM ')
from streamlit.runtime.caching import cache_data
import pandas as pd
import json
import numpy as np




client_id = "1064852912425-m29ngfi8mc6bmo11crfjb99t01e93ddo.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "https://daydream-crm.streamlit.app"

st.header("Daydream CRM ")
import streamlit as st

import streamlit.components.v1 as components



if __name__ == "__main__":
    app_name = '''
    Please authenticate yourself before proceeding.
    '''
    app_desc = '''
    Daydream CRM uses <strong>Google Oauth</strong>.
    The user must have a google account to log in into the application.
    '''
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        app_name=app_name,
        app_desc=app_desc,
        logout_button_text="Logout",
    )
    if login_info:
        user_id, user_email = login_info
        st.write(f"Welcome {user_email}")

            # st.text('Upons clicking the check button an')
        # Create connection
        conn = st.experimental_connection("your_connection_name", type=AirtableConnection)

        # Retrieve base schema
        base_schema = conn.get_base_schema()
        # Get the first table's ID

        first_table = base_schema["tables"][0]
        st.markdown(f"First table ID: `{first_table['id']}` (named `{first_table['name']}`)")

        # Retrieve all records for the first table (pyAirtable paginates automatically)
        # (Note you can also pass in parameters supported by pyAirtable
        # (https://pyairtable.readthedocs.io/en/stable/api.html#parameters) such as as
        # max_records, view, sort, and formula into conn.query() like so:
        # table_records = conn.query(first_table["id"], max_records=25, view='viwXXX')
        table_records = conn.query(table_id=first_table["id"])
        # # Convert the dictionary to JSON
        # json_data = json.dumps(table_records)
        df2 = table_records.to_json()
        df = json.loads(df2)

        result = {
            "Name": df.get("Name", {})
            ,
            "Company/Fund": df.get("Company/Fund", {})
        }
        result_json = json.dumps(result, indent=4)
        
        json_data = json.loads(result_json)
        
        df = pd.DataFrame(json_data
        )
        


        def dataframe_with_selections(df):
            df_with_selections = df.copy()
            df_with_selections.insert(2, "Request_an_Intro", False)
                    # Boolean to resize the dataframe, stored as a session state variable
            st.checkbox("Use container width", value=True,key="use_container_width")

            # Display the dataframe and allow the user to stretch the dataframe
            # across the full width of the container, based on the checkbox value
            edited_df = st.data_editor(
                df_with_selections,
                hide_index=True,
                column_config={"Request_an_Intro": st.column_config.CheckboxColumn(required=True)},
                disabled=df.columns,
                use_container_width=st.session_state.use_container_width
            )
            # st.dataframe(edited_df, use_container_width=st.session_state.use_container_width)
            
            selected_indices = list(np.where(edited_df.Request_an_Intro)[0])
            selected_rows = df[edited_df.Request_an_Intro]

            return {"ggs":selected_indices ,"selected_rows": selected_rows}






        selection = dataframe_with_selections(df)
        # st.write(selection)

        if not selection["selected_rows"].empty:
            last_row = selection["selected_rows"].iloc[-1]
            name= last_row[0]
            company= last_row[1]
            st.write("You have selected " +  last_row[0])

            import resend

            resend.api_key = "re_eU6ku1aN_KXqc4Sos21xBHHEw4pY2jfds"

            params = {
                "from": "Daydream CRM <chan@abubakr.tech>",
                "to": ["changjonathan23@gmail.com"],
                "subject": "Introduction Requested!",
                "html": f"<strong>The user with the mail: {user_email} has requested introduction for the person with name: {name} and company: {company} </strong>",
            }

            # st.success('Your intro has been requested', icon="✅")

            st.toast('Your intro has been requested' , icon='😍')
            
            # custom_notification_box(icon='info', textDisplay='We are almost done with your registration...', externalLink='more info', url='#', styles=styles, key="foo")

            email = resend.Emails.send(params)
            params = {
                "from": "Daydream CRM <chan@abubakr.tech>",
                "to": [user_email],
                "subject": "Introduction Requested!",
                "html": f"<strong> Your Intro to the person with name: {name} and company: {company} is being worked on by the Daydream Team.</strong>",
            }
            # print(email)
            email = resend.Emails.send(params)
            
    
        selection["selected_rows"] = ""
        
        print(selection["selected_rows"])
        # st.write(selection["selected_rows"])
        st.markdown(f"{len(table_records)} records retrieved")
        # st.write(table_records)   
        import pandas as pd

        # Cache the dataframe so it's only loaded once
        @st.cache_data
        def load_data():
            return pd.DataFrame(
            table_records
            )


