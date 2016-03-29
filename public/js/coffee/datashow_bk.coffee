ds = [
  key: 'NVD3'
  values: [
    {
      key: "Charts"
      _values: [
        {
          key: "Simple Line"
          type: "Historical"
          url: "http://novus.github.com/nvd3/ghpages/line.html"
        }
        {
          key: "Scatter / Bubble"
          type: "Snapshot"
          url: "http://novus.github.com/nvd3/ghpages/scatter.html"
        }
      ]
    }
    {
      key: "Chart Components"
      _values: [
        {
          key: "Legend"
          type: "Universal"
          url: "http://novus.github.com/nvd3/examples/legend.html"
        }
      ]
    }
  ]
]


dataCol = [
  {
    key: 'key'
    label: 'Name'
    showCount: true
    width: '75%'
    type: 'text'
    classes: (d) -> if d.url then 'clickable name' else 'name'
    click: (d) -> if d.url then window.location.href = d.url
  }
  {
    key: 'type'
    label: 'Type'
    width: '25%'
    type: 'text'
  }
]

nv.addGraph () ->
  chart = nv.models.indentedTree()
  .columns(dataCol)

  d3.select('#vis')
  .datum(ds)
  .call(chart)
