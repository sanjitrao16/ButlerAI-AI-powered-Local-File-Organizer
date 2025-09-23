import os
import datetime
import calendar

def group_files_by_year(files):
  ''' Grouping files by year 
  
  JSON Structure

  {
  
  "2025" : [file_path1,file_path2]
  "2024" : [file_path3,file_path4]

  }
  
  '''
  year_object = {}
  for file in files:
    timestamp = os.path.getmtime(file)
    dt = datetime.datetime.fromtimestamp(timestamp)
    year = str(dt.year)

    if year not in year_object:
      year_object[year] = []
    
    year_object[year].append(file)
  
  return year_object

def group_files_by_year_month(files):
  ''' Grouping files by year-month
  
  JSON Structure

  {
  
  "2025-January" : [file_path1,file_path2]
  "2024-September" : [file_path3,file_path4]

  }
  '''

  year_month_object = {}

  for file in files:
    timestamp = os.path.getmtime(file)
    dt = datetime.datetime.fromtimestamp(timestamp)
    year_month_key = f"{dt.year}-{calendar.month_name[dt.month]}"

    if year_month_key not in year_month_object:
      year_month_object[year_month_key] = []

    year_month_object[year_month_key].append(file)
  
  return year_month_object