library(shinydashboard)
library(shiny)
library(leaflet)
library(plotly)
library(normalr)
library(rgdal)
library(zipcode)

data("zipcode")

##### Extract zip in your working directory
shp <- readOGR(dsn = 'cb_2017_us_zcta510_500k.shp',layer = 'cb_2017_us_zcta510_500k')

frame = read.csv('data_final.csv')

shp = merge(x = shp,y = frame,by.x = 'GEOID10',by.y = 'zip',all.x = T)
shp@data[is.na(shp$Rank1),][6:23] = 0

shp$Category <- factor(shp$Rank1,
                       levels = c(5,4,3,2,1,0),
                       labels = c('Excellent','Good','Average',"Below Average",'Poor',"Nil"))

x<-colnames(frame)[4:16]
y<-colnames(frame)[2:3]

ui = dashboardPage(
  dashboardHeader(title = "ADAlytix"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Heatmap", tabName = "heatmap"),
      menuItem("Scatter Plot", tabName = "scatter"),
      menuItem("Correlation", tabName = "correlation")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem("heatmap",
              fluidPage(fluidRow(width=12,
                                 column(width = 4,selectInput("state", "State",
                                                              unique(frame$state), selected = 'Texas',multiple = F)),
                                 column(width = 4,selectInput("city", "City",
                                                              unique(frame$city),'Dallas',multiple = F))
                                 
                                 
              ),
              fluidRow(width = 12,
                       column(12,leafletOutput("map",height = 400))
              ),br(),
              fluidRow(width = 12,
                       column(width = 4,selectInput('variable','Variable',
                                                    c('Current Population','Distance in Miles',
                                                      'Age Median','White Race','Overall Crime','Total Households',
                                                      'Households Value','Average Income','Overall Costs'),multiple = F))
              ),
              fluidRow(width = 12,
                       column(12,leafletOutput("map1",height = 400))
                       )
              )
      ),
      tabItem("scatter",
              fluidPage(
                fluidRow(width = 12,
                  column(width=3,selectInput("xaxis1","X-Axis:",x)),
                  column(width=3,selectInput("yaxis1","Y-Axis:",y))
                ),br(),
                fluidRow(width = 12,
                         plotlyOutput("plot1")),
                br(),br(),
                fluidRow(width =12,
                  column(width=3,selectInput("xaxis2","X-Axis:",x)),
                  column(width=3,selectInput("yaxis2","Y-Axis:",x)),
                  column(width=3,selectInput("zaxis2","Z-Axis:",y))
                ),br(),
                fluidRow(width = 12,
                         plotlyOutput("plot2"))
              )
      )
      # tabItem("correlation",
      #           fluidPage()
      # )
      
    )
  )
)

server = function(session,input,output){
  
  ########## Heat Map ################
  choices <- reactive({
    switch (input$state,
            'Texas' = 'TX',
            'Utah' = 'UT',
            'Virginia' = 'VA'
    )
  })
  
  data <- reactive({
    shp[shp$GEOID10 %in% zipcode[zipcode$state %in% choices() & zipcode$city %in% input$city,]$zip,] #choices()
    
  })
  
  observeEvent(input$state,{
    updateSelectInput(session,'city','City',
                      choices = unique(frame[frame$state == input$state,]$city))
  })
  
  output$map <- renderLeaflet({
    
    pal <- colorFactor(c('#09ef4d','#b1ef09','#2bef09','#09efef',"#1809ef",'#ebef09',"#ef090c"), data()$Category) # green,dark blue, light blue,orange,red
    
    leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
      addTiles() %>% 
      addPolygons(fillColor = ~pal(data()$Category),weight = 3,
                  label = paste(data()$GEOID10,'-',data()$Category),
                  color = 'black'
      ) %>%
      addLegend(pal = pal,values = data()$Category,position = 'bottomright',title = 'Performance in Different Regions')
  })
  
  
  
  observeEvent(input$variable,{
    
    if(input$variable == 'Current Population'){
      
      bins = c(0,100,10000,30000,70000,101000)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$population_current,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$population_current),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$population_current),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$population_current,title = 'Current Population')
      })
      
    }
    
    if(input$variable == 'Distance in Miles'){
      
      bins = c(0,10,30,50,70,100)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$distance_in_miles,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$distance_in_miles),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$distance_in_miles),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$distance_in_miles,title = 'Distance in Miles')
      })
      
    }
    
    if(input$variable == 'Age Median'){
      
      bins = c(20,25,30,35,40,60)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$age_median,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$age_median),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$age_median),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$age_median,title = 'Age Median')
      })
      
    }
    
    if(input$variable == 'White Race'){
      
      bins = c(0,10,30,50,70,100)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$race_white,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$race_white),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$race_white),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$race_white,title = 'White Race')
      })
      
    }
    
    if(input$variable == 'Overall Crime'){
      
      bins = c(0,10,30,50,70,100,150,200)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$crime_overall,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$crime_overall),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$crime_overall),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$crime_overall,title = 'Overall Crime')
      })
      
    }
    
    if(input$variable == 'Total Households'){
      
      bins = c(0,5000,10000,15000,20000,25000,30000,40000)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$households_total,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$households_total),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$households_total),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$households_total,title = 'Total Households')
      })
      
    }
    
    if(input$variable == 'Households Value'){
      
      bins = c(0,10000,100000,300000,500000,700000,900000,1000000)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$households_value,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$households_value),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$households_value),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$households_value,title = 'Households Value')
      })
      
    }
    
    if(input$variable == 'Average Income'){
      
      bins = c(0,30000,70000,100000,150000,200000,250000,300000)
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$income_average,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$income_average),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$income_average),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$income_average,title = 'Average Income')
      })
      
    }
    
    if(input$variable == 'Overall Costs'){
      
      bins = c(0,10,30,50,70,100,150,200) 
      pal <- colorBin(c("#ef090c",'#ebef09',"#1809ef",'#09efef','#2bef09','#b1ef09','#09ef4d'), 
                      data()$costs_overall,
                      bins = bins)
      
      output$map1 <- renderLeaflet({
        
        leaflet(data(),options = leafletOptions(zoomControl = FALSE)) %>% 
          addTiles() %>% 
          addPolygons(fillColor = ~pal(data()$costs_overall),weight = 3,
                      label = paste(data()$GEOID10,'-',data()$costs_overall),
                      color = 'black'
          ) %>%
          addLegend(position = 'bottomright',pal = pal,values = data()$costs_overall,title = 'Overall Costs')
      })
      
    }
    
  })
  
  ######### scatter plot #########
  
  output$plot1 <- renderPlotly({
    plot_ly(data = frame, x = frame[[input$xaxis1]], y = frame[[input$yaxis1]])%>%
      layout(xaxis = list(title=input$xaxis1), yaxis = list(title=input$yaxis1))
  })
  range01 <- function(x){(x-min(x))/(max(x)-min(x))}
  output$plot2 <- renderPlotly({
    plot_ly(frame, x = frame[[input$xaxis2]], y = frame[[input$yaxis2]], text = ~zip, type = 'scatter', mode = 'markers',
            marker = list(size = range01(frame[[input$zaxis2]])*30, opacity = 0.5)) %>%
      layout(title = paste('Bubble Chart of ',input$xaxis2,' vs ',input$yaxis2,' for ',input$zaxis2,sep=' '),
             xaxis = list(showgrid = FALSE),
             yaxis = list(showgrid = FALSE))
  })
  
}

shinyApp(ui,server)