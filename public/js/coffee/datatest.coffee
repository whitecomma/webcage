d3.json '/archive.json', (err, ds) ->
  ds = d3.nest()
  .key((d) -> d.species)
  .sortKeys(d3.ascending)
  .sortValues((a, b) ->
    d3.ascending(a.dataName, b.dataName)
  )
  .entries(ds)

  for i in ds
    for j in i.values
      j['key'] = j['dataName']
      `delete j['dataName']`
      j['url'] = "/download/#{j['id']}/#{j['key']}"
    i['_values'] = i['values']
    `delete i['values']`

  for i in ds
    i['_values'] = d3.nest()
    .key((d) -> d.cellType)
    .sortKeys(d3.ascending)
    .entries(i['_values'])
    for j in i['_values']
      j['_values'] = [
        {
          "key": "model"
          "url": j.key
        }
        {
          "key": "Data Set"
          "_values": j['values']
        }
      ]
      `delete j['values']`

  ds = [
    {
      key: "All"
      values: ds
    }
  ]

  dataCol = [
    {
      key: 'key'
      label: 'Data'
      showCount: false
      width: '40%'
      type: 'text'
      classes: (d) -> if d.url then 'clickable name' else 'name'
      click: (d) -> if d.url then window.location.href = d.url
    }
    {
      key: 'name'
      label: 'Uploader'
      width: '20%'
      type: 'text'
    }
    {
      key: 'org'
      label: 'organization'
      width: '20%'
      type: 'text'
    }
    {
      key: 'lastUpdate'
      label: 'Last Update'
      width: '20%'
      type: 'text'
    }
  ]

  nv.addGraph () ->
    chart = nv.models.indentedTree()
    .columns(dataCol)
    d3.select('#vis')
    .datum(ds)
    .call(chart)


