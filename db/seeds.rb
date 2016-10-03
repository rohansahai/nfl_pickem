nflteams = [
"Arizona Cardinals",
"Atlanta Falcons",
"Baltimore Ravens",                  
"Buffalo Bills", 
"Carolina Panthers",                 
"Chicago Bears", 
"Cincinnati Bengals",                
"Cleveland Browns", 
"Dallas Cowboys",                    
"Denver Broncos", 
"Detroit Lions",                     
"Green Bay Packers", 
"Houston Texans",                    
"Indianapolis Colts", 
"Jacksonville Jaguars",              
"Kansas City Chiefs",
"Los Angeles Rams",
"Miami Dolphins",                    
"Minnesota Vikings", 
"New England Patriots",              
"New Orleans Saints", 
"New York Giants NYG",               
"New York Jets NYJ", 
"Oakland Raiders",                   
"Philadelphia Eagles", 
"Pittsburgh Steelers",               
"San Diego Chargers", 
"San Francisco 49ers",  
"Seattle Seahawks",
"Tampa Bay Buccaneers", 
"Tennessee Titans",                  
"Washington Redskins"
]

nflteams.each do|team|
  Team.create(name: team)
end