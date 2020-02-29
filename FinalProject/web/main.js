Promise.all([
    d3.csv('../dataset/covid_confirmed_02_25_20.csv'),
    d3.csv('../dataset/covid_deaths_02_25_20.csv'),
    d3.csv('../dataset/covid_recovered_02_25_20.csv')
]).then(files => {

    var example_vis = null
    var map_vis = null

    console.log(files[0])

    data_confirmed = files[0]
    data_deaths = files[1]
    data_recovered = files[2]

    //example_vis = new ExampleVis(data_confirmed, '.example-vis-container', example_vis_dimensions)
    // map_vis = new MapVis(data_confirmed, 'mapid', map_vis_dimensions)
    new_map_vis = new NewMapVis(data_confirmed, 'map_container', map_vis_dimensions)
})

