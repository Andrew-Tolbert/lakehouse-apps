from datetime import datetime
import pytz
import streamlit as st

def deploy_time():
  # Get the current time in EST
  est_tz = pytz.timezone('America/New_York')
  current_time = datetime.now(est_tz)
  # Format the datetime
  formatted_time = current_time.strftime("%Y-%m-%d %I:%M:%S %p %Z")  
  return formatted_time 