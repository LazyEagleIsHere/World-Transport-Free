import pygame

tko_line_stations_name = {
  "Po Lam", "Hang Hau", "TKO", "LOHAS Park", "TKL", "Yau Tong", "Quarry Bay", "North Point"
}

tko_line_stations_pos = {
  "Po Lam": (100, 100), 
  "Hang Hau": (100, 150), 
  "TKO": (150, 150), 
  "LOHAS Park": (150, 200), 
  "TKL": (200, 150), 
  "Yau Tong": (250, 150), 
  "Quarry Bay": (250, 300), 
  "North Point": (300, 300)
}

# tko_line_stations_branches = {
#   "Po Lam": ["Hang Hau"], 
#   "Hang Hau": ["Po Lam"], 
#   "TKO": ["Hang Hau", "LOHAS Park", "TKL"], 
#   "LOHAS Park": ["TKO"], 
#   "TKL": ["TKO", "Yau Tong"], 
#   "Yau Tong": ["TKL", "Quarry Bay"], 
#   "Quarry Bay": ["Yau Tong", "North Point"], 
#   "North Point": ["Quarry Bay"]
# }

# linked with stations
tko_line_stations_branches = {
  "Po Lam": ["Hang Hau"], 
  "Hang Hau": ["TKO"], 
  "TKO": ["LOHAS Park", "TKL"], 
  "LOHAS Park": [], 
  "TKL": ["Yau Tong"], 
  "Yau Tong": ["Quarry Bay"], 
  "Quarry Bay": ["North Point"], 
  "North Point": []
}

tko_line_stations_opened = {name: True for name in tko_line_stations_name}

# tko_line_stations_opened = {
#   "Po Lam": True, 
#   "Hang Hau": False, 
#   "TKO": False, 
#   "LOHAS Park": False, 
#   "TKL": False, 
#   "Yau Tong": False,
#   "Quarry Bay": False, 
#   "North Point": False
# }