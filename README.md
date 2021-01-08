# Ookla_map

This code is for a dashboard that shows average downlink speeds in Finland using [Ookla open data set](https://www.speedtest.net/insights/blog/announcing-ookla-open-datasets)

Ookla data set is available via the [Registry of Open Data on AWS](https://registry.opendata.aws/speedtest-global-performance/) in Apache Parquet and Shapefile formats. The data is to be used under the [Creative Commons license for non-commercial use](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

Ookla's technical documentation and tutorials are available on [GitHub](https://github.com/teamookla/ookla-open-data).
[Here](https://github.com/teamookla/ookla-open-data/blob/master/tutorials/aggregate_by_county_py.ipynb) is a tutorial for analyzing download speeds in Kentucky counties using Python.

Project Organization
------------

    ├── FinlandDta
    │   ├── external                  <- Data from third party sources.
    │   ├── interim                   <- Intermediate data that has been transformed.
    │   ├── processed                 <- The final, canonical data sets for modeling.
    │   └── raw                       <- The original, immutable data dump.
    │
    ├── notebooks          
    │   ├── exploratory               <- Jupyter notebooks used for EDA, data exploration
    │   └── final                     <- Jupyter notebooks in a finalized form.
    │    
    ├── other                         <- Other supporting files/material.
    │   └── html_graph_versions       <- Interactive html version of each graph.
    │
    ├── references                    <- Data dictionaries, manuals, and all other exploratory
    │                                    material
    │
    ├── sql                           <- SQL code.
    │
    ├── src                           <- Source code for use in this project.
    │   ├── __init__.py               <- Makes src a Python module.
    │   │
    │   ├── data                      <- Scripts to download or generate data.
    │   │   └── make_dataset.py
    │   │
    │   ├── main                      <- Main code.
    │   │   ├── main.py
    │   │   ├── dataset_build.py      <- Fucntions that reformat the data for the dashboard graphs.
    │   │   └── helper_functions.py   <- Supporting functions.
    │   │
    │   └── modules                   <- Modules to be imported in the main code.
    │       └── vizualizations.py     <- Scripts to create results oriented visualizations.
    │            
    ├── README.md                     <- The top-level README for developers using this project.
    │                
    └── requirements.txt              <- The requirements file for reproducing the analysis
                                        environment, e.g.generated with
                                        `conda freeze -e > requirements.txt`.
