import os
import datetime

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
  
  print(year_object)
  
  return year_object