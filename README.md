# pathPlanner
This project demo optimizes on-road charging efficiency by accounting for battery charging rate decline to ensure a smoother journey to the destination.

## Instruction On How to Run the file

### Run backend only
1. Running the Backend via Jupyter Notebook
- The backend can be directly executed from the Jupyter Notebook.
- To test different cities and car types, manually alter the configuration section in the notebook:
    - Vancouver, Prince George, Chilliwack, Merritt, Banff, Clearwater, Jasper, Edson, Calgary, and Edmonton
    - Model3LR, Cybertruck is currently available

Note*: If the selected cities are very close, the path may result in no charging being required.


```
# Define start and end cities
# Vancouver, Prince George, Chilliwack, Merritt, Banff, Clearwater, Jasper, Edson, Calgary, and Edmonton
# Vancouver and Calgary as default. If 2 Cities are Too close, the path will result in no charging needed.

start_city = "Vancouver"
end_city = "Calgary"

# Model3LR, Cybertruck is currently available
car_type = "Model3LR"
```



## Backend File is divided into two parts 
```
pathPlanner/
├── backend/
│   ├── __init__.py
│   ├── app.py  
│   ├── controller.py  
│   ├── controller_notebook.py 
│   ├── venv/
│   ├── path_planner_package/
│   │   ├── __init__.py
│   │   ├── test_pathPlanner.py
│   │   └── path_planner.py  
│   ├── charging_strategy_optimizer/
│   │   ├── __init__.py
│   │   └── charging_strategy_optimizer.py 
│   ├── data/
│   │   ├── mapData.py      #Generate graph         
│   │   ├── Cars.json       # Data about cars and charging curves  
│   │   ├── nodes.json      # City and station data with coordinates           
│   │   └── graph.json             
│   │   └── Filtered_Charging_Stations__Updated_.csv # contain pre filtered data
├── ev_path_planner_with_controller.ipynb   
├── requirements.txt                        
├── venv/                                     
├── charging-strategy-frontend/  # Frontend folder 
├── .gitignore        
```

### Notes on the Backend Folders
1. controller.py and controller_notebook.py:
- `controller.py`: Handles standalone backend operations, such as shortest path and charging optimization.
- `controller_notebook.py`: Adapts backend logic for Jupyter Notebook execution.


2. path_planner_package:
- Contains path_planner.py, which handles shortest path computations and related graph algorithms.
- Provide an alternative path option in `path_planner` file

3. charging_strategy_optimizer:
- Optimizes EV charging strategies by leveraging segment distances and vehicle-specific parameters.

4. data:
- Contains essential data files:
    - Cars.json: Defines available car types and their charging curves.
    - nodes.json: Details nodes (cities and charging stations) with GPS coordinates.
        - City is mannuly added
        - Station is from the CSV file from `Transport Canada. (2024, October 22). Zero-Emission Vehicle Charging stations` wesbite
    - graph.json: Represents the route connections and distances between nodes.
    - mapData.py: construct the graph from the nodes.json


### Run frontend

Prerequisites
Download and install from Node.js official website.
Backend Service: Make sure the backend service is running on http://127.0.0.1:5000.
python3 app.py

1. Navigate to the Frontend Directory: Open a terminal or command prompt and navigate to the frontend folder:
cd pathPlanner/charging-strategy-frontend

2. Install Dependencies: Install the required npm packages by running:
   npm install
3. Start the Frontend: Start the development server with the following command
   npm start
